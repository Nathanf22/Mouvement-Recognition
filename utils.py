#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:33:12 2022

@author: nathan
"""

import cv2
import numpy as np
from path import Path
#mp_pose = mp.solutions.pose

abs_path = Path('').abspath()
print('path: {}'.format(abs_path))

global depth, frame_dim

depth = False

if depth:
    frame_dim = 3
else:
    frame_dim = 2
    
def convert_frame_to_dense_OFI(frame, prev_frame):
    '''
    

    Parameters
    ----------
    frame : numpy array
    prev_frame : numpy array 
        this function convert two consecutives frames in a deth image frame

    Returns
    -------
    frame : rgb numy array
        The frame returned is the dense optical flow image

    '''
    mask = np.zeros_like(frame)
    mask[..., 1] = 255
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, 
                                       None,
                                       0.5, 3, 15, 3, 5, 1.2, 0)
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    frame = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    
    return frame

    
def get_gray_vid(rep, name, depth=False, OFI=False):
    if depth:
        vid_depth = []
    if OFI:
        vid_ofi = []
    vid_gray = []
    frames = get_frames_from_vid(rep, name)
    if OFI:
        i =0
        prev_frame = None
        for frame in frames:
            if i == 0:
                ofi = convert_frame_to_dense_OFI(frame, frame)
            else:
                ofi = convert_frame_to_dense_OFI(frame, prev_frame)
            prev_frame = frame
            gray_ofi = cv2.cvtColor(ofi, cv2.COLOR_BGR2GRAY)
            gray_ofi = degrade_frame(gray_ofi, 4,)
            #print("addind ofi")
            vid_ofi.append(gray_ofi)
            i+=1
    if depth:
        depth_frames = get_frames_from_vid(rep+'Depth/', name)
        for frame in depth_frames:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #print(frame.shape)
            vid_depth.append(degrade_frame(frame, 4,))
    for frame in frames:
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #print(gray.shape)
        #degradation de l'image
        gray = degrade_frame(gray, 4,)
        vid_gray.append(gray)
    if depth and not OFI:
        return vid_gray, vid_depth
    if OFI and not depth:
        return vid_gray, vid_ofi
    if depth and OFI:
        #print("returning depth and ofi")
        return vid_gray, vid_depth, vid_ofi
    return vid_gray

def get_frames_from_vid(rep, name):
   # print("entring get_frames_from_vid")
    list_frames = []
    #print(rep+name)
    cap = cv2.VideoCapture(rep+name)
    if (cap.isOpened()== False):
        print("Error opening video stream or file:\nfile location is {}".format(rep+name))
    while cap.isOpened():
        ret, frame = cap.read()
       # print(ret)
       # print(frame)
        if not ret:
            break
        list_frames.append(frame) 
    cap.release()
    #read the vid
    #save each frame
    return list_frames

def degrade_frame(frame,step_degradation, return_same=False):
    
    '''
    Call after converting in gray scaled
    '''
    if return_same:
        return frame
    frame = np.array(frame)
    new_shape = [round(frame.shape[0]/step_degradation), round(frame.shape[1]/step_degradation)]
    new_frame =np.array([frame[i,j] for i in range(0,frame.shape[0],step_degradation) for j in range(0,frame.shape[1],step_degradation)]).reshape(new_shape[0], new_shape[1]) 
    return new_frame
