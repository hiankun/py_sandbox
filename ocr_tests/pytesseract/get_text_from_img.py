#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt install tesseract-ocr
# pip install pytesseract

import pytesseract
import cv2
import argparse

'''
usage: python get_text_from_img.py -i <img> -l <lang>
'''

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
        help='path to input image')
ap.add_argument('-l', '--lang', default='eng',
        help='language to be extracted')
args=vars(ap.parse_args())

img = cv2.imread(args['image'])
print(img.shape)
language = args['lang']
print(pytesseract.image_to_string(img, lang=language))
