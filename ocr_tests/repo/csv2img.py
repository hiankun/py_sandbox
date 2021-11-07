import numpy as np
import cv2
import csv

input_csv = #https://www.kaggle.com/sachinpatel21/az-handwritten-alphabets-in-csv-format

def main():

    with open(input_csv, 'r') as f:
        data = csv.reader(f)
        for row in data:
            label = row[0]
            img = np.asarray(row[1:],dtype=np.uint8).reshape(28,28)
            cv2.imshow('res', img)
            if cv2.waitKey(0) & 0xff == ord('q'):
                break


if __name__=='__main__':
    main()
