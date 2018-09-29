# origin: https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

import cv2
import sys
import argparse

major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=1, help='Device index of the camera.')
    parser.add_argument('-tr', '--tracker', dest='tracker_id', type=int,
                        default=2, help='Tracker ID [0-7]')
    args = parser.parse_args()

    # Trackers
    tracker_types = ['BOOSING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 
            'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[args.tracker_id]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN': #failed to run
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()

    video = cv2.VideoCapture(args.video_source)

    if not video.isOpened():
        print('Could not open video')
        sys.exit()

    ok, frame = video.read()
    if not ok:
        print('Could not read video file')
        sys.exit()

    # initial bounding box
    bbox = cv2.selectROI(frame) #(x,y,w,h)
    ok = tracker.init(frame, bbox)

    while True:
        ok, frame = video.read()
        if not ok:
            break

        timer = cv2.getTickCount()
        ok, bbox = tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # draw bbox
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv2.putText(frame, "Failed to track...",
                     (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display info
        cv2.putText(frame, tracker_type + " Tracker", (100,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        cv2.imshow("Tracking", frame)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

