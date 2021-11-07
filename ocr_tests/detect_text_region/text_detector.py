import cv2
import numpy as np
from PIL import Image
from pathlib import Path

input_imgs = '../test_img/poj_text/'


def main():
    cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    for img_f in Path(input_imgs).glob('*.png'):
        img = cv2.imread(str(img_f), cv2.IMREAD_UNCHANGED)
        img = cv2.bitwise_not(img)
        #img = cv2.Sobel(img,cv2.CV_8U,0,1,ksize=5)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        mask = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,3))
        dilate = cv2.dilate(mask, kernel, iterations=2)

        cnts, _ = cv2.findContours(
            dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ar = w/float(h)
            area = w*h
            # filter out small and "short" regions
            if area < 2000 or ar < 2:
                cv2.drawContours(dilate, [c], -1, 0, -1)
        res = 255 - cv2.bitwise_and(dilate, img)

        cv2.imshow('res', np.hstack((res, img, dilate)))
        if cv2.waitKey(0) & 0xff == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__=='__main__':
    main()
