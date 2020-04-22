import os
import shutil
import cv2
import numpy as np
import argparse
from glob import glob
import itertools
from tqdm import tqdm
import collections
import multiprocessing as MP


manager = MP.Manager()
MP_idendical_list = manager.list()


def get_hist_similarity(img1, img2):
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
    hist1= cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
    hist2= cv2.normalize(hist2, hist2).flatten()
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

  
def is_identical(files):
    """ Find identical images.
    The image pair will be converted to gray image for comparison.
    Note that this method can only find exactly matched images.
    """
    f1, f2 = files
    img1 = cv2.imread(f1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(f2, cv2.IMREAD_UNCHANGED)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    identical = (gray1.shape == gray2.shape and 
            not(np.bitwise_xor(gray1,gray2).any()))
    if identical:
        MP_idendical_list.append((f1,f2))


def is_similar(files, threshold=0.96):
    """ Find similar images.
    The threshold sould be set in the range of [0,1].
    Higher threshold means higher similarity.
    Note that the method is not robust and reliabel.
    Sometimes it even fails to spot 'almost identical' images.
    """
    f1, f2 = files
    img1 = cv2.imread(f1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(f2, cv2.IMREAD_UNCHANGED)
    similarity = get_hist_similarity(img1, img2)
    similar = True if similarity > threshold else False
    if similar:
        MP_idendical_list.append((f1, f2))


def clean_duplicated(files_list):
  '''
  source: https://stackoverflow.com/a/17483756
  purpose: [(A,B), (B,C), (A,C), (D,E)] --> [(A,B,C), (D,E)]
  to future me: I don't understand all the code here...
  '''
  # build an adjacency list representation of the input
  graph = collections.defaultdict(set)
  for first, second in files_list:
    graph[first].add(second)
    graph[second].add(first)

  # breadth-first search the graph to produce the output
  output = []
  marked = set() # a set of all nodes whose connected component is known
  for node in graph:
    if node not in marked:
      # this node is not in any previously seen connected component
      # run a breadth-first search to determine its connected component
      frontier = set([node])
      connected_component = []
      while frontier:
        marked |= frontier
        connected_component.extend(frontier)
        # find all unmarked nodes directly connected to frontier nodes
        # they will form the new frontier
        new_frontier = set()
        for node in frontier:
          new_frontier |= graph[node] - marked
        frontier = new_frontier
      #output.append(tuple(connected_component))
      output.append(list(connected_component))

  return output


def get_img_size(img_file):
    img = cv2.imread(img_file)
    return img.shape[0]*img.shape[1]


def get_list_info(idendical_list):
    for _, files in enumerate(idendical_list):
        sorted_files = sorted(files, 
                key=lambda f: get_img_size(f), reverse=True)
        #print(_, [os.path.basename(f) for f in sorted_files])


def move2_temp_folders(idendical_list):
    """ Move possible similar images to different folders
    for manual checking later.
    """
    for dir_idx, f_list in enumerate(idendical_list):
        folder = os.path.join(
                os.path.dirname(f_list[0]), '{:03d}'.format(dir_idx))
        os.mkdir(folder)
        for f in f_list:
            print('Moving {} to {}...'.format(f, folder))
            shutil.move(f, folder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', required=True,
            help='path to the folder of input images')
    args = parser.parse_args()

    files_list = glob(os.path.join(args.folder, '*.*'))
    process_len = sum(1 for _ in itertools.combinations(files_list, 2))

    # set None to use the number returned by cpu_count()
    with MP.Pool(processes=None) as p: 
        with tqdm(total=process_len) as pbar:
            for _ in p.imap_unordered(is_similar,
                    itertools.combinations(files_list, 2)):
                pbar.set_description('Identical pairs {}'.format(len(MP_idendical_list)))
                pbar.update()

    idendical_list = clean_duplicated(MP_idendical_list)
    #get_list_info(idendical_list)
    move2_temp_folders(idendical_list)


if __name__=='__main__':
    main()
