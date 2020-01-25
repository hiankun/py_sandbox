import numpy as np
import cv2


frame = cv2.imread('/home/thk/Desktop/trump.jpg', cv2.IMREAD_COLOR)
ref = cv2.imread('/home/thk/Desktop/cartoon.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

sigmaColor = 60
sigmaSpace = 5 ## large value will slow down the program dramatically

# Color
#filtered_color = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
filtered_color = cv2.bilateralFilter(filtered_color, -1, sigmaColor, sigmaSpace)
#filtered_color = cv2.resize(filtered_color, (0,0), fx=2, fy=2)

# Sketch
blurred = cv2.GaussianBlur(gray,(3,3),0,0)
laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize = 5, scale = 1, delta = 0)
_, edges = cv2.threshold(laplacian, 120, 255, cv2.THRESH_BINARY_INV)
edges_3ch = cv2.merge((edges,edges,edges))

res = cv2.bitwise_and(filtered_color, edges_3ch)

cv2.imshow('filtered_color', np.hstack((filtered_color, edges_3ch, res, ref)))
cv2.waitKey(0)

cv2.destroyAllWindows()
