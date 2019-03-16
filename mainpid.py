import serial
import time
import datetime
import camera

import cv2

# import CSP

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400, timeout=0.5)

aim_speed = 1
aim_angle = 90

speed_p = 10
speed_i = 1

angle_error_sum = 0
angle_error_last_time = 0


speed_turn_left = 1.5
speed_turn_right = 1.5

time_each_loop = 100


def GetArdunaldata():

    back = None
    # getstr = ser.read_all()
    getstr = ser.read_all().decode("utf-8")
    # print("------------------------")
    # print(getstr)
    strpart = getstr.split('\r\n')
    # sp = str1.split('\t\n')
    # sp_use = sp[-2]
    # speed = float(sp_use)/100
    if len(strpart) > 1:
        left_speed = int(strpart[0].split(' ')[0])
        right_speed = int(strpart[0].split(' ')[1])
        speed = [left_speed, right_speed]
        # speed = float(str_speed)
    else:
        speed = [-1, -1]
    return getstr, speed


def GetCPUdata():
    angle_error, distance_error = 0, 0
    # csp.main()
    return angle_error, distance_error


def ControlAlgorithm(speed, distance_errIor, angle_error, left_pwm, right_pwm):
    # left_pwm,right_pwm = 0,0
    global angle_error_sum
    # speed_output = distance_error * speed_p
    # angle_output = angle_error * angle_p

    # left_pwm = speed + .  + angle_error
    # right_pwm = speed + speed_output - angle_error
    # print('distance_errIor')
    # print(distance_errIor)
    angle_p = 0.10
    angle_i = 0.000001

    angle_error_sum += angle_error

    if angle_error_sum > 110:
        angle_error_sum =110
    if angle_error_sum < -110:
        angle_error_sum = -110
    #pidout需要在外面进行定义
    pidout = 0
    if distance_errIor > -200 and distance_errIor < 200:

        pidout = angle_error * angle_p + angle_error_sum * angle_i

        if distance_errIor > 0:
            left_pwm, right_pwm = 30.3-pidout, 31+pidout
        else :
            left_pwm, right_pwm = 0,0

    else:
        left_pwm, right_pwm = 0, 0

    print("error:{}\tsumerror:{}\t pidout:\t{}\trightpwm:{}\tleftpwn:{}\t".format(
        angle_error, angle_error_sum, pidout, left_pwm, right_pwm))
    angle_error_last_time = angle_error
    return left_pwm, right_pwm


def SendArdunaldata(left_pwm, right_pwm):
    # ser.write("c".encode('utf-8'))
    # ser.write(left_pwm.encode('utf-8'))
    # ser.write(right_pwm.encode('utf-8'))

    a = int(left_pwm/100*250)
    b = int(right_pwm/100*250)

    if a > 80:
        a = 80
    if a < 0:
        a = 0

    if b > 80:
        b = 80
    if b < 0:
        b = 0
    # b= 80
    sss = '{}{}{}{}{}{}n'.format(
        a//100, a//10 % 10, a % 10, b//100, b//10 % 10, b % 10).encode('utf-8')
    # print("sss",sss)
    ser.write(sss)
    # ser.write('080080\t\n'.encode('utf-8'))

    return sss


def main(cap):
    time.sleep(0.01)
    left_pwm, right_pwm = 0, 0
    while 1:

        # 
        time1 = (int(round(time.time() * 1000)))
        # current_distance,current_angle = camera.redRecognition()
        getstr, current_speed = GetArdunaldata()

        # current_speed = 0
        # 读取距离和角度
        start = datetime.datetime.now()
        current_distance, current_angle = camera.redRecognition(cap)
        end = datetime.datetime.now()
        time5 = (end - start).microseconds
        # print('time:',time5)

        # current_distance,current_angle = [0,0]

        error_angle = current_angle
        error_distance = current_distance-50

        # 生成控制信号
        left_pwm, right_pwm = ControlAlgorithm(
            current_speed, error_distance, error_angle, left_pwm, right_pwm)
        # 发送控制信号
        send = SendArdunaldata(left_pwm, right_pwm)

        # 记录当前时间
        time2 = (int(round(time.time() * 1000)))

        # 时间控制
        time_use = time2-time1
        time_sleep = abs(time_each_loop - time_use)
        time.sleep(time_sleep/1000)

        print('get:{}\t send:{}\t time_use:{}\t speed:{}\t angle:{}\t dis:{}\t left_pwm:{}\t right_pwm:{}'.format(
            getstr, send, time_use, current_speed, current_angle, current_distance, left_pwm, right_pwm))

    ser.close()


def PutPwm():
    pwma = 35  # 百分比
    pwmb = 35

    time.sleep(0.1)
    while 1:

        # 记录当前时间
        time1 = (int(round(time.time() * 1000)))

        # 从mcu读取数据
        getstr, speed = GetArdunaldata()
        current_speed = 0
        # current_distance,current_angle = camera.redRecognition()
        current_distance, current_angle = 0, 0
        error_angle = current_angle
        error_distance = current_distance-100

        # left_pwm,right_pwm = ControlAlgorithm(current_speed,current_distance,current_angle)
        left_pwm, right_pwm = ControlAlgorithm(
            current_speed, error_distance, error_angle)
        send = SendArdunaldata(pwma, pwmb)
        time2 = (int(round(time.time() * 1000)))

        time_use = time2-time1
        time_sleep = abs(time_each_loop - time_use)
        # print('timesleep',time_sleep)
        time.sleep(time_sleep/1000)

        print('get:{}\t send:{}\t time_use:{}\t speed:{}\t angle:{}\t dis:{}\t left_pwm:{}\t right_pwm:{}'.format(
            getstr, send, time_use, current_speed, current_angle, current_distance, left_pwm, right_pwm))

    cap.release() 
    cv2.destroyAllWindows()
    ser.close()


if __name__ == '__main__':
    # PutPwm()
    cap = cv2.VideoCapture(0)
    main(cap)
