import cv2
import numpy as np


windowName = 'Tracking'
trackbarType = 'Tolerance'
trackbarMode = 'Mode(0): -tolerance\nMode(1): +tolerance'

class Settings:
  pts = []
  patch = None
  frame_0 = None
  frame_1 = None
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
  frame_0 = Settings.frame_0
  frame_1 = Settings.frame_1
  obj_mask = cv2.inRange(frame_0, Settings.lower, Settings.upper).astype('uint8')
  # refine bg_mask
  obj_mask = cv2.morphologyEx(obj_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=5)
  #fg_mask = cv2.bitwise_not(bg_mask)

  # apply mask
  #masked_bg = cv2.bitwise_and(bg, bg, mask=bg_mask)
  #masked_fg = cv2.bitwise_and(fg, fg, mask=fg_mask)
  #res = cv2.addWeighted(masked_fg,1,masked_bg,1,0)

  #return res
  return obj_mask


def colorPatchSelector(action, x, y, flags, userdata):
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.pts.append([x,y])
  if action==cv2.EVENT_LBUTTONUP:
    Settings.pts.append([x,y])
    [xmin, ymin], [xmax, ymax] = Settings.pts
    Settings.patch = Settings.frame_0[ymin:ymax,xmin:xmax].copy()
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
  
  cap_0 = cv2.VideoCapture(0)
  cap_1 = cv2.VideoCapture(1)
  while True:
    _, Settings.frame_0 = cap_0.read()
    #Settings.bg = cv2.imread(bg_file, cv2.IMREAD_COLOR)
    _, Settings.frame_1 = cap_1.read()

    #Settings.fg = cv2.resize(Settings.fg, None, fx=0.25, fy=0.25)
    #Settings.fg = cv2.cvtColor(Settings.fg, cv2.COLOR_BGR2HSV)
    cv2.imshow(windowName, np.hstack((Settings.frame_0, Settings.frame_1)))
    res = apply_mask()
    cv2.imshow('res', res)

    if cv2.waitKey(33) & 0xFF == ord('q'):
      break
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()

