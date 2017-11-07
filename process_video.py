#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:28:59 2017

@author: tortugar
"""

import cv2
import os.path
import matplotlib.pylab as plt 



vname = '10_20_17_crh1_001-0000.avi'
ppath = '/Users/tortugar/Desktop/Run_Experiment/'


print(cv2.__version__)
vidcap = cv2.VideoCapture(os.path.join(ppath, vname))

success,image = vidcap.read()
height = image.shape[0]
width  = image.shape[1]
vidout = cv2.VideoWriter(os.path.join(ppath, 'out.avi'),cv2.cv.FOURCC('m','p','4','v'), 5, (width, height))
#vidout = cv2.VideoWriter(os.path.join(ppath, 'out.mpg'),cv2.cv.FOURCC('M','J','P','G'), 5, (width, height))

plt.figure()
ax = plt.subplot(111)
plt.ion()

count = 0
success = True
while success:
    success,image = vidcap.read()
    #cv2.imshow('Frame',image)
    
    print 'Read a new frame: ', success, count
    #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    count += 1  
    vidout.write(image)
    ax.clear()
    ax.imshow(image.mean(axis=2)[::2,::2], cmap='gray')
    plt.pause(0.001)

vidcap.release()
vidout.release()


# open video file to write frames to video
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
  
  
# write text into video
#cv2.putText(img,'text',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

# draw rectangle
#cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)

# efficient video compression with mpeg
# ffmpeg -i out.avi -vcodec libx264 -crf 20 output.mp4

