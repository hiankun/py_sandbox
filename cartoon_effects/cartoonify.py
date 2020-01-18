import numpy as np
import cv2


sigmaColor = 60
sigmaSpace = 5 ## large value will slow down the program dramatically
cap = cv2.VideoCapture(0)

while True:
  ret, frame = cap.read()

  frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
  frame = cv2.bilateralFilter(frame, -1, sigmaColor, sigmaSpace)
  frame = cv2.resize(frame, (0,0), fx=2, fy=2)
  cv2.imshow('frame', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()
