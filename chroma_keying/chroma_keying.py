'''
Use mouse to choose the bg reference zone.
Then use tolerance to fine tune.
'''
import cv2
import numpy as np


windowName = 'Chroma Keying'
trackbarValue = 'Scale'
trackbarType = 'Tolerance'
trackbarMode = 'Mode(0): -tolerance\nMode(1): +tolerance'

# load an image or video as the background
in_vid = './vids/greenscreen-demo-half.mp4'
bg_vid = './vids/chaplin_a_thief.mp4'
bg_file = './pics/twice_bg.jpg'

class Settings:
  pts = []
  patch = None
  fg = None
  bg = None
  upper = np.array([255,255,255], dtype=np.uint8)
  lower = np.array([0,0,0], dtype=np.uint8)
  mode = 1


def apply_mask(tol=None):
  # get lower and upper boundaries
  if Settings.patch is not None:
    img = Settings.patch
    # Use np.int16 to handle later calculations which exceed [0,255]
    Settings.upper = np.array([np.amax(img[:,:,i]) for i in range(3)], dtype=np.int16)
    Settings.lower = np.array([np.amin(img[:,:,i]) for i in range(3)], dtype=np.int16)

  if tol is not None:
    Settings.upper += tol
    Settings.upper[Settings.upper>255]=255
    Settings.lower -= tol
    Settings.lower[Settings.lower<0]=0

  #print(Settings.lower, Settings.upper)

  # get mask
  bg = Settings.bg
  fg = Settings.fg
  bg_mask = cv2.inRange(fg, Settings.lower, Settings.upper).astype('uint8')
  # refine bg_mask
  bg_mask = cv2.morphologyEx(bg_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=7)
  fg_mask = cv2.bitwise_not(bg_mask)

  # apply mask
  masked_bg = cv2.bitwise_and(bg, bg, mask=bg_mask)
  masked_fg = cv2.bitwise_and(fg, fg, mask=fg_mask)
  res = cv2.addWeighted(masked_fg,1,masked_bg,1,0)

  return res


def colorPatchSelector(action, x, y, flags, userdata):
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.pts.append([x,y])
  if action==cv2.EVENT_LBUTTONUP:
    Settings.pts.append([x,y])
    [xmin, ymin], [xmax, ymax] = Settings.pts
    Settings.patch = Settings.fg[ymin:ymax,xmin:xmax].copy()
    cv2.imshow('patch', Settings.patch)
    apply_mask()
    Settings.patch = None #reset patch to keep old lower/upper boundaries
  #if action==cv2.EVENT_RBUTTONDOWN: #clear
    Settings.pts.clear()
    cv2.waitKey(5000)
    cv2.destroyWindow('patch')


def tolerance(*args):
  if Settings.mode == 1:
    tol = args[0]
  else:
    tol = -args[0]

  apply_mask(tol)


def tolerance_mode(*args):
  Settings.mode = args[0]


def main():
  cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
  cv2.setMouseCallback(windowName, colorPatchSelector)
  cv2.createTrackbar(trackbarType, windowName, 0, 255, tolerance)
  cv2.createTrackbar(trackbarMode, windowName, 1, 1, tolerance_mode)
  
  fg_cap = cv2.VideoCapture(in_vid)
  bg_cap = cv2.VideoCapture(bg_vid)
  while True:
    _, Settings.fg = fg_cap.read()
    #Settings.bg = cv2.imread(bg_file, cv2.IMREAD_COLOR)
    _, Settings.bg = bg_cap.read()

    #Settings.fg = cv2.resize(Settings.fg, None, fx=0.25, fy=0.25)
    #Settings.fg = cv2.cvtColor(Settings.fg, cv2.COLOR_BGR2HSV)
    fg_h, fg_w, _ = Settings.fg.shape
    Settings.bg = cv2.resize(Settings.bg, (fg_w, fg_h))
    cv2.imshow(windowName, Settings.fg) 
    res = apply_mask()
    cv2.imshow('res', res)

    if cv2.waitKey(0) & 0xFF == ord('q'):
      break
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()

