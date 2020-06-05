import os
import cv2
import numpy as np
from datetime import datetime
import calib_res

DIM = calib_res.DIM
K = calib_res.K
D = calib_res.D


def undistort(img, balance=0.0, dim2=None, dim3=None):
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort    
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"    
    
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1    

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K 
    # used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D,
            dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, 
            np.eye(3), new_K, DIM, cv2.CV_16SC2)
    return cv2.remap(img, map1, map2, 
            interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


def main():
  cam = cv2.VideoCapture(0)

  while True:
    _, frame = cam.read()

    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
      break

    #map1, map2 = cv2.fisheye.initUndistortRectifyMap(
    #        K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    #rect_frame = cv2.remap(frame, map1, map2, 
    #        interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    rect_frame = undistort(frame, balance=0.8)
    res = np.hstack((frame, rect_frame))
    cv2.imshow('res', res)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
