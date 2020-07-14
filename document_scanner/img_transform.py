# https://www.learnopencv.com/homography-examples-using-opencv-python-c/
import cv2
import numpy as np


class Common:
    x = 0
    y = 0
    pts = []


def do_warp(img_src):
    pts_src = np.array([[141, 131], [480, 159], [493, 630],[64, 601]])
    pts_dst = np.array([[141, 131], [480, 159], [493, 630],[64, 601]])
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
    
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        Common.x, Common.y = x,y
        pts.append([x,y])


def main():
    cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('res', get_xy)
    img = cv2.imread('scanned-form.jpg')

    while True:
        cv2.imshow('res', img)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    do_warp()

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
