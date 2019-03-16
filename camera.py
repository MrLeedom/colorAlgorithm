#!/usr/bin/python3.6
# -*- encoding: utf-8 -*-
'''
   @Author:leedom

   Created on Sat Mar 16 08:33:05 2019
   Description:存放三个方法,分别对应着:
                    1.调用摄像头读取,调用每一帧,将其进行处理,实时展示
                    2.调用摄像头,录视频,保存到指定路径
                    3.从视频中抓取每一帧,并进行处理,将结果保存到视频文件中
   License: (C)Copyright 2019
'''
import cv2 
import numpy as np 
import sample

####################################  原始版本,未与视频进行交互  #########################################################3
def redRecognition():
    cap = cv2.VideoCapture(1) 

    while(1):
        ret,frame = cap.read()
        d = sample.Detect(frame)
        distance, angle = d.img_process_main(count)

        #waitKey(int delay)其中delay<=0时表示无限期等待,而delay>0是表示等待的毫秒数
        if cv2.waitKey(40) & 0xFF == ord('q'): 
            break
    cap.release() 
    cv2.destroyAllWindows()
    return distance, angle 

#####################################  调用摄像头拍视频,输出至文件  ##########################################################
def redRecognition_toVideo():
    cap = cv2.VideoCapture(0) 
    ret = True

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    out = cv2.VideoWriter('camera3.mp4', fourcc, fps, size, True)

    while(ret): 
        ret,frame = cap.read()

        cv2.imshow("Capture_Test", frame) 
        #每一帧的大小跟之前的视频文件定义有区别,所以需要转一下大小 
        frame = cv2.resize(frame, (int(size[0]), int(size[1])))
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    cap.release() 
    cv2.destroyAllWindows()

##########################  读取视频,测试算法的性能  ########################################################################
def redRecognition_fromVideo():
    cap = cv2.VideoCapture('video.mp4')   #读视频
    ret = True

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    
    out = cv2.VideoWriter('camera4.mp4', fourcc, fps, size, True)
    while(ret): 
        ret,frame = cap.read()
        cv2.imshow("Capture_Test", frame)  
 
        d = sample.Detect(frame)

        distance, angle, image = d.img_process_main()
        img = cv2.resize(
            image, (int(size[0]), int(size[1])))
        cv2.putText(img, 'distance:'+str(distance)+',angle:'+str(angle),(10,20),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,255,0),1,cv2.LINE_AA)
 
        out.write(img)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        distance = 0
        angle = 0
    cap.release() 
    cv2.destroyAllWindows()
    return distance, angle 
if __name__ == '__main__':
    # redRecognition()
    # redRecognition_toVideo()
    redRecognition_fromVideo()

