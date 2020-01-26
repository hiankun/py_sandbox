import cv2
import numpy as np

# Lists to store the points
pts=[]
source = cv2.imread("/home/thk/Desktop/blemish.png", cv2.IMREAD_COLOR)
saved_roi = './face.jpg'

class Settings:
  crop_zone = None
  radius = 15
  block_size = 2*radius


def tile_sub_blocks(sub_blocks ,bsize):
  '''debug'''
  padding = 1
  for i in range(9):
    bg = np.zeros((bsize+2*padding,bsize+2*padding,3), 
      dtype=sub_blocks[i].dtype)
    bg[padding:bsize+padding,padding:bsize+padding] = sub_blocks[i]
    sub_blocks[i] = bg

  blocks_tile = np.vstack((
    np.hstack((sub_blocks[0],sub_blocks[1],sub_blocks[2])),
    np.hstack((sub_blocks[3],sub_blocks[4],sub_blocks[5])),
    np.hstack((sub_blocks[6],sub_blocks[7],sub_blocks[8])),
    ))
  cv2.imshow('debug: tile sub blocks', blocks_tile)


def get_subzones():
  bsize = Settings.block_size
  sub_blocks = [
    Settings.crop_zone[i*bsize:(i+1)*bsize,j*bsize:(j+1)*bsize]
    for i in range(3)
    for j in range(3)]

  #tile_sub_blocks(sub_blocks, bsize)


def get_roi(action, x, y, flags, userdata):

  if action==cv2.EVENT_LBUTTONDOWN:
    radius = Settings.radius
    xmin = x - radius*3
    ymin = y - radius*3
    xmax = x + radius*3
    ymax = y + radius*3

    Settings.crop_zone = source[ymin:ymax,xmin:xmax].copy()
    get_subzones()

  elif action==cv2.EVENT_RBUTTONDOWN:
    Settings.crop_zone = None # reset
    cv2.destroyWindow("ROI")

    #xmin, ymin = pts[0]
    #xmax, ymax = pts[1]

    #crop_zone = source[ymin:ymax,xmin:xmax].copy()
    #cv2.imwrite(saved_roi, crop_zone)
    #print('Selected ROI has been saved to {}...'.format(saved_roi))

    #cv2.rectangle(source, (xmin,ymin), (xmax,ymax), (0,255,0), 2, cv2.LINE_AA)
    #pts.clear()

    #cv2.imshow("Copy ROI",source)
  if Settings.crop_zone is not None:
    cv2.imshow("ROI", Settings.crop_zone)
  

def main():
  cv2.namedWindow("Source Image")

  # highgui function called when mouse events occur
  cv2.setMouseCallback("Source Image", get_roi)

  k = 0
  # loop until escape character is pressed
  while k != ord('q') :
    
    cv2.imshow("Source Image", source)
    #cv2.putText(source,'''Click top-left corner and drag to bottom-right...''' ,
    #            (10,30), cv2.FONT_HERSHEY_SIMPLEX,
    #            0.6,(255,255,255), 2 );

    k = cv2.waitKey(1) & 0xFF

  cv2.destroyAllWindows()


if __name__ == "__main__":
  main()
