# folder icon maker
'''
This Script takes an icon and embosses it onto the MacOs folder icon to make custom folder icons for your project
'''

# from scipy.misc import imread
import cv2 as cv
import numpy as np
import os
from os.path import expanduser
from scipy.misc import imresize
# import os
# import glob
# import imageio

home = expanduser('~')

folder_icon_path = home + "/Documents/testicons/resources/GenericFolderIcon.png"
# theme_icon_path=input("Icon Path: ")
theme_icon_path="/Users/lisa/Documents/testicons/resources/noun_clouds.png"
icon_name=input("Icon Name: ")

# load image files
rgb_folder=cv.imread(folder_icon_path, cv.IMREAD_UNCHANGED)
rgb_icon=cv.imread(theme_icon_path, cv.IMREAD_UNCHANGED)
(h, w) = rgb_folder.shape[:2]
(iH, iW) = rgb_icon.shape[:2]

# make overlay mask
overlay = np.zeros((h, w, 4), dtype="uint8")

overlay[round((h - iH)/2):round((h - iH)/2)+iH, round((w - iW)/2):round((w - iW)/2)+iW] = rgb_icon
# cv.imwrite("/Users/lisa/Documents/testicons/icns/test1.png", overlay)

# Get individual layers
(iB, iG, iR, iA) = cv.split(overlay)
(fB, fG, fR, fA) = cv.split(rgb_folder)

# # alpha layer opacity is set to 0.25, converted to values between 1 and 0
# iA=1-((iA*0.2)/255)

# # Manualy weight each layer of the folder png with the opacity of the icon to create "embossed" feel.
# nR= (fR)*((iA))
# nG= (fG)*((iA))
# nB= (fB)*((iA))

iA = (iA/255)

nR = fR
nR[iA==1] = fR[iA==1]*0.757 

nG = fG
nG[iA==1] = fG[iA==1]*0.888 

nB = fB
nB[iA==1] = fG[iA==1]*0.928 




# merge layers into single image var
output = cv.merge([nB.astype(float), nG.astype(float), nR.astype(float), fA.astype(float)])


#icns file
icns_dir_path = home + "/Documents/testicons/icns/"
icns_path = icns_dir_path + "/" + icon_name + ".iconset"

if os.path.exists(icns_path):
    raise Exception("That name is taken")
    
else:
    os.makedirs(icns_path)

os.chdir(icns_path)

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

for icon in icons:
    im = imresize(output, icon[1], interp='bilinear', mode=None) 
    cv.imwrite( '{}/{}'.format(icns_path, icon[0]), im)

os.chdir(icns_dir_path)
os.system("iconutil -c icns "+ icon_name + ".iconset")