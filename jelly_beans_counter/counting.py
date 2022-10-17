import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter


BEANS = {
    'dark': 24,
    'yellow': 21,
    'red': 20,
    'green': 17,
}


def img_seg(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    k_size = 11
    blur = cv2.GaussianBlur(img, (k_size, k_size), 0)
    thld = 100
    _, mask = cv2.threshold(blur, thld, 255, cv2.THRESH_BINARY)
    return mask


def get_beans_count(mask):
    contours, _ = cv2.findContours(
        image=mask, 
        mode=cv2.RETR_EXTERNAL, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    cont_areas = []
    for contour in contours:
        cont_areas.append(cv2.contourArea(contour))

    # By observing the mask of the beans, the median was chosen as the 
    # reference area for a single bean to avoid the affect of too 
    # small/large values.
    ref_size = np.median(cont_areas)
    all_size = sum(cont_areas)

    total_est = int(all_size/ref_size)
    total_gt = sum(BEANS.values())
    print(f'Estimated counts: {total_est}, True counts: {total_gt}\n')

    return ref_size


def get_beans_count_by_colors(img, ref_size):
    h,w,c = img.shape
    img = img.reshape((h*w, c))
    kmeans_model = KMeans(n_clusters=5) # 4 colors + 1 bg = 5 clusters
    cluster_labels = kmeans_model.fit_predict(img)
    labels_count = Counter(cluster_labels)
    centroids = kmeans_model.cluster_centers_
    total = 0
    for label, count in labels_count.items():
        bean_count = int(count/ref_size)
        print(f'{centroids[label]}: {bean_count}')


def show_res(img, img_hsv, mask, beans):
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(16, 4))
    axs[0].matshow(img)
    axs[1].matshow(img_hsv)
    axs[2].matshow(mask)
    axs[3].matshow(beans)
    plt.show()


def main():
    img = cv2.imread('./data/jellybeans2.png')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = img_seg(img_hsv)
    _mask = cv2.merge((mask,mask,mask))
    beans = cv2.cvtColor(np.where(_mask > 0, img, 0), cv2.COLOR_BGR2RGB)
    
    ref_size = get_beans_count(mask) 
    get_beans_count_by_colors(beans, ref_size)
    show_res(img, img_hsv, mask, beans)


if __name__=='__main__':
    main()
