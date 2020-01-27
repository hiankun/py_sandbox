import cv2
import numpy as np


DEBUG = False # set to True to show more debug figures

class Settings:
  source = cv2.imread("./pics/blemish.png", cv2.IMREAD_COLOR)
  h,w,c = source.shape
  crop_zone = None
  click_pos = (0, 0)
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
  ''' TODO
  Maybe use frequency methods as a LPF to make selected patch smoother...
  '''
  pass


def get_gradients(blocks, bsize):
  '''
  Calculate Gxy of (blurred) blocks)
  '''
  gradients = {}
  for i, blk in enumerate(blocks):
    if blk.shape == (bsize, bsize, 3):
      blk = cv2.cvtColor(blk, cv2.COLOR_BGR2GRAY)
      gx = np.mean(cv2.Sobel(blk,cv2.CV_32F,1,0,ksize=3))
      gy = np.mean(cv2.Sobel(blk,cv2.CV_32F,0,1,ksize=3))
      gxy = np.sqrt(gx*gx+gy*gy)
      gradients[i] = gxy
    else:
      print(i, 'incomplete block with shape of {}'.format(blk.shape))
  return gradients


def apply_patch(sub_blocks, gradients):
  '''
  Sort the gradients of sub blocks,
  and then choose the one with the least Gxy value as the patch.
  Finally, clone the patch to the source image.
  '''
  sorted_gradients = sorted(gradients, key=gradients.get)
  patch_idx = sorted_gradients[0] if sorted_gradients[0] != 4 else sorted_gradients[1]
  patch = sub_blocks[patch_idx]
  target = Settings.source #sub_blocks[4]
  center = Settings.click_pos #(Settings.radius, Settings.radius)
  if DEBUG:
    cv2.imshow('patch', patch)
  patch_mask = np.zeros(patch.shape, patch.dtype)
  patch_mask = cv2.circle(patch_mask,(Settings.radius, Settings.radius),
                          Settings.radius, (255,255,255), -1)
  Settings.source = cv2.seamlessClone(patch, target, patch_mask, center, cv2.NORMAL_CLONE)


def get_subzones(blurred_roi):
  '''
  According to the click position, divide the cropped ROI into sub blocks.
  If the whole ROI were within the source image, then there'll be 3x3 tiled blocks.
  The center one should contain the user clicked blemish.
  The `tile_sub_blocks()` shows all complete blocks.
  '''
  bsize = Settings.block_size
  shift = Settings.orig_shift
  idx = np.array([[shift[1]+i*bsize,shift[1]+(i+1)*bsize,
                   shift[0]+j*bsize,shift[0]+(j+1)*bsize]
                   for i in range(3) for j in range(3)])
  idx[idx <= 0] = 0 #set negative idx to zero

  blurred_blocks = [blurred_roi[idx[b][0]:idx[b][1], idx[b][2]:idx[b][3]]
                for b in range(9)]
  sub_blocks = [Settings.crop_zone[idx[b][0]:idx[b][1], idx[b][2]:idx[b][3]]
                for b in range(9)]

  # Use blurred blocks to find the usable patch
  if DEBUG:
    tile_sub_blocks(blurred_blocks, bsize)
  gradients = get_gradients(blurred_blocks, bsize)
  # Apply the original (un-blurred) patch to the source image
  apply_patch(sub_blocks, gradients)


def get_roi(action, x, y, flags, userdata):
  radius3 = Settings.radius*3
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.click_pos = (x, y)

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

    Settings.crop_zone = Settings.source[ymin:ymax,xmin:xmax].copy()
    # Filter out salt-and-pepper noise
    blurred_roi = Settings.crop_zone.copy()
    blurred_roi = cv2.medianBlur(blurred_roi, ksize=3)
    #blurred_roi = cv2.GaussianBlur(blurred_roi, ksize=(3,3), sigmaX=0)
    get_subzones(blurred_roi)

  elif action==cv2.EVENT_RBUTTONDOWN:
    Settings.crop_zone = None # reset
    cv2.destroyWindow("ROI")

  if Settings.crop_zone is not None and DEBUG:
    cv2.imshow("ROI", Settings.crop_zone)
  

def main():
  cv2.namedWindow("Source Image")
  cv2.setMouseCallback("Source Image", get_roi)

  while True:
    cv2.imshow("Source Image", Settings.source)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cv2.destroyAllWindows()


if __name__ == "__main__":
  main()
