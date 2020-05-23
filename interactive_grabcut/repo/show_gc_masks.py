# Check the mask produced during the GC process
import numpy as np
import cv2

mask_file = 'mask04.jpg'
mask = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)
print(mask.shape, mask.size)
mask_0 = np.count_nonzero(mask==0)
mask_1 = np.count_nonzero(mask==1)
mask_2 = np.count_nonzero(mask==2)
mask_3 = np.count_nonzero(mask==3)
mask_4 = np.count_nonzero(mask==4)

print('mask == 0: ', mask_0) # cv2.GC_BGD
print('mask == 1: ', mask_1) # cv2.GC_FGD
print('mask == 2: ', mask_2) # cv2.GC_PR_BGD
print('mask == 3: ', mask_3) # cv2.GC_PR_FGD
print('mask == 4: ', mask_4) # who're you? 
print('total: ', mask_0+mask_1+mask_2+mask_3+mask_4)

bgr_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
bgr_mask[mask == 0] = (0,0,255)
bgr_mask[mask == 1] = (0,255,0)
bgr_mask[mask == 2] = (0,0,125)
bgr_mask[mask == 3] = (255,0,0)

cv2.imshow('mask', bgr_mask)
cv2.waitKey(0)
