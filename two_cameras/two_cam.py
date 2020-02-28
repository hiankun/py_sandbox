import cv2
import numpy as np


def main():
  cam_1 = cv2.VideoCapture(1)
  cam_2 = cv2.VideoCapture(2)

  while True:
    _, frame_1 = cam_1.read()
    _, frame_2 = cam_2.read()

    res = np.hstack((frame_1, frame_2))

    if cv2.waitKey(33) & 0xFF == ord('q'):
      break

    cv2.imshow('res', res)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
