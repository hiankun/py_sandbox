import numpy as np
import cv2


sigmaColor = 60
sigmaSpace = 5 ## large value will slow down the program dramatically
cap = cv2.VideoCapture(1)

while True:
  _, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Color
  filtered_color = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
  filtered_color = cv2.bilateralFilter(filtered_color, -1, sigmaColor, sigmaSpace)
  filtered_color = cv2.resize(filtered_color, (0,0), fx=2, fy=2)

  # Sketch
  blurred = cv2.GaussianBlur(gray,(3,3),0,0)
  laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize = 5, scale = 1, delta = 0)
  _, edges = cv2.threshold(laplacian, 150, 255, cv2.THRESH_BINARY_INV)
  edges_3ch = cv2.merge((edges,edges,edges))
  
  res = cv2.bitwise_and(filtered_color, edges_3ch)
  cv2.imshow('frame', res)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()
