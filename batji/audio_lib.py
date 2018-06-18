#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

#import simpleaudio as sa # This need wav files
# avconv -i audio/d/dog.mp3 -acodec pcm_u8 -ar 8000 audio/d/dog.wav

import time
import os
from gtts import gTTS
import pyglet
from subprocess import call

def get_tts_mp3(lang, text, audio_path):
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)
    print('>>> Generated and saved audio file to {}.'.format(audio_path))
    return


def play_audio(audio_path):
    for i in range(2):
        call(['mpg123', audio_path])
        if i != 1: time.sleep(1.5)
    return


def get_audio(audio_path, text):
    if os.path.isfile(audio_path):
        play_audio(audio_path)
    else:
        print('>>> No audio file named {}...'.format(audio_path))
        obj_name = os.path.splitext(os.path.basename(audio_path))[0]
        text = obj_name.replace('_', ' ')
        lang = 'en'
        get_tts_mp3(lang, text, audio_path)
        play_audio(audio_path)

    return
