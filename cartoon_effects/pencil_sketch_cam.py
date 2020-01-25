import numpy as np
import cv2


cap = cv2.VideoCapture(1)

while True:
  _, frame = cap.read(cv2.COLOR_BGR2GRAY)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  blurred = cv2.GaussianBlur(gray,(3,3),0,0)
  laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize = 5, scale = 1, delta = 0)
  _, edges = cv2.threshold(laplacian, 120, 255, cv2.THRESH_BINARY_INV)

  cv2.imshow('edges', edges)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()
