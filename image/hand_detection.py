import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

# Window name and settings
cv2.namedWindow("Color Adjustments", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Color Adjustments", 300, 300)

# Create trackbars for color adjustment and thresholding
def nothing(x):
    pass

cv2.createTrackbar("Thresh", "Color Adjustments", 0, 255, nothing)
cv2.createTrackbar("Lower_H", "Color Adjustments", 0, 255, nothing)
cv2.createTrackbar("Lower_S", "Color Adjustments", 0, 255, nothing)
cv2.createTrackbar("Lower_V", "Color Adjustments", 0, 255, nothing)
cv2.createTrackbar("Upper_H", "Color Adjustments", 255, 255, nothing)
cv2.createTrackbar("Upper_S", "Color Adjustments", 255, 255, nothing)
cv2.createTrackbar("Upper_V", "Color Adjustments", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        break

    frame = cv2.resize(frame, (400, 400))

    # Apply Gaussian Blur to reduce noise
    blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)

    # Convert frame to HSV
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # Get current positions of the trackbars
    l_h = cv2.getTrackbarPos("Lower_H", "Color Adjustments")
    l_s = cv2.getTrackbarPos("Lower_S", "Color Adjustments")
    l_v = cv2.getTrackbarPos("Lower_V", "Color Adjustments")
    u_h = cv2.getTrackbarPos("Upper_H", "Color Adjustments")
    u_s = cv2.getTrackbarPos("Upper_S", "Color Adjustments")
    u_v = cv2.getTrackbarPos("Upper_V", "Color Adjustments")

    # Define the lower and upper bounds for color thresholding
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # Create a mask based on the lower and upper bounds
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply morphological operations (opening to reduce noise)
    kernel = np.ones((5, 5), np.uint8)
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Filter the mask with the original image
    filtered = cv2.bitwise_and(frame, frame, mask=mask_clean)

    # Invert the mask
    mask_inv = cv2.bitwise_not(mask_clean)

    # Thresholding
    thresh_val = cv2.getTrackbarPos("Thresh", "Color Adjustments")
    ret, thresh = cv2.threshold(mask_inv, thresh_val, 255, cv2.THRESH_BINARY)

    # Dilation to enhance the contours
    dilated = cv2.dilate(thresh, None, iterations=6)

    # Find contours
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and draw large contours only
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Draw only if the contour area is larger than a threshold
            frame = cv2.drawContours(frame, [cnt], -1, (176, 10, 15), 4)

    # Display the result
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Mask", mask_clean)
    cv2.imshow("Filtered", filtered)
    cv2.imshow("Result", frame)

    # Exit on 'Esc' key
    key = cv2.waitKey(50) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
