import cv2
import numpy as np

# Function called when trackbar is moved
def cross(x):
    pass

# Create blank page
img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow("Color Picker")

# Create switch
switch = "0: OFF\n1: ON"
cv2.createTrackbar(switch, "Color Picker", 0, 1, cross)

# Create trackbars for adjusting color
cv2.createTrackbar("R", "Color Picker", 0, 255, cross)
cv2.createTrackbar("G", "Color Picker", 0, 255, cross)
cv2.createTrackbar("B", "Color Picker", 0, 255, cross)

while True:
    cv2.imshow("Color Picker", img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Exit on 'Esc' key
        break

    # Get trackbar positions
    s = cv2.getTrackbarPos(switch, "Color Picker")
    r = cv2.getTrackbarPos("R", "Color Picker")
    g = cv2.getTrackbarPos("G", "Color Picker")
    b = cv2.getTrackbarPos("B", "Color Picker")

    # Update image color based on switch and RGB values
    if s == 1:
        img[:] = [b, g, r]  # OpenCV uses BGR format
    else:
        img[:] = [0, 0, 0]

cv2.destroyAllWindows()
