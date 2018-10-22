import cv2
import sys
import argparse
import json
import csv
import os
import math
import time
#from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader

RADIUS = 10

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
        dist = RADIUS
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.points:
                dist = math.sqrt( (x - self.points[-1][0])**2 + (y - self.points[-1][1])**2 )
            if dist < RADIUS:
                print('Deleted {}'.format(self.points[-1]))
                self.points.pop()
            else:
                self.points.append((x,y))
                print('Clicked on ({0}, {1})'.format(x,y))
            if coord_pts.points:
                frame_copy = frame.copy()
                for pt in coord_pts.points:
                    cv2.circle(frame_copy, pt, RADIUS, (0,0,255), 2)
                    cv2.circle(frame_copy, pt, RADIUS, (0,255,255), -1)
                cv2.imshow("Projectiles", frame_copy)

#instantiate class
coord_pts = CoordinateStore()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', dest='vid_source', type=str,
                        help='Video file.')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.vid_source)
    #cap = FFMPEG_VideoReader(args.vid_source)
    #cap.initialize()

    if not cap.isOpened():
        print('Could not open camera or video')
        sys.exit()

    ok, frame = cap.read()
    if not ok:
        print('Could not read camera frames or video file')
        sys.exit()

    cv2.namedWindow("Projectiles", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Projectiles', coord_pts.select_point)

    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #total_frame = int(cap.fps * cap.duration)
    frame_num = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ok, frame = cap.read()
        if not ok: break
        #frame = cap.get_frame((frame_num+1) / cap.fps)

        frame_info = str(frame_num) + '/' +str(total_frame)
        cv2.putText(frame, frame_info, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        cv2.imshow("Projectiles", frame)

        k = cv2.waitKey(0) & 0xff
        if k == ord('s'):
            if coord_pts:
                filename = os.path.splitext(os.path.basename(args.vid_source))[0] + time.strftime("_%Y%m%d-%H%M%S")
                #coord_pts.saveas_json(coord_pts.points,  filename + '.json')
                coord_pts.saveas_csv(coord_pts.points,  filename + '.csv')
            else:
                print('Coordinate list is empty...')
        elif k == ord('b'):
            frame_num -= 1
        elif k == ord('f'):
            frame_num += 10
        elif k == ord('x'):
            frame_num = 0
            coord_pts.points = []
            print('Back to first frame and the coordinate list has been deleted.')
        elif k == ord('h'):
            help_str = ("[help message]\ns: save the points\n"
                    "b: step one frame back\n"
                    "f: step 10 frames forward\n"
                    "x: back to the first frame and clear coord points\n"
                    "Esc: quit\n"
                    "Any other key to step frames forward\n")
            print(help_str)
        elif k == 27:
            break
        else:
            frame_num += 1


    cap.release()
    cv2.destroyAllWindows()
