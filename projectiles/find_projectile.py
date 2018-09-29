import cv2
import sys
import argparse
import json
import csv
import os

class CoordinateStore:
    def __init__(self):
        self.points = []

    def saveas_json(self, coord, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(coord, outfile)
            print('coord saved as', file_name)

    def saveas_csv(self, coord, file_name):
        with open(file_name, 'w') as outfile:
            csv.writer(outfile).writerows(coord)
            print('coord saved as', file_name)

    def select_point(self,event,x,y,flags,param):
        #if event == cv2.EVENT_LBUTTONDBLCLK:
        if event == cv2.EVENT_LBUTTONDOWN:
            #cv2.circle(frame,(x,y),10,(0,0,200),-1)
            self.points.append((x,y))

#instantiate class
coord_pts = CoordinateStore()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', dest='vid_source', type=str,
                        help='Video file.')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.vid_source)

    if not cap.isOpened():
        print('Could not open camera or video')
        sys.exit()

    ok, frame = cap.read()
    if not ok:
        print('Could not read camera frames or video file')
        sys.exit()

    cv2.namedWindow("Projectiles", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Projectiles', coord_pts.select_point)

    while True:
        ok, frame = cap.read()
        if not ok: break

        if coord_pts.points:
            for pt in coord_pts.points:
                cv2.circle(frame, pt, 10, (0,150,255), -1)
        cv2.imshow("Projectiles", frame)

        k = cv2.waitKey() & 0xff
        if k == ord('s'):
            filename = os.path.splitext(os.path.basename(args.vid_source))[0]
            #coord_pts.saveas_json(coord_pts.points,  filename + '.json')
            coord_pts.saveas_csv(coord_pts.points,  filename + '.csv')
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
