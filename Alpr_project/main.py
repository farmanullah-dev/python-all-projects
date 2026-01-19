# main.py — improved ALPR with preprocessing, multi-variant OCR & majority voting
import cv2
import csv
import collections
import numpy as np
from ultralytics import YOLO
import easyocr
from sort import Sort
import util
from util import format_license, license_complies_format  # from your util.py

# ---------------- CONFIG ----------------
VIDEO_PATH = r"F:\python\Alpr_project\2103099-uhd_3840_2160_30fps.mp4"
PLATE_MODEL_PATH = r"F:\python\Alpr_project\license-detector.pt"
OUTPUT_VIDEO = "alpr_annotated.mp4"
OUTPUT_CSV = "alpr_results.csv"

DISPLAY_SIZE = (1280, 720)     
OCR_TARGET_HEIGHT = 140      
HISTORY_LEN = 9                
MIN_OCR_CONF = 0.35          
MIN_PLATE_AREA = 1000         
YOLO_CONF = 0.20            
YOLO_IOU = 0.45
# ----------------------------------------

# load detectors and OCR
plate_detector = YOLO(PLATE_MODEL_PATH)
reader = easyocr.Reader(['en'], gpu=False)  # set gpu=True if you have CUDA available

tracker = Sort()  # ensure sort.py present

# state: per-track history for majority voting
track_history = collections.defaultdict(collections.deque)  # track_id -> deque(texts)
track_best = {}  # track_id -> stable plate

# prepare video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open video: {VIDEO_PATH}")

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

# CSV writer
csv_file = open(OUTPUT_CSV, "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame", "track_id", "plate_text", "plate_conf", "bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2", "stable"])

