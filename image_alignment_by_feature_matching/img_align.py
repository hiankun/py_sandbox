# This code is based on the course of OpenCV: https://courses.opencv.org/
# photo source: http://www.loc.gov/pictures/collection/prok/
import cv2
import numpy as np

MAX_FEATURES = 20000 # should be big enough
GOOD_MATCH_PERCENT = 0.02 # should be small
photos = [
        'photos/01522v.jpg',
        'photos/01598v.jpg',
        'photos/emir.jpg',
        ]
  
def split_bgr(img):
  _h, width = img.shape
  height = int(_h/3)
  
  img_color = np.zeros((height,width,3), dtype=np.uint8)
  for i in range(3):
    img_color[:,:,i] = img[i*height : (i+1)*height, :]
  
  blue = img_color[:,:,0]
  green = img_color[:,:,1]
  red = img_color[:,:,2]

  return blue, green, red
  

def match_features(descriptors1, descriptors2):
  # Matcher
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)
  # Sort matches by score
  matches.sort(key=lambda x: x.distance, reverse=False)
  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]

  return matches
  

def get_homography(kp1, kp2, matches):
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
  
  for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    points2[i, :] = kp2[match.trainIdx].pt
  
  # Find homography
  h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
  #print(h)
  return h
  

def main():
  '''
  Step 1: Preprocessing
  '''
  img = cv2.imread(photos[2], cv2.IMREAD_GRAYSCALE)
  blue, green, red = split_bgr(img)
  
  '''
  Step 2: Detect Features
  '''
  orb = cv2.ORB_create(MAX_FEATURES)
  kp_blue, des_blue = orb.detectAndCompute(blue, None)
  kp_green, des_green = orb.detectAndCompute(green, None)
  kp_red, des_red = orb.detectAndCompute(red, None)
  
  '''
  Step 3: Match Features
  '''
  matchesBlueGreen = match_features(des_blue, des_green)
  matchesRedGreen = match_features(des_red, des_green)
  imMatchesBlueGreen = cv2.drawMatches(blue, kp_blue, green, kp_green, matchesBlueGreen, None)
  imMatchesRedGreen = cv2.drawMatches(red, kp_red, green, kp_green, matchesRedGreen, None)
  cv2.imshow('matches', np.vstack((imMatchesBlueGreen, imMatchesRedGreen)))
  
  '''
  Step 4: Calculate Homography 
  '''
  hBlueGreen = get_homography(kp_blue, kp_green, matchesBlueGreen)
  hRedGreen = get_homography(kp_red, kp_green, matchesRedGreen)
  
  height, width = green.shape
  blueWarped = cv2.warpPerspective(blue, hBlueGreen, (width, height))
  redWarped = cv2.warpPerspective(red, hRedGreen, (width, height))
  cv2.imshow('warped', np.hstack((blueWarped, redWarped)))

  '''
  Final results
  '''
  original = cv2.merge((blue,green,red))
  aligned = cv2.merge((blueWarped,green,redWarped))
  cv2.imshow('original vs. aligned', np.hstack((original, aligned)))

  cv2.waitKey()


if __name__=='__main__':
  main()
