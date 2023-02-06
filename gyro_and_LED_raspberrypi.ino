#include <usbdrv.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#define RQ_GET_GYRO 0
#define RQ_SET_LED 1

MPU6050 mpu;

int16_t ax, ay, az;
int16_t gx, gy, gz;
int valx , valy , valz;
char rd;
int prevVal;
int led = PIN_PC0,buzzer=PIN_PC1;
int pin11 = 11 , pin10 = 10 ;
int val1 , val2 ;
int valgy1 = 0 , valgy2 = 0;

usbMsgLen_t usbFunctionSetup(uint8_t data[8])
{
  usbRequest_t *rq = (usbRequest_t*)data;
  static uint8_t gyro_state;

  if (rq->bRequest == RQ_GET_GYRO)
  {
    if (valx < 100||valy < 100){
      digitalWrite(buzzer,LOW); 
      gyro_state = 1;
    }
    else{
      digitalWrite(buzzer,HIGH);
      gyro_state = 0;
    }

    usbMsgPtr = (uint8_t*) &gyro_state;
    return sizeof(gyro_state);
  }
  
  else if (rq->bRequest == RQ_SET_LED)
  {
    uint8_t led_val = rq->wValue.bytes[0];
    if(led_val == 0)
      digitalWrite(led, LOW);
    else if(led_val == 1)
      digitalWrite(led,HIGH);
    return 0; 
  }
  return 0; 
}

void setup()
{
    Wire.begin();
    mpu.initialize();
    pinMode(led,OUTPUT);
    pinMode(buzzer,OUTPUT);
    digitalWrite(led,LOW);
    usbInit();

    usbDeviceDisconnect();
    delay(300);
    usbDeviceConnect();
}

//////////////////////////////////////////////////////////////////////
void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); 
  valx = map(ax, -17000, 17000, 0, 179);
  valy = map(ay, -17000, 17000, 0, 179);
  usbPoll();
  delay(50);
}
