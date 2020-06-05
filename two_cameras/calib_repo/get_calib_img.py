import os
import cv2
import numpy as np
from datetime import datetime

ROOT_PATH = './frames/'

def main():
  cam = cv2.VideoCapture(0)

  while True:
    _, frame = cam.read()

    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
      break
    if key == ord('r'):
      time_stamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')[:-3]
      frame_filename = os.path.join(ROOT_PATH, time_stamp+'.jpeg')
      cv2.imwrite(frame_filename, frame)
      print('{} saved...'.format(frame_filename))

    cv2.imshow('frame', frame)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
