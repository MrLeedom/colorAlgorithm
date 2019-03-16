整个文件夹文件分布:
urty.mp4                最终系统的运行效果图
mainpid.py              系统的主控制函数,发出串口数据,使其平稳行驶,程序的起点
camera.py               视频识别程序的入口
sample.py               颜色识别的算法部分,主要是提取到特定区域,然后将其框住     
run_control             根据串口得到的数据控制小车运动 

环境:
python 3.x
opencv-python                      3.4.3.18
numpy                              1.15.4
scikit-image(skimage)              0.14.0
pyserial                           3.4

整个程序的主文件是mainpid.py,直接运行python mainpid.py