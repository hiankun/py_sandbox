import cv2

# Lists to store the points
pts=[]
source = cv2.imread("/home/thk/Desktop/blemish.png",1)
saved_roi = './face.jpg'

def draw_roi(action, x, y, flags, userdata):
  # Action to be taken when left mouse button is pressed
  if action==cv2.EVENT_LBUTTONDOWN:
    pts.append((x,y))

  # Action to be taken when left mouse button is released
  elif action==cv2.EVENT_LBUTTONUP:
    pts.append((x,y))

    xmin, ymin = pts[0]
    xmax, ymax = pts[1]

    crop_img = source[ymin:ymax,xmin:xmax].copy()
    cv2.imwrite(saved_roi, crop_img)
    print('Selected ROI has been saved to {}...'.format(saved_roi))

    cv2.rectangle(source, (xmin,ymin), (xmax,ymax), (0,255,0), 2, cv2.LINE_AA)
    pts.clear()

    cv2.imshow("Copy ROI",source)


def main():
  cv2.namedWindow("Copy ROI")

  # highgui function called when mouse events occur
  cv2.setMouseCallback("Copy ROI", draw_roi)

  k = 0
  # loop until escape character is pressed
  while k!=27 :
    
    cv2.imshow("Copy ROI", source)
    cv2.putText(source,'''Click top-left corner and drag to bottom-right...''' ,
                (10,30), cv2.FONT_HERSHEY_SIMPLEX,
                0.6,(255,255,255), 2 );

    k = cv2.waitKey(20) & 0xFF

  cv2.destroyAllWindows()


if __name__ == "__main__":
  main()