# ----- helper functions -----
def preprocess_variants(plate_bgr):
    """
    Return a list of image variants (BGR) to try OCR on.
    Variants include resized color, CLAHE-equalized, denoised, thresholded, inverted.
    """
    variants = []
    if plate_bgr is None or plate_bgr.size == 0:
        return variants

    h, w = plate_bgr.shape[:2]
    # upscale to target height while preserving aspect
    new_h = OCR_TARGET_HEIGHT
    scale = new_h / max(1, h)
    new_w = max(10, int(w * scale))
    try:
        resized = cv2.resize(plate_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    except Exception:
        resized = plate_bgr.copy()

    variants.append(resized)  # raw resized

    # grayscale + CLAHE
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(gray)
    variants.append(cv2.cvtColor(cl, cv2.COLOR_GRAY2BGR))

    # denoise (bilateral) + equalize
    den = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    den_eq = cv2.equalizeHist(den)
    variants.append(cv2.cvtColor(den_eq, cv2.COLOR_GRAY2BGR))

    # adaptive threshold
    try:
        thr = cv2.adaptiveThreshold(den_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
        variants.append(cv2.cvtColor(thr, cv2.COLOR_GRAY2BGR))
        variants.append(cv2.cvtColor(cv2.bitwise_not(thr), cv2.COLOR_GRAY2BGR))  # inverted
    except Exception:
        pass

    return variants


def best_ocr_from_variants(variants):
    """
    Run EasyOCR on each variant, return best (formatted_text, confidence) that passes license format.
    """
    best_text = None
    best_conf = 0.0
    for img in variants:
        try:
            ocr_res = reader.readtext(img)  # list of [bbox, text, conf]
        except Exception:
            ocr_res = []
        for bbox, text, conf in ocr_res:
            if not text:
                continue
            txt = ''.join(filter(str.isalnum, text.upper()))
            # check format with your util function
            if license_complies_format(txt):
                formatted = format_license(txt)
                if conf > best_conf:
                    best_conf = float(conf)
                    best_text = formatted
    return best_text, best_conf


# main loop
frame_idx = -1
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1

    # detect plates on full frame - increase imgsz if plates are small (tradeoff: slower)
    # you can pass imgsz param to YOLO call; adjust if needed (e.g., imgsz=1280)
    plate_preds = plate_detector(frame, imgsz=1280, conf=YOLO_CONF, iou=YOLO_IOU)[0]

    # convert boxes to list
    boxes = plate_preds.boxes.data.tolist() if plate_preds is not None else []

    # for SORT we need detection list if we want to track vehicles; here we will use plate box center for tracking
    # Convert plate boxes to detections for tracker: x1,y1,x2,y2,score
    detections_for_sort = []
    for b in boxes:
        x1, y1, x2, y2, score, cls = b
        area = max(0, (x2 - x1) * (y2 - y1))
        if area < MIN_PLATE_AREA:
            continue
        detections_for_sort.append([x1, y1, x2, y2, score])

    # update tracker
    if len(detections_for_sort) > 0:
        tracked = tracker.update(np.asarray(detections_for_sort))
    else:
        tracked = np.empty((0,5))

    # match tracked boxes to plate boxes by containment or IoU (we can use simple nearest match)
    # We'll iterate plate boxes and find track id if bounding box matches a returned tracker box.
    # Convert tracked to list for searching
    tracked_list = tracked.tolist() if tracked.size else []

    for b in boxes:
        px1, py1, px2, py2, pscore, pcls = b
        px1_i, py1_i, px2_i, py2_i = int(px1), int(py1), int(px2), int(py2)
        area = max(0, (px2_i - px1_i) * (py2_i - py1_i))
        if area < MIN_PLATE_AREA:
            continue

        # find matching track id (plate bbox inside tracker bbox)
        matched_track_id = -1
        for tr in tracked_list:
            tx1, ty1, tx2, ty2, tr_id = tr
            if px1 > tx1 and py1 > ty1 and px2 < tx2 and py2 < ty2:
                matched_track_id = int(tr_id)
                break
        # If no containment match, try IoU threshold match
        if matched_track_id == -1 and tracked_list:
            # compute IoU with each trk
            best_iou, best_id = 0.0, -1
            for tr in tracked_list:
                tx1, ty1, tx2, ty2, tr_id = tr
                xx1 = max(px1, tx1); yy1 = max(py1, ty1); xx2 = min(px2, tx2); yy2 = min(py2, ty2)
                w = max(0, xx2-xx1); h = max(0, yy2-yy1)
                inter = w*h
                union = area + max(0, (tx2-tx1)*(ty2-ty1)) - inter
                iou = inter/union if union>0 else 0
                if iou > best_iou:
                    best_iou, best_id = iou, int(tr_id)
            if best_iou > 0.25:
                matched_track_id = best_id

        # crop plate from full frame
        plate_crop = frame[py1_i:py2_i, px1_i:px2_i]
        if plate_crop.size == 0:
            continue

        # build variants and run OCR
        variants = preprocess_variants(plate_crop)
        best_text, best_conf = best_ocr_from_variants(variants)

        stable = False
        if best_text is not None and best_conf >= MIN_OCR_CONF and matched_track_id != -1:
            # add to history for the matched track
            dq = track_history[matched_track_id]
            dq.append(best_text)
            if len(dq) > HISTORY_LEN:
                dq.popleft()
            # majority vote
            most_common, count = collections.Counter(dq).most_common(1)[0]
            if count >= max(2, HISTORY_LEN//3):  # stable enough threshold
                track_best[matched_track_id] = most_common
                stable = True
        elif best_text is not None and matched_track_id == -1:
            # a detection without track; still record but mark unstable
            pass

        # annotate display frame (draw box & text: use majority if available)
        display_text = best_text if best_text is not None else ""
        if matched_track_id in track_best:
            display_text = track_best[matched_track_id]  # show stable version
        # draw rectangle and text
        cv2.rectangle(frame, (px1_i, py1_i), (px2_i, py2_i), (0, 255, 0), 2)
        cv2.putText(frame, f"{display_text}", (px1_i, max(py1_i-8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)

        
        csv_writer.writerow([frame_idx, matched_track_id if matched_track_id!=-1 else -1,
                             best_text if best_text else "", round(best_conf,3), px1_i, py1_i, px2_i, py2_i,
                             int(stable)])

    
    if out is None:
        out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, 20.0, DISPLAY_SIZE)

  
    disp = cv2.resize(frame, DISPLAY_SIZE)
    out.write(disp)
    cv2.imshow("ALPR (improved)", disp)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup
cap.release()
out.release()
csv_file.close()
cv2.destroyAllWindows()
