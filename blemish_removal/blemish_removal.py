import cv2
import numpy as np

# Lists to store the points
pts=[]
source = cv2.imread("./pics/blemish.png", cv2.IMREAD_COLOR)
saved_roi = './face.jpg'

class Settings:
  h,w,c = source.shape
  crop_zone = None
  click_pos = [0, 0]
  orig_shift = [0, 0]
  radius = 15
  block_size = 2*radius


def tile_sub_blocks(sub_blocks ,bsize):
  ''' Debug function
      Show complete sub blocks 
  '''
  padding = 1
  sub_blk = sub_blocks.copy()
  for i in range(9):
    bg = np.zeros((bsize+2*padding,bsize+2*padding,3), 
      dtype=sub_blk[i].dtype)
    try:
      bg[padding:bsize+padding,padding:bsize+padding] = sub_blk[i]
    except:
      pass
    sub_blk[i] = bg

  blocks_tile = np.vstack((
    np.hstack((sub_blk[0],sub_blk[1],sub_blk[2])),
    np.hstack((sub_blk[3],sub_blk[4],sub_blk[5])),
    np.hstack((sub_blk[6],sub_blk[7],sub_blk[8])),
    ))
  cv2.imshow('debug: tile sub blocks', blocks_tile)


def get_freq():
  pass


def get_gradients(blocks, bsize):
  for i, blk in enumerate(blocks):
    if blk.shape == (bsize, bsize, 3):
      blk = cv2.cvtColor(blk, cv2.COLOR_BGR2GRAY)
      gx = np.mean(cv2.Sobel(blk,cv2.CV_32F,1,0,ksize=3))
      gy = np.mean(cv2.Sobel(blk,cv2.CV_32F,0,1,ksize=3))
      gxy = np.sqrt(gx*gx+gy*gy)
      print(i, gxy)
    else:
      print(i, 'incomplete block with shape of {}'.format(blk.shape))


def get_subzones():
  bsize = Settings.block_size
  # This code clip can only handle all complete blocks
  #sub_blocks = [
  #  Settings.crop_zone[i*bsize:(i+1)*bsize,j*bsize:(j+1)*bsize]
  #  for i in range(3)
  #  for j in range(3)]

  shift = Settings.orig_shift
  idx = np.array([[shift[1]+i*bsize,shift[1]+(i+1)*bsize,
                   shift[0]+j*bsize,shift[0]+(j+1)*bsize]
                   for i in range(3) for j in range(3)])
  idx[idx <= 0] = 0 #set negative idx to zero
  sub_blocks = [Settings.crop_zone[idx[b][0]:idx[b][1], idx[b][2]:idx[b][3]]
                for b in range(9)]

  tile_sub_blocks(sub_blocks, bsize)
  get_gradients(sub_blocks, bsize)


def get_roi(action, x, y, flags, userdata):
  radius3 = Settings.radius*3
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.click_pos = [x, y]
    #xmin = x - radius3 if x >= radius3 else 0
    #ymin = y - radius3 if y >= radius3 else 0
    xmin = x - radius3
    if xmin < 0:
      Settings.orig_shift[0] = xmin
      xmin = 0
    else:
      Settings.orig_shift[0] = 0
    ymin = y - radius3
    if ymin < 0:
      Settings.orig_shift[1] = ymin
      ymin = 0
    else:
      Settings.orig_shift[1] = 0

    xmax = x + radius3
    if xmax > Settings.w: 
      xmax = Settings.w
    ymax = y + radius3
    if ymax > Settings.h: 
      ymax = Settings.h

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
