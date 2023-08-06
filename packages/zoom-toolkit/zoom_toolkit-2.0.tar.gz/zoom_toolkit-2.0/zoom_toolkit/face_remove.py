from moviepy.editor import *
from moviepy.video.fx import resize
import sys
import cv2
import numpy as np
import cv2

class FaceRemover():
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))

    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier(haar_model)

    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_upperbody.xml')
    bodyCascade = cv2.CascadeClassifier(haar_model)

    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_eye_tree_eyeglasses.xml')
    glassCascade = cv2.CascadeClassifier(haar_model)

    blur_or_remove = 1
    def blur_right_corner_auto(image):
        if(last==None):
            last=image
        faces = faceCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        bodies = bodyCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        glasses = glassCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        detected = 0
        if(len(faces)>0 or len(bodies)>0 or len(glasses)>0):
            for(x, y, w, h) in faces:       
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            for (x, y, w, h) in bodies:
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            for(x, y, w, h) in glasses:
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            if(detected>=1 or image.mean()>50):
                frame = np.copy(image)
                frame[0:58, frame.shape[1]-100 : frame.shape[1]]=cv2.GaussianBlur(frame[0:58, frame.shape[1]-100 : frame.shape[1]],(5,5),3) 
                return frame
            else:
                return image
        else:
            return image

    def blur_right_corner(image):
        frame = np.copy(image)
        frame[0:58, frame.shape[1]-100 : frame.shape[1]]=cv2.GaussianBlur(frame[0:58, frame.shape[1]-100 : frame.shape[1]],(5,5),3)
        return frame

    def remove_right_corner_auto(image):
        if(last==None):
            last=image
        faces = faceCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        bodies = bodyCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        glasses = glassCascade.detectMultiScale(
                image,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(5, 5),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        detected = 0
        if(len(faces)>0 or len(bodies)>0 or len(glasses)>0):
            for(x, y, w, h) in faces:       
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            for (x, y, w, h) in bodies:
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            for(x, y, w, h) in glasses:
                if(y<=58 and y>=0 and image.shape[1]-100<=x and image.shape[1]>=x):
                    detected+=1
            if(detected>=1 or image.mean()>50):
                frame = np.copy(image)
                frame[0:58, frame.shape[1]-100 : frame.shape[1]]=(0,0,0) 
                return frame
            else:
                return image
        else:
            return image
            
    def remove_right_corner(image):
        frame = np.copy(image)
        frame[0:58, frame.shape[1]-100 : frame.shape[1]]=(0,0,0)
        return frame

    def face_remove(file,auto=True,start=0,end=0,one_for_blur_zero_for_remove=1):
        if(auto):
            clip_of_interest = VideoFileClip(file)

            W = clip_of_interest.w
            H = clip_of_interest.h

            print("Width x Height of clip 1 : ", end = " ") 
            print(str(W) + " x ", str(H)) 
            
            print("---------------------------------------") 

            clip_of_interest = clip_of_interest.resize((852,480))
            clip_blurred = clip_of_interest.fl_image(blur_right_corner_auto)
            
            final = concatenate_videoclips([clip_blurred]).set_audio(clip_of_interest.audio)
            final.write_videofile('modified.mp4', bitrate="3000k")
        else:
            clip_of_interest = VideoFileClip(file).subclip(start,end)

            W = clip_of_interest.w
            H = clip_of_interest.h

            print("Width x Height of clip 1 : ", end = " ") 
            print(str(W) + " x ", str(H)) 
            
            print("---------------------------------------") 

            clip_of_interest = clip_of_interest.resize((852,480))
            clip_blurred = clip_of_interest.fl_image(blur_right_corner)
            
            final = concatenate_videoclips([clip_blurred]).set_audio(clip_of_interest.audio)
            final.write_videofile('modified.mp4', bitrate="3000k")

