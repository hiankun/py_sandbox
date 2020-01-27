import cv2
import numpy as np

maxScaleUp = 100
scaleFactor = 1
scaleType = 0
maxType = 1

windowName = 'Chroma Keying'
trackbarValue = 'Scale'
trackbarType = 'Tolerance'

# load an image
in_vid = './vids/greenscreen-demo.mp4'

class Settings:
  pts = []
  patch = None
  frame = None


def get_mask(tol):
  img = Settings.patch
  upper = np.array([np.amax(img[:,:,i]) for i in range(3)], dtype=np.uint8)
  lower = np.array([np.amin(img[:,:,i]) for i in range(3)], dtype=np.uint8)
  #print(Settings.frame.shape, type(lower), type(upper))
  mask = cv2.inRange(Settings.frame, lower, upper)
  cv2.imshow('mask',mask)

def colorPatchSelector(action, x, y, flags, userdata):
  if action==cv2.EVENT_LBUTTONDOWN:
    Settings.pts.append([x,y])
  if action==cv2.EVENT_LBUTTONUP:
    Settings.pts.append([x,y])
    [xmin, ymin], [xmax, ymax] = Settings.pts
    Settings.patch = Settings.frame[ymin:ymax,xmin:xmax].copy()
    cv2.imshow('patch', Settings.patch)
  if action==cv2.EVENT_RBUTTONDOWN: #clear
    Settings.pts.clear()
    cv2.destroyWindow('patch')


def tolerance(*args):
  tol = args[0]
  get_mask(tol)

def main():
  cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
  cv2.setMouseCallback(windowName, colorPatchSelector)
  cv2.createTrackbar(trackbarType, windowName, 0, 255, tolerance)
  
  cap = cv2.VideoCapture(in_vid)
  while True:
    _, Settings.frame = cap.read()
    Settings.frame = cv2.resize(Settings.frame, None, fx=0.25, fy=0.25)
    #Settings.frame = cv2.cvtColor(Settings.frame, cv2.COLOR_BGR2HSV)
    cv2.imshow(windowName, Settings.frame)

    if cv2.waitKey(0) & 0xFF == ord('q'):
      break
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()

# Callback functions
#def scaleImage(*args):
#    global scaleFactor
#    global scaleType
#
#    if scaleType == 0:
#      scaleFactor = 1 + args[0]/100.0
#    else:
#      scaleFactor = 1 - args[0]/100.0
#      
#    if scaleFactor == 0:
#        scaleFactor = 1
#    scaledImage = cv2.resize(im, None, fx=scaleFactor,\
#            fy = scaleFactor, interpolation = cv2.INTER_LINEAR)
#    cv2.imshow(windowName, scaledImage)
#
#def scaleTypeImage(*args):
#    global scaleFactor
#    global scaleType
#
#    scaleType = args[0]
