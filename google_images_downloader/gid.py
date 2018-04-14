#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import time
#import requests
import urllib3
from socket import error as SocketError
import errno
import sys
from imagesoup import ImageSoup

# parse the arguments
ap = argparse.ArgumentParser(description='''
    This is gid (Google Images downloader).

    The purpose of this script is to simplify the download process
    from the searching results of Google Images.
    ''', formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument("-k", "--search-keywords", required=True,
    help="""The searching keyword.
NOTE: Without assign -d option, the images will be saved as
      your_keywords/your-keywords-dddd.ext.
      When -d or -f option is given, the images will be saved as
      dir_name/file-name-dddd.ext.""")
ap.add_argument("-s", "--search-size", default='any',
    help="image size to search; the default value is 'any'")
ap.add_argument("-n", "--image-number", type=int, default='10',
    help="Image number to search; the default value is 10.")
ap.add_argument("-d", "--saving-directory", default=None,
    help="Directory in which the images to be saved.")
ap.add_argument("-f", "--saving-file", default=None,
    help="File name to be saved.")
args = vars(ap.parse_args())

# set up
keywords = args["search_keywords"]
filename = args["saving_file"]
size = args["search_size"]
number = args["image_number"]
directory = ( "_".join(args["saving_directory"].split())
        if args["saving_directory"] is not None
        else "_".join(keywords.split()) )
filename = ( "-".join(args["saving_file"].split())
        if args["saving_file"] is not None
        else "-".join(keywords.split()) )

if os.path.exists(directory):
    directory += time.strftime("_%Y%m%d_%H%M%S")
os.makedirs(directory)

soup = ImageSoup()
images = soup.search(keywords, image_size=size, n_images=number)
http = urllib3.PoolManager()

for i, img in enumerate(images):
    # During the requesting loop, there're many kinds of errors
    # which crash the program.
    # Therefore here are some try-except blocks to deal with it.
    # I'm not good at handling exceptions, so if you have better
    # mechanism for this, please let me know.
    try:
        response = http.request('GET', img.URL)
        try:
            # Content-Type might in the form of
            # ``image/jpeg; charset=utf-8'' or something alike.
            # The following code is used to handle it.
            file_type, file_ext, *_ = [tmp.strip()
                for tmp in response.info()['Content-Type'].replace(';', '/').split('/')]
        except KeyError:
            print("response.info() = {}".format(response.info()))
            continue
        except ValueError:
            print("response.info()['Content-Type'] = {}"
                    .format(response.info()['Content-Type']))
            continue
        if (file_type == 'image' and file_ext != 'vnd.ms-photo'):
            file_path = "{0}/{1}_{2:04d}.{3}".format(directory, filename, i, file_ext)
            #file_path = "{0}/{1}_{2:04d}.{3}".format(
            #        directory,
            #        "-".join(filename.split()), i, file_ext)
            img.to_file(file_path)
            print('{0} has been saved...'.format(file_path))
    except urllib3.exceptions.HTTPError as e:
        print('HTTPError: ', e)
        continue
    except urllib3.exceptions.ProtocolError as e:
        print('ProtocolError: ', e)
        continue
    except SocketError as e:
        print('SocketError: ', e)
        continue

