#!/usr/bin/env python
import cv2 as cv
import numpy as np
import os
import shutil
from os.path import expanduser
from scipy.misc import imresize
from argparse import ArgumentParser

# folder icon maker
# '''
# This Script takes an icon and embosses it onto the MacOs folder icon to make custom folder icons for your project
# '''
cwd = os.getcwd()
folder_icon_path = cwd + "/resources/GenericFolderIcon.png"

def main():
    parser = ArgumentParser()
    parser.add_argument('-i', 
                        '--icon', 
                        help='path to input icon to be superimposed', 
                        required=True,
                        metavar="FILENAME")
    parser.add_argument('-o', 
                        '--output', 
                        help='name for output file', 
                        required=True)                    
    args = parser.parse_args()

    icon=superimposeIcon(args.icon)
    makeIcns(args.output, icon)

# theme_icon_path=input("Icon Path: ")
# theme_icon_path="/Users/lisa/Documents/testicons/resources/noun_clouds.png"
# icon_name=input("Icon Name: ")


def superimposeIcon(theme_icon_path):
    '''
    Takes an icon and embosses it onto the MacOs folder icon to make custom folder icons
    '''

    # load image files
    rgb_folder=cv.imread(folder_icon_path, cv.IMREAD_UNCHANGED)
    rgb_icon=cv.imread(theme_icon_path, cv.IMREAD_UNCHANGED)
    (h, w) = rgb_folder.shape[:2]
    (iH, iW) = rgb_icon.shape[:2]

    # make overlay mask of the same size as the folder icon
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[round((h - iH)/2):round((h - iH)/2)+iH, round((w - iW)/2):round((w - iW)/2)+iW] = rgb_icon

    # Get individual layers
    (iB, iG, iR, iA) = cv.split(overlay)
    (fB, fG, fR, fA) = cv.split(rgb_folder)
    
    # only using opacity layer to get shape because icons should be simple enough only the shape matters...?
    iA = (iA/255)
    # the numbers tacked onto the back here make the icon a similar shade as the system ones
    #red
    nR = fR
    nR[iA==1] = fR[iA==1]*0.757 
    # green
    nG = fG
    nG[iA==1] = fG[iA==1]*0.888 
    # blue
    nB = fB
    nB[iA==1] = fG[iA==1]*0.928 

    # merge layers into single image var (making sure the type is the same everywhere)
    output = cv.merge([nB.astype(float), nG.astype(float), nR.astype(float), fA.astype(float)])

    return(output)


def makeIcns(icon_name, icon):
    '''
    Takes icon and generates .icns file with all the required resolutions inside
    '''
    #icns file
    icns_dir_path = cwd + "/icns/"
    icns_path = icns_dir_path + "/" + icon_name + ".iconset"

    # try to make that folder
    if os.path.exists(icns_dir_path + "/" + icon_name + "icns"):
        raise Exception("That name is taken")
    else:
        os.makedirs(icns_path)

    os.chdir(icns_path)

    # required files for icns folder
    icons = [('icon_512x512@2x.png', (1024, 1024)),
            ('icon_512x512.png',  (512, 512)),
            ('icon_256x256@2x.png', (512, 512)),
            ('icon_256x256.png',  (256, 256)),
            ('icon_128x128@2x.png', (256, 256)),
            ('icon_128x128.png',  (128, 128)),
            ('icon_32x32@2x.png',  (64, 64)),
            ('icon_32x32.png',   (32, 32)),
            ('icon_16x16@2x.png',  (32, 32)),
            ('icon_16x16.png', (16, 16))]

    # generate required files
    for i in icons:
        im = imresize(icon, i[1], interp='bilinear', mode=None) 
        cv.imwrite( '{}/{}'.format(icns_path, i[0]), im)

    # make into icns file
    os.chdir(icns_dir_path)
    os.system("iconutil -c icns "+ icon_name + ".iconset")
    shutil.rmtree( icon_name + ".iconset" )

if __name__ == "__main__":
    main()