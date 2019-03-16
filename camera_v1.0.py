import cv2 
import numpy as np 
import sample

def redRecognition(cap):
     
    ret,frame = cap.read()
    d = sample.Detect(frame)
    distance, angle = d.img_process_main(count)

    #waitKey(int delay)其中delay<=0时表示无限期等待,而delay>0是表示等待的毫秒数
    #后者表示按q键终止程序
  
    if cv2.waitKey(40) & 0xFF == ord('q'): 
        return
    return distance, angle 

if __name__ == '__main__':
    redRecognition()


'''
部分调试代码：
１．抓取五帧计算平均帧
    # ret1, frame1 = cap.read() # show a frame 
    # ret2, frame2 = cap.read() # show a frame 
    # ret3, frame3 = cap.read() # show a frame 
    # ret4, frame4 = cap.read() # show a frame 
    # ret5, frame5 = cap.read() # show a frame 

    # img1 = frame1.astype(np.float32)
    # img2 = frame1.astype(np.float32)
    # img3 = frame1.astype(np.float32)
    # img4 = frame1.astype(np.float32)
    # img5 = frame1.astype(np.float32)
    # img = (img1+img2+img3+img4+img5)/5
    # img = img.astype(np.uint8)

2．从视频中以指定帧数截取图片保存下来
    # if(count % timeF == 0): #每隔timeF帧进行存储操作
    #     cv2.imwrite('./img/'+str(600) + '.jpg',frame) #存储为图像
    count += 1
    # cv2.imshow('frame',frame)
3. timeF = 10 #视频帧计数间隔频率
'''