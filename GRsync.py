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

# ==========================================================
# METADATA
# ==========================================================
__version__ = "1.1.0"
__author__ = "no-ra-inu"

# ==========================================================
# CONFIGURATION
# ==========================================================
# Base directory for photos. Change this to your local path.
# IMPORTANT: Use "/" at the end of the path.
PHOTO_DEST_BASE = "D:/doc/Pictures/GR3/"

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
    'RICOH GR IIIx HDF'
]
DEVICE = "GR2"

def getDeviceModel():
    req = urllib.request.Request(GR_HOST + GR_PROPS)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        props = json.loads(data)
        if props['errCode'] != 200:
            print(f"Error code: {props['errCode']}, Message: {props['errMsg']}")
            sys.exit(1)
        else:
            return props['model']
    except urllib.error.URLError:
        print("Unable to fetch device props. Please check your Wi-Fi connection to the camera.")
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
            print(f"Error: {photoDict['errMsg']}")
            sys.exit(1)
        
        photoList = []
        for dic in photoDict['dirs']:
            for file in dic['files']:
                photoList.append("%s/%s" % (dic['name'], file ))
        return photoList
    except Exception as e:
        print(f"Error fetching photo list: {e}")
        sys.exit(1)

def fetchPhotoWithProgress(photouri, dest_root, useTimestamp, count, total):
    """Downloads a photo with a Homebrew-style progress bar."""
    if useTimestamp:
        # Save directly under the timestamp folder without camera subdirs
        filename = os.path.basename(photouri)
        local_path = os.path.join(dest_root, filename).replace('\\', '/')
    else:
        # Maintain camera's directory structure (e.g., 100RICOH/...)
        local_path = os.path.join(dest_root, photouri).replace('\\', '/')
    
    local_dir = os.path.dirname(local_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    # Check if file already exists locally to skip download
    if os.path.exists(local_path):
        sys.stdout.write(f"\r({count}/{total}) Skip {photouri}, already exists.\n")
        return True

    try:
        url = GR_HOST + (photouri if DEVICE == 'RICOH GR II' else PHOTO_LIST_URI + '/' + photouri)
        
        with urllib.request.urlopen(url) as response:
            file_size = int(response.info().get('Content-Length', 0))
            chunk_size = 1024 * 16
            downloaded = 0
            
            with open(local_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if file_size > 0:
                        percent = downloaded / file_size
                        bar_length = 20
                        filled = int(bar_length * percent)
                        bar = '=' * filled + '-' * (bar_length - filled)
                        sys.stdout.write(f"\r({count}/{total}) [{bar}] {int(percent*100):>3}% {photouri}")
                        sys.stdout.flush()
            print() # New line after finish
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
            print(f"File {starturi} not found on camera.")
            sys.exit(1)

    totalPhoto = len(photoLists)
    print(f"Downloading {totalPhoto} photos to: {dest_root}")
    
    for i, photouri in enumerate(photoLists, 1):
        fetchPhotoWithProgress(photouri, dest_root, useTimestamp, i, totalPhoto)
    
    print("\nAll tasks completed.")
    shutdownGR()

if __name__ == "__main__":
    socket.setdefaulttimeout(5)
    
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='''
GRsync: A tool to sync photos from Ricoh GR series via Wi-Fi.
Supports GR II, III, IIIx, and HDF models.
''')
    parser.add_argument("-a", "--all", action="store_true", help="Download all photos")
    parser.add_argument("-d", "--dir", help="Specify directory (e.g., 100RICOH)")
    parser.add_argument("-f", "--file", help="Specify start file (e.g., R0000001.JPG)")
    parser.add_argument("-tf", "--timestamp-folder", action="store_true", 
                        help="Create a YMD-HM subfolder and save photos directly inside it")

    print("Connecting to GR...")
    model = getDeviceModel()
    if model in SUPPORT_DEVICE:
        DEVICE = model
        print(f"Connected to {DEVICE}")
    else:
        print(f"Unsupported device detected: {model}")
        sys.exit(1)

    batt = getBatteryLevel()
    if batt < 15:
        print(f"Battery level is too low ({batt}%). Please charge the camera.")
        sys.exit(1)

    args = parser.parse_args()
    if args.all or (args.dir and args.file):
        if args.dir: STARTDIR = args.dir
        if args.file: STARTFILE = args.file
        downloadPhotos(isAll=args.all, useTimestamp=args.timestamp_folder)
    else:
        parser.print_help()
