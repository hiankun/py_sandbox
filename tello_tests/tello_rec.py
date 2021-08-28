# src: https://github.com/damiafuentes/DJITelloPy/blob/master/examples/record-video.py

import sys, time, cv2
from datetime import datetime
from threading import Thread
from djitellopy import Tello


def videoRecorder(frame_read): 
    height, width, _ = frame_read.frame.shape
    time_stamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")
    vid_fname = f'tello_rec_{time_stamp}.avi'
    video = cv2.VideoWriter(vid_fname, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while True:
        frame = frame_read.frame
        time_now = datetime.now().strftime("%Y%m%d-%H:%M:%S")
        cv2.putText(frame, time_now, (50,50), 1, 2, (0,255,255), 1)
        cv2.imshow('tello', frame)
        video.write(frame)
        #time.sleep(1/30) # we have waitKey(), don't need sleep()

        if cv2.waitKey(33) == ord('q'):
            break

    cv2.destroyAllWindows()
    video.release()


def main():
    tello = Tello()
    tello.connect()
    
    battery = tello.get_battery()
    print(f'>>>>>>>>>>>> Battery: {battery}%')
    if int(battery) < 30:
        print(f'<<<<<<<<<<<< Battery LOW: {battery}%')
        sys.exit(1)
    
    tello.streamon()
    frame_read = tello.get_frame_read()
    
    recorder = Thread(target=videoRecorder, args=(frame_read,))
    recorder.start()
    
    tello.takeoff()
    tello.rotate_counter_clockwise(360)
    #tello.move_down(25)
    #tello.rotate_clockwise(360)
    tello.land()
    
    recorder.join()


if __name__=='__main__':
    main()
