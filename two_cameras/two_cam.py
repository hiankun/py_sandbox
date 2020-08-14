import cv2
import numpy as np
import time
from pathlib import Path

CAM_1 = 1
CAM_2 = 2
DEBUG = False #enable only camera 1

WIDTH, HEIGHT = 1024, 576
#WIDTH, HEIGHT = 1920, 1080 

def get_time_stamp(short_format=False):
    if short_format:
        return time.strftime('%Y%m%d-%H%M%S',time.localtime())
    else:
        return time.strftime('%Y%m%d-%H%M%S',time.localtime()) \
                    + '-' + str(time.time()).split('.')[-1][:3]

def main():
    REC_path = './rec_' + get_time_stamp(short_format=True)
    p = Path(REC_path)
    p.mkdir(parents=True, exist_ok=True)

    REC = False

    '''
    The left/right is determined by facing the target
    '''
    cam_1 = cv2.VideoCapture(CAM_1) #left-half screen
    cam_1.set(3, WIDTH)
    cam_1.set(4, HEIGHT)

    if not DEBUG:
        cam_2 = cv2.VideoCapture(CAM_2) #right-half screen
        cam_2.set(3, WIDTH)
        cam_2.set(4, HEIGHT)

    while True:
        _, frame_1 = cam_1.read()
        #frame_1 = cv2.flip(frame_1, 0)
        frame_1_rot = cv2.rotate(frame_1, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if not DEBUG:
            _, frame_2 = cam_2.read()
            #frame_2 = cv2.flip(frame_2, 0)
            frame_2_rot = cv2.rotate(frame_2, cv2.ROTATE_90_CLOCKWISE)

            res = np.hstack((frame_1_rot, frame_2_rot))
                    #(np.rot90(frame_1,k=-1), np.rot90(frame_2,k=1)))
        else:
            res = frame_1
        res_copy = res.copy()

        key = cv2.waitKey(66) & 0xFF 
        if key == ord('q'):
            break
        if key == ord('r'):
            REC = not REC

        if REC and not DEBUG:
            time_stamp = get_time_stamp()
            res_filename = Path(REC_path)/(time_stamp+'.jpeg')
            res_filename1 = Path(REC_path)/(time_stamp+'_cam1.jpeg')
            res_filename2 = Path(REC_path)/(time_stamp+'_cam2.jpeg')

            info_str = f'REC:{time_stamp}'
            cv2.rectangle(res_copy, (0,0), (250,20), (0,0,0), -1)
            cv2.circle(res_copy, (10,10), 5, (0,0,255), -1)
            cv2.putText(res_copy, info_str, (20,15), 1, 1, (0,255,255), 1)

            #cv2.imwrite(str(res_filename), res)
            cv2.imwrite(str(res_filename1), frame_1)
            cv2.imwrite(str(res_filename2), frame_2)

        cv2.imshow('res', res_copy)
    
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()
