from PIL import Image
from skimage.morphology import skeletonize
from skimage.util import invert
import numpy as np
import matplotlib.pyplot as plt

image = invert(
    np.asarray(Image.open('../test_img/KHKP-0590_09.png').convert('L')))
binary_img = np.where(image>125, 1, 0)
skeleton = skeletonize(binary_img)

plt.imshow(skeleton)
plt.show()

