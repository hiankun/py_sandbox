#https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API
import cv2
import time
import numpy as np

src = 1 #'/home/thk/Downloads/soccer-ball.mp4'
MODEL = './models/ssd_mobilenet_v2_coco_2018_03_29.pb'
CONFIG = './models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
LABEL_FILE = './models/coco_labels.txt'
#MODEL = './models/ssd_mobilenet_v2_twice.pb'
#CONFIG = './models/ssd_mobilenet_v2_twice.pbtxt'
#LABEL_FILE = './models/twice_labels.txt'
NET = cv2.dnn.readNetFromTensorflow(MODEL, CONFIG)
try:
  with open(LABEL_FILE) as f:
    LABELS = [line.rstrip() for line in f]
except:
  LABELS = None


def draw_results(img, objects, infer_time=None):
  height, width, _ = img.shape
  for obj in objects[0,0,:,:]:
    score = float(obj[2])
    if score > 0.6:
      xmin = int(obj[3] * width)
      ymin = int(obj[4] * height)
      xmax = int(obj[5] * width)
      ymax = int(obj[6] * height)
      cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,255,255), 1)
      if LABELS:
        label = LABELS[int(obj[1])]
        text_w = 110
      else:
        label = int(obj[1])
        text_w = 60
      cv2.rectangle(img, (xmin,ymin), (xmin+text_w,ymin+20), (0,255,255), -1)
      det_info = '{}:{:.2f}'.format(label, score)
      cv2.putText(img, det_info, (xmin+5,ymin+15), 1, 1.0, (0,0,0), 1)

  if infer_time:
    #cv2.rectangle(img, (0,0), (100,20), (0,0,0), -1)
    infer_time_info = '{:.2f} FPS'.format(1.0/infer_time)
    cv2.putText(img, infer_time_info, (10,15), 1, 1.0, (255,255,255), 1)

  return img


def main():
  cap = cv2.VideoCapture(src)

  while True:
    _, frame = cap.read()

    # The following code was used to test the CONTIGUOUS
    #print(frame.dtype, frame.flags)
    #frame = np.array(frame[:,:,::-1], dtype=np.uint8)
    #frame = frame[:,:,::-1]
    #print(frame.dtype, frame.flags)
  
    infer_start = time.perf_counter()    
    NET.setInput(cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False))
    objects = NET.forward()
    infer_time = time.perf_counter() - infer_start

    res = draw_results(frame, objects, infer_time)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break


if __name__=='__main__':
  main()
