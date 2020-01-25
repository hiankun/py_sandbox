import numpy as np
import cv2


gray = cv2.imread('/home/thk/Desktop/trump.jpg', cv2.IMREAD_GRAYSCALE)
ref = cv2.imread('/home/thk/Desktop/pencilSketch.jpg', cv2.IMREAD_GRAYSCALE)

blurred = cv2.GaussianBlur(gray,(3,3),0,0)
laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize = 5, scale = 1, delta = 0)
#laplacian = (laplacian*255).astype("uint8")
#laplacian = cv2.bitwise_not(laplacian)
_, edges = cv2.threshold(laplacian, 120, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('frame', np.hstack((edges, ref)))
cv2.waitKey(0)

cv2.destroyAllWindows()
