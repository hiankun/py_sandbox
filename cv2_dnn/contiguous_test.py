'''
https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
https://docs.scipy.org/doc/numpy/reference/generated/numpy.ascontiguousarray.html
https://stackoverflow.com/questions/26998223/what-is-the-difference-between-contiguous-and-non-contiguous-arrays
https://stackoverflow.com/questions/509211/understanding-slice-notation
'''
import cv2
import numpy as np


'''
Read the image and set some variables
'''
img = cv2.imread('./pics/twice.jpg', cv2.IMREAD_COLOR)
h, w, _ = img.shape
center = (int(w/2),int(h/2))
size = 100
top_right = (center[0]+size,center[1]-size)
bottom_left = (center[0]-size,center[1]+size)

'''
Ream logo for overlay test
'''
logo = cv2.imread('./pics/twice_logo.png', cv2.IMREAD_COLOR)
logo = cv2.resize(logo, (size,size))

'''
Try different methods and check the flags
'''
print('img: {}\n{}'.format(img.dtype, img.flags))
img_swap = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img_swap = img[:,:,::-1]
#img_swap = np.array(img[:,:,::-1])
#img_swap = np.ascontiguousarray(img[:,:,::-1])
print('img_swap: {}\n{}'.format(img_swap.dtype, img_swap.flags))

'''
Try cv2 drawing functions
'''
cv2.rectangle(img_swap, top_right, bottom_left, (0,0,255), 2)
cv2.line(img_swap, top_right, bottom_left, (0,255,0), 2)
cv2.circle(img_swap, center, int(h/4), (255,0,0), 2)
cv2.putText(img_swap, 'Twice', bottom_left, 3, 1.5, (0,255,255), 2)

'''
Try overlay
'''
overlay = cv2.addWeighted(img_swap[h-size:h,w-size:w],0.2,logo,0.8,0)
img_swap[h-size:h,w-size:w] = overlay

'''
Show the result
'''
cv2.imshow('img', np.hstack((img, img_swap)))
cv2.waitKey()
