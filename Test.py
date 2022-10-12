#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:32:50 2022

@author: nathan


this file is created to test the model on a single video
note that the video must have a rbg part and a depth map part
"""
import os
from utils import get_gray_vid
from tensorflow import keras
import numpy as np
import shutil
import cv2

#the first step is to get the X matrix

#vid_rep = "_the location_of_the_vid(relatif_path without the name of the vid and without the / at the end)"
vid_rep = "TestModel"
#vid_name = "_the_name_of_the_video_"  

#vid_name = "2_11_3_NORMAL.avi"
#vid_name = "3_6_3_NORMAL.avi"
#vid_name = "6_15_1_NORMAL.avi"
vid_name = "7_14_5_NORMAL.avi"

# the depth of the image must be in a Folder named Deth and must have the same name than the rgb vid

#test if the Depth folder exist

list_mvt = ["Repos - Rest", "Suffoquer - Suffocate", "Chuter - Fall down", "Convulser - Convulse", "S'asseoir - Sit", "Se coucher - Lie on bed", "Tousser - cough", "Vomir - Vomit"]

if os.path.exists(vid_rep+"/"+"Depth"):
    print("loading the model...")
    loaded_model = keras.models.load_model("model92_28V1_0_0.h5")
    print("____SUMMARY OF THE MODEL_____")
    print(loaded_model.summary())
    print("loading the data...")
    X = get_gray_vid(vid_rep+'/',vid_name, depth=True, OFI=True)
    X = np.array(X)
    print(X.shape)
    X = X.reshape(1,3,90,120,160,1)
    print("Making the prediction...")
    y_pred=loaded_model.predict(X)
    y_classes = y_pred.argmax(axis=-1)
    print("y_classes: {}".format(y_classes))
    mvt = list_mvt[y_classes[0]]
    print("mvt: {}".format(mvt))
    shutil.copy(vid_rep+"/"+vid_name, vid_rep+"/"+mvt+"__"+vid_name)
else:
    print("Depth folder doesn't exist, please create it and put the depth map inside, with the same name than the rgb vid")
    

cap = cv2.VideoCapture(vid_rep+"/"+mvt+"__"+vid_name)

# We need to check if camera
# is opened previously or not
if (cap.isOpened() == False): 
    print("Error reading video file")
  
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)
   
# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.avi' file.
result = cv2.VideoWriter(mvt+'.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, size)
  
while(True):
      
    # Capture frames in the video
    ret, frame = cap.read()
    if ret:
  
        # describe the type of font
        # to be used.
        font = cv2.FONT_HERSHEY_SIMPLEX
      
        # Use putText() method for
        # inserting text on video
        cv2.putText(frame, 
                    mvt, 
                    (50, 50), 
                    font, 1, 
                    (255, 0, 0), 
                    2, 
                    cv2.LINE_4)
        result.write(frame)
        # Display the resulting frame
        cv2.imshow('video', frame)
      
        # creating 'q' as the quit 
        # button for the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
      
# release the cap object
cap.release()
result.release()
# close all windows
cv2.destroyAllWindows()

#the Labeled video is saved in the root directory