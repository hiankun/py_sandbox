# source: https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
# GOTURN: https://www.learnopencv.com/goturn-deep-learning-based-object-tracking/
import cv2
import sys
import time
 
trackingWindow = 'Tracking'

class Settings:
  bbox = [] #(x,y,w,h)
  tracker_init = False
  tracker_list = [ 'BOOSTING',   'MIL',    'KCF',    'TLD', 
                    'MEDIANFLOW', 'GOTURN', 'MOSSE',  'CSRT']
  tracker_type = ''


def targetSelector(action, x, y, flags, userdata):
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.bbox.extend([x,y])
  if action==cv2.EVENT_LBUTTONUP:
    w = x - Settings.bbox[0]
    h = y - Settings.bbox[1]
    Settings.bbox.extend([w,h])
 

def get_tracker(tracker_idx):
  tracker_type = Settings.tracker_type = Settings.tracker_list[tracker_idx]
 
  if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting_create()
  if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
  if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
  if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD_create()
  if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow_create()
  if tracker_type == 'GOTURN': #need goturn.prototxt
    tracker = cv2.TrackerGOTURN_create()
  if tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE_create()
  if tracker_type == "CSRT":
    tracker = cv2.TrackerCSRT_create()

  return tracker


def main():
 
  cv2.namedWindow(trackingWindow, cv2.WINDOW_AUTOSIZE)
  cv2.setMouseCallback(trackingWindow, targetSelector)

  cap = cv2.VideoCapture(0)
 
  while True:
    _, frame = cap.read()

    # Create a tracker when bbox is ready
    if len(Settings.bbox) == 4:
      tracker = get_tracker(4)
      bbox = tuple(Settings.bbox)
      Settings.tracker_init = tracker.init(frame, bbox)
      Settings.bbox = []
 
    if Settings.tracker_init:
      # Start timer
      timer = cv2.getTickCount()
 
      # Update tracker
      tracker_status, bbox = tracker.update(frame)
 
      # Calculate Frames per second (FPS)
      fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
      # Draw bounding box
      if tracker_status:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,255,255), 1, 1)
      else :
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
 
      cv2.putText(frame, Settings.tracker_type + " Tracker", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,170,50),2);
      cv2.putText(frame, "FPS : " + str(int(fps)), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,170,50), 2);
    cv2.imshow(trackingWindow, frame)
 
    if cv2.waitKey(1) & 0xff == ord('q') : break


if __name__ == '__main__' :
  main()
