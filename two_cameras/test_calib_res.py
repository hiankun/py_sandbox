import os
import cv2
import numpy as np
from datetime import datetime
import calib_res

DIM = calib_res.DIM
K = calib_res.K
D = calib_res.D

def main():
  cam = cv2.VideoCapture(0)

  while True:
    _, frame = cam.read()

    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
      break

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
            K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    rect_frame = cv2.remap(frame, map1, map2, 
            interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    res = np.hstack((frame, rect_frame))
    cv2.imshow('res', res)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
