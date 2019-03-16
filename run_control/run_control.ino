// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#include "Wire.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69

#define LED_PIN 13
bool blinkState = false;

int pl=0;//左轮的pwm波输出值
int pr=0;//右轮的pwm波输出值
int i=0;//存从串口读到的单个字符的值
long r=0;//存从串口读到的整个字符串的值

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.begin();

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(38400);

    // configure Arduino LED for
    pinMode(LED_PIN, OUTPUT);

    //设置9，10口为输出口
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);

    //设置pwm波频率
    TCCR1B = TCCR1B & B11111000 | B00000001;
}

void loop() {
    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);

    //从串口读取接收到的数据进行处理并根据读出的数据输出pwm波
    while(Serial.available()>0){
      i=Serial.read();      
      if(i>47 && i<58){
        if(r>255255)
          continue;
        else
          r=r*10+i-48;
      }     
      else if(i==('n')){
        pl=r/1000;
        pr=r%1000;  
        if(pl<256 && pl>=0 && pr<256 && pr>=0){
          analogWrite(9, pl);
          analogWrite(10, pr);
          Serial.print(pl); Serial.print(' ');
          Serial.println(pr);        
        }
        else
          Serial.println("fail");
        r=0;
      }
    }
    delay(100);
}
