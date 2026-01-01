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

# Remember the ending "/"
# eg: PHOTO_DEST_DIR = "/Users/username/Pictures/GR3/"
PHOTO_DEST_DIR = "D:/doc/Pictures/GR3/"

# GR_HOST is FIXED. DO NOT CHANGE!!
GR_HOST = "http://192.168.0.1/"
PHOTO_LIST_URI = "v1/photos"
GR_PROPS = "v1/props"
STARTDIR = ""
STARTFILE = ""

# Supported devices
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
            print("Error code: %d, Error message: %s" % (props['errCode'], props['errMsg']))
            sys.exit(1)
        else:
            return props['model']
    except urllib.error.URLError as e:
        print("Unable to fetch device props. Please check your Wi-Fi connection to the camera.")
        sys.exit(1)

def getBatteryLevel():
    req = urllib.request.Request(GR_HOST + GR_PROPS)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        props = json.loads(data)
        if props['errCode'] != 200:
            print("Error code: %d, Error message: %s" % (props['errCode'], props['errMsg']))
            sys.exit(1)
        else:
            return props['battery']
    except urllib.error.URLError as e:
        print("Unable to fetch device props from %s" % DEVICE)
        sys.exit(1)

def getPhotoList():
    req = urllib.request.Request(GR_HOST + PHOTO_LIST_URI)
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read()
        photoDict = json.loads(data)
        if photoDict['errCode'] != 200:
            print("Error code: %d, Error message: %s" % (photoDict['errCode'], photoDict['errMsg']))
            sys.exit(1)
        else:
            photoList = []
            for dic in photoDict['dirs']:
                # Check if this directory already exists in local PHOTO_DEST_DIR
                # If not, create one
                if not os.path.isdir(PHOTO_DEST_DIR+dic['name']):
                    os.makedirs(PHOTO_DEST_DIR+dic['name'])
                
                # Generate the full photo list
                for file in dic['files']:
                    photoList.append("%s/%s" % (dic['name'], file ))
            return photoList
    except urllib.error.URLError as e:
        print("Unable to fetch photo list from %s" % DEVICE)
        sys.exit(1)
    
def getLocalFiles():
    fileList = []
    if not os.path.exists(PHOTO_DEST_DIR):
        try:
            os.makedirs(PHOTO_DEST_DIR)
        except OSError as e:
            print(f"Error creating directory {PHOTO_DEST_DIR}: {e}")
            sys.exit(1)

    for (dir, _, files) in os.walk(PHOTO_DEST_DIR):
        for f in files:
            fileList.append((os.path.join(dir, f).replace(PHOTO_DEST_DIR, "")).replace('\\', '/'))
    return fileList

def fetchPhoto(photouri):
    try:
        if DEVICE == 'RICOH GR II':
            f = urllib.request.urlopen(GR_HOST+photouri)
        else:
            # GR III series use API v1 path
            f = urllib.request.urlopen(GR_HOST+PHOTO_LIST_URI+'/'+photouri)
        with open(PHOTO_DEST_DIR+photouri, "wb") as localfile:
            localfile.write(f.read())
        return True
    except urllib.error.URLError as e:
        return False

def shutdownGR():
    try:
        req = urllib.request.Request("http://192.168.0.1/v1/device/finish")
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, json.dumps({}).encode())
    except:
        pass # Ignore errors on shutdown
    
def downloadPhotos(isAll):
    print("Fetching photo list from %s ..." % DEVICE)
    photoLists = getPhotoList()
    localFiles = getLocalFiles()
    count = 0
    if isAll == True:
        totalPhoto = len(photoLists)
    else:
        starturi = "%s/%s" % (STARTDIR, STARTFILE)
        if starturi not in photoLists:
            print("Unable to find %s in Ricoh %s" % (starturi, DEVICE))
            sys.exit(1)
        else:
            while True:
                if not photoLists:
                    break
                if photoLists[0] != starturi:
                    photoLists.pop(0)
                else:
                    totalPhoto = len(photoLists)
                    break
                    
    print("Start to download photos ...")    
    while True:
        if not photoLists:
            print("\nAll photos are downloaded.")
            shutdownGR()
            break
        else:
            photouri = photoLists.pop(0)
            count += 1
            if photouri in localFiles:
                print("(%d/%d) Skip %s, already exists locally!!" % (count, totalPhoto, photouri))
            else:
                print("(%d/%d) Downloading %s ... " % (count, totalPhoto, photouri), end=' ')
                if fetchPhoto(photouri) == True:
                    print("done!!")
                else:
                    print("*** FAILED ***")

if __name__ == "__main__":
    # Set connection timeout to 2 seconds
    socket.setdefaulttimeout(2)
    
    # Setting up argument parser
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='''
GRsync for GR III HDF
Sync photos from Ricoh GR II, III, IIIx, and HDF models via Wi-Fi.
''')
    parser.add_argument("-a", "--all", action="store_true", help="Download all photos")
    parser.add_argument("-d", "--dir", help="Assign directory (eg. -d 100RICOH). MUST use with -f")
    parser.add_argument("-f", "--file", help="Start to download photos from specific file \n(eg. -f R0000005.JPG). MUST use with -d")

    print("Connecting to GR...")
    model = getDeviceModel()
    
    if model not in SUPPORT_DEVICE:
        print("Your source device '%s' is unknown or not supported!" % model)
        print("Supported devices:", SUPPORT_DEVICE)
        sys.exit(1)
    else:
        DEVICE = model
        print(f"Connected to {DEVICE}")

    batt = getBatteryLevel()
    if batt < 15:
        print("Battery level is low (%s%%). Please charge before syncing!" % batt)
        sys.exit(1)

    args = parser.parse_args()

    if args.all == True and args.dir is None and args.file is None:
        downloadPhotos(isAll=True)
    elif args.dir is not None and args.file is not None and args.all == False:
        match_dir = re.match(r"^[1-9]\d\dRICOH$", args.dir)
        if match_dir:
            STARTDIR = args.dir
        else:
            print("Incorrect directory name. It should be something like '100RICOH'.")
            sys.exit(1)
        
        # Check filename prefix based on device model
        if 'GR IIIx' in DEVICE:
            match_file = re.match(r"^RX\d{6}\.JPG$", args.file)
        else:
            match_file = re.match(r"^R0\d{6}\.JPG$", args.file)
            
        if match_file:
            STARTFILE = args.file
        else:
            print("Incorrect file name format. Ensure it matches camera naming (R0... or RX...).")
            sys.exit(1)
        downloadPhotos(isAll=False)
    else:
        parser.print_help()
