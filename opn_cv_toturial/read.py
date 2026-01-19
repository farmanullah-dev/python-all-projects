import cv2 as cv

# img = cv.imread(r"D:\#PICS\Camera Roll\2023_05_10_15_46_IMG_7276.JPG")
# #give the image height and width
# cv.imshow("Image",img)
# cv.waitKey(0)

#######################################****************************$######################################
# video capture 

# cap=cv.VideoCapture(r"D:\#PICS\Camera Roll\2019_10_26_06_35_IMG_8747.3GP")

# while True:
#     isTrue,frame=cap.read()
#     cv.imshow("Video",frame)
#     cv.imshow("video_resized",cv.resize(frame,(500,500)))
#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break

# cap.release()
# cv.destroyAllWindows()

####################*****************************####################################



 #  Read webcam
# cap = cv.VideoCapture(0)
# while True:
#         isTrue, frame = cap.read()
#         cv.imshow("Video", frame)
#         if cv.waitKey(20) & 0xFF == ord('d'):
#             break    
#             cap.release()    


####################*****************************##########

# import numpy as np

# black=np.zeros((512,512,3),np.uint8)
# cv.imshow("Black",black)
# cv.rectangle(black,(0,0),(250,250),(0,255,0),thickness=2)
# cv.imshow("Rectangle",black)


# cv.circle(black,(300,250),100,(255,255,140),thickness=4)
# cv.imshow("Circle",black)

# cv.putText(black,"FARMAN",(200,400),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),thickness=2)
# cv.imshow("Text",black)

# cv.waitKey(0)

##################################***************####################################




# img = cv.imread(r"D:\#PICS\Camera Roll\2023_05_10_15_46_IMG_7276.JPG")

# blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)

# small = cv.resize(blur, (300, 300))

# canny=cv.Canny(img,125,175)

# res=cv.resize(canny,(300,300) )
# cv.imshow("canny",res)

# cv.imshow("Small Blurred Image", small)

# counters = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(img, counters[0], -1, (0, 255, 0), 2)
# counters_size=cv.resize(img,(300,300) )
# cv.imshow("Contours", counters_size) 
# cv.waitKey(0)
# cv.destroyAllWindows()


##################################***************####################################



# # Load image
# img = cv.imread(r"D:\#PICS\Life in Frames\1725346728267.jpg")

# # adaptive threshold method
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# # resize for better visualization
# gray = cv.resize(gray, (500, 500))
# adaptive_threshold = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
# cv.imshow("Adaptive Threshold", adaptive_threshold)
# cv.waitKey(0)
# cv.destroyAllWindows()

##################################***************####################################




# img = cv.imread(r"D:\#PICS\Life in Frames\1725346728267.jpg")

# # use laplacian method to detect edges
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# gray = cv.resize(gray, (500, 500))
# laplacian = cv.Laplacian(gray, cv.CV_64F)
# cv.imshow("Laplacian", laplacian)
# cv.waitKey(0)
# cv.destroyAllWindows()


##################################***************####################################





img = cv.imread(r"D:\#PICS\Camera Roll\2021_07_30_10_03_IMG_3173.JPG")


img2 = cv.resize(img, (500, 500))
cv.imshow("Original", img2)


gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

cv.imshow("Gray", gray)

# Load Haar Cascade (using built-in OpenCV path)
haar_case = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# Detect faces
facce_rect = haar_case.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
print("No of faces found:", len(facce_rect))

# Draw rectangles
for (x, y, w, h) in facce_rect:
    cv.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

cv.imshow("Detected Face", img2)

cv.waitKey(0)
cv.destroyAllWindows()


