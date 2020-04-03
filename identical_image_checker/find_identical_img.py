import os
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
  f1, f2 = files
  img1 = cv2.imread(f1, cv2.IMREAD_UNCHANGED)
  img2 = cv2.imread(f2, cv2.IMREAD_UNCHANGED)
  similarity = get_hist_similarity(img1, img2)
  identical = True if similarity > 0.95 else False
  if identical:
    MP_idendical_list.append(
            (os.path.basename(f1), os.path.basename(f2)))
  #print('{}: {} <--> {}'.format(get_hist_similarity(img1, img2), f1, f2))
  #gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  #gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  #identical = (gray1.shape == gray2.shape and 
  #    not(np.bitwise_xor(gray1,gray2).any()))
  #if identical:
  #  MP_idendical_list.append((f1,f2))


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
      output.append(tuple(connected_component))

  return output


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
      for _ in p.imap_unordered(is_identical, itertools.combinations(files_list, 2)):
        pbar.set_description('Identical pairs {}'.format(len(MP_idendical_list)))
        pbar.update()

  idendical_list = clean_duplicated(MP_idendical_list)
  for _, f in enumerate(idendical_list):
    print(_, sorted(f)) #TODO: write to file


if __name__=='__main__':
  main()


# repo code: might be used for similarity comparison...
#hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8],
#  [0, 256, 0, 256, 0, 256])
#hist1= cv2.normalize(hist1, hist1).flatten()

#hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8],
#  [0, 256, 0, 256, 0, 256])
#hist2= cv2.normalize(hist2, hist2).flatten()

#d = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
#print(d)

