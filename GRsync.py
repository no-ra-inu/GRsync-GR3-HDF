#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.error
import sys
import json
import argparse
from argparse import RawTextHelpFormatter
import socket
import re
import os
from datetime import datetime

# Base directory for photos
PHOTO_DEST_BASE = "" #格納するフォルダ名を入力

# GR_HOST is FIXED. DO NOT CHANGE!!
GR_HOST = "http://192.168.0.1/"
PHOTO_LIST_URI = "v1/photos"
GR_PROPS = "v1/props"
STARTDIR = ""
STARTFILE = ""

SUPPORT_DEVICE = [
    'RICOH GR II',
    'RICOH GR III',
    'RICOH GR IIIx',
    'RICOH GR III HDF',
    'RICOH GR IIIx HDF',
    'RICOH GR IV',
    'RICOH GR IV HDF',
    'RICOH GR IV Monochrome'
]
DEVICE = "GR2"

def getDeviceModel():
    req = urllib.request.Request(GR_HOST + GR_PROPS)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        props = json.loads(data)
        if props['errCode'] != 200:
            print("Error code: %d, Error message: %s" % (props['errCode'], props['errMsg']))
            sys.exit(1)
        else:
            return props['model']
    except urllib.error.URLError as e:
        print("Unable to fetch device props. Please check your Wi-Fi connection.")
        sys.exit(1)

def getBatteryLevel():
    req = urllib.request.Request(GR_HOST + GR_PROPS)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        props = json.loads(data)
        return props['battery']
    except:
        return 0

def getPhotoList():
    req = urllib.request.Request(GR_HOST + PHOTO_LIST_URI)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        photoDict = json.loads(data)
        if photoDict['errCode'] != 200:
            print("Error: %s" % photoDict['errMsg'])
            sys.exit(1)

        photoList = []
        for dic in photoDict['dirs']:
            for file in dic['files']:
                photoList.append("%s/%s" % (dic['name'], file ))
        return photoList
    except Exception as e:
        print("Error fetching photo list: %s" % e)
        sys.exit(1)

def fetchPhotoWithProgress(photouri, dest_root, useTimestamp, count, total):
    """Downloads a photo with progress bar."""
    if useTimestamp:
        # -tf 指定時はファイル名のみ抽出して日付フォルダに保存
        filename = os.path.basename(photouri)
        if os.path.splitext(filename)[1].lower() == ".dng":
            local_path = os.path.join(dest_root, "DNG", filename).replace('\\', '/')
        else:
            local_path = os.path.join(dest_root, filename).replace('\\', '/')
    else:
        # 通常時はカメラのディレクトリ構造（100RICOH等）を維持
        filename = os.path.basename(photouri)
        photo_dir = os.path.dirname(photouri)
        if os.path.splitext(filename)[1].lower() == ".dng":
            local_path = os.path.join(dest_root, photo_dir, "DNG", filename).replace('\\', '/')
        else:
            local_path = os.path.join(dest_root, photouri).replace('\\', '/')

    local_dir = os.path.dirname(local_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    if os.path.exists(local_path):
        # 進捗表示の行を壊さないように空改行を入れてからメッセージを出す
        sys.stdout.write(f"\r({count}/{total}) Skip {photouri}, already exists.\n")
        return True

    try:
        url = GR_HOST + (photouri if DEVICE == 'RICOH GR II' else PHOTO_LIST_URI + '/' + photouri)

        with urllib.request.urlopen(url) as response:
            file_size = int(response.info().get('Content-Length', 0))
            chunk_size = 1024 * 256
            downloaded = 0
            last_shown_pct = -1

            with open(local_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if file_size > 0:
                        percent = downloaded / file_size
                        current_pct = int(percent * 100)
                        if current_pct > last_shown_pct:
                            last_shown_pct = current_pct
                            bar_length = 20
                            filled = int(bar_length * percent)
                            bar = '=' * filled + '-' * (bar_length - filled)
                            sys.stdout.write(f"\r({count}/{total}) [{bar}] {current_pct:>3}% {photouri}")
                            sys.stdout.flush()
            print()
        return True
    except Exception as e:
        print(f"\n*** FAILED {photouri}: {e} ***")
        return False

def shutdownGR():
    try:
        req = urllib.request.Request("http://192.168.0.1/v1/device/finish")
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req, json.dumps({}).encode())
    except:
        pass

def downloadPhotos(isAll, useTimestamp):
    if useTimestamp:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        dest_root = os.path.join(PHOTO_DEST_BASE, timestamp).replace('\\', '/')
    else:
        dest_root = PHOTO_DEST_BASE

    photoLists = getPhotoList()

    if not isAll:
        starturi = "%s/%s" % (STARTDIR, STARTFILE)
        if starturi in photoLists:
            photoLists = photoLists[photoLists.index(starturi):]
        else:
            print(f"File {starturi} not found.")
            sys.exit(1)

    totalPhoto = len(photoLists)
    print(f"Downloading {totalPhoto} photos to {dest_root}...")

    for i, photouri in enumerate(photoLists, 1):
        fetchPhotoWithProgress(photouri, dest_root, useTimestamp, i, totalPhoto)

    print("\nCompleted.")
    shutdownGR()

if __name__ == "__main__":
    socket.setdefaulttimeout(30)

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='GRsync for HDF')
    parser.add_argument("-a", "--all", action="store_true", help="Download all photos")
    parser.add_argument("-d", "--dir", help="Directory name (e.g., 100RICOH)")
    parser.add_argument("-f", "--file", help="File name (e.g., R0000001.JPG)")
    parser.add_argument("-tf", "--timestamp-folder", action="store_true", help="Save to a YMD-HM subfolder (ignores camera dir structure)")

    print("Connecting to GR...")
    model = getDeviceModel()
    if model in SUPPORT_DEVICE:
        DEVICE = model
        print(f"Connected to {DEVICE}")
    else:
        print(f"Unsupported device: {model}")
        sys.exit(1)

    if getBatteryLevel() < 15:
        print("Battery low. Please charge.")
        sys.exit(1)

    args = parser.parse_args()
    if args.all or (args.dir and args.file):
        if args.dir: STARTDIR = args.dir
        if args.file: STARTFILE = args.file
        downloadPhotos(isAll=args.all, useTimestamp=args.timestamp_folder)
    else:
        parser.print_help()
