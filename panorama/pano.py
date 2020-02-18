import cv2
import numpy as np
import os
from glob import glob

#imagefiles = sorted(glob('./inputs/*.jpg'))
imagefiles = glob('./inputs/*.jpg')

images = []
for filename in imagefiles:
  img = cv2.imread(filename)
  images.append(img)

stitcher = cv2.Stitcher.create()
_, res = stitcher.stitch(images)

cv2.imshow('Panorama', res[100:-100,50:-50])
cv2.waitKey()
