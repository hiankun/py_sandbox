import numpy as np
import cv2

def get_bilateral(img, 
  sigmaColor = 60,
  sigmaSpace = 5 ## large value will slow down the program dramatically
  ):
  #filtered_color = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
  filtered_color = cv2.bilateralFilter(img, -1, sigmaColor, sigmaSpace)
  #filtered_color = cv2.resize(filtered_color, (0,0), fx=2, fy=2)
  return filtered_color


def get_sketch_lines(
  img, blur_ksize=(3,3), 
  laplacian_ksize = 5,
  threshold = (120,255)):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  blurred = cv2.GaussianBlur(gray, ksize=blur_ksize, sigmaX=0)
  laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize=laplacian_ksize, scale=1, delta=0)
  _, edges = cv2.threshold(laplacian, threshold[0], threshold[1], cv2.THRESH_BINARY_INV)

  return cv2.merge((edges, edges, edges))


def main():
  img = cv2.imread('./pics/chhaukau.jpg', cv2.IMREAD_COLOR)
  sketch = get_sketch_lines(img)
  cv2.imshow('sketch', sketch)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


if __name__=='__main__':
  main()
