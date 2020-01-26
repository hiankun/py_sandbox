import numpy as np
import cv2
import cartoon_filters


def main():
  frame = cv2.imread('./pics/chhaukau.jpg', cv2.IMREAD_COLOR)
  
  colors = cartoon_filters.get_bilateral(frame) 
  edges = cartoon_filters.get_sketch_lines(frame)
  
  res = cv2.bitwise_and(colors, edges)

  cv2.imshow('filtered_color', np.hstack((colors, edges, res)))
  cv2.waitKey(0)
  
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
