#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, random
import cv2
import numpy as np
import time
import csv
from PIL import ImageFont, ImageDraw, Image
import argparse
import audio_lib


PHOTO = 'photos/'
AUDIO = 'audio_clips/'
FONTPATH = 'fonts/FreeMonoBold.ttf'
WIDTH = 640
HEIGHT = 480

def recursive_files(dir):
    for path, _, fnames in os.walk(dir):
        for fname in fnames:
            yield os.path.join(path, fname)

def online_choice(iterable):
    for n, x in enumerate(iterable, 1):
        if random.randrange(n) == 0:
            pick = x
    return pick

def show_text(file_name, dictionary=None):
    text_card = np.zeros((HEIGHT,WIDTH,3), np.uint8)
    text_card[:] = (0,180,200)
    obj_name = os.path.splitext(os.path.basename(file_name))[0]
    text = obj_name.replace('_', ' ')
    if dictionary:
        text = dictionary.get(text) + ' ' # a workaround to prevent the word ended with 'o͘' being cropped
    TEXT = text.upper()

    TEXTColor = (10,10,10)
    textColor = (255,255,255)

    font = ImageFont.truetype(FONTPATH, 64)
    TEXTsize = font.getsize(TEXT)
    textsize = font.getsize(text)
    linespace = 10
    h_shift = 0
    TEXT_pos = ((WIDTH-TEXTsize[0])//2-h_shift, (HEIGHT-TEXTsize[1])//2-5*linespace)
    text_pos = ((WIDTH-textsize[0])//2-h_shift, (HEIGHT+textsize[1])//2-3*linespace)

    img_pil = Image.fromarray(text_card)
    draw = ImageDraw.Draw(img_pil)
    draw.text(TEXT_pos, TEXT, font=font, fill=TEXTColor)
    draw.text(text_pos, text, font=font, fill=textColor)
    text_card = np.array(img_pil)

    return text_card


def get_audio_path(file_path):
    return file_path.replace(PHOTO, AUDIO).replace(os.path.splitext(file_path)[1],'.mp3')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--taigi", required=False, action='store_true', help='toggle to use Tâigí')
    args = vars(ap.parse_args())
    taigi = args["taigi"]

    if taigi:
        with open('pio.csv', mode='r') as infile:
            dictionary = dict(csv.reader(infile, skipinitialspace=False)) # keep the initial space to compensate the one added in show_text()
        img = cv2.imread('pics/Cover_taigi.png')
    else:
        dictionary = None
        img = cv2.imread('pics/Cover.png')

    cv2.imshow('Bat Ji', img)
    question_path = None

    while True:
        k = cv2.waitKey(33)
        if k == 32: #Space
            question_path = online_choice(recursive_files(PHOTO))
            question_card = show_text(question_path, dictionary)
            cv2.imshow('Bat Ji', question_card)
        elif k == ord('t'): #text
            question_card = show_text(question_path, dictionary)
            cv2.imshow('Bat Ji', question_card)
        elif k == ord('a'): #answer/ audio
            answer_img = cv2.imread(question_path)
            cv2.imshow('Bat Ji', answer_img)
            audio_path = get_audio_path(question_path)
            audio_lib.get_audio(audio_path, question_card)
        elif k == 27:
            break


if __name__ == "__main__":
        main()
