import os
import cv2
import numpy as np
from datetime import datetime

ROOT_PATH = './records/'
REC = False

def main():
  global REC
  '''
  The left/right is determined by facing the target
  '''
  cam_1 = cv2.VideoCapture(0) #left
  cam_2 = cv2.VideoCapture(2) #right

  while True:
    _, frame_1 = cam_1.read()
    _, frame_2 = cam_2.read()

    frame_1 = cv2.flip(frame_1, 0)
    frame_2 = cv2.flip(frame_2, 0)

    frame_1 = cv2.rotate(frame_1, cv2.ROTATE_90_CLOCKWISE)
    frame_2 = cv2.rotate(frame_2, cv2.ROTATE_90_COUNTERCLOCKWISE)

    res = np.hstack((frame_1, frame_2))
        #(np.rot90(frame_1,k=-1), np.rot90(frame_2,k=1)))
    res_copy = res.copy()

    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
      break
    if key == ord('r'):
      REC = not REC

    if REC:
      time_stamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S.%f')[:-3]
      info_str = f'REC:{time_stamp}'
      cv2.rectangle(res_copy, (0,0), (250,20), (0,0,0), -1)
      cv2.circle(res_copy, (10,10), 5, (0,0,255), -1)
      cv2.putText(res_copy, info_str, (20,15), 1, 1, (0,255,255), 1)
      res_filename = os.path.join(ROOT_PATH, time_stamp+'.jpeg')
      cv2.imwrite(res_filename, res)

    cv2.imshow('res', res_copy)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
