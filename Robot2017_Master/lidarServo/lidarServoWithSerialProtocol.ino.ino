#include <Adafruit_PWMServoDriver.h>

#include <LIDARLite.h>

#include <Wire.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver servo = Adafruit_PWMServoDriver();

#define min 150
#define max 600

uint8_t servonum = 0;

unsigned long serialdata;
int inbyte;
int servoPose;
int servoPoses[80] = {};
int attachedServos[80] = {};
int servoPin;




LIDARLite myLidarLite;

void setup()
{
  Serial.begin(115200);
  myLidarLite.begin();
  myLidarLite.changeAddress(0x66,false);
  servo.begin();
  servo.setPWMFreq(60);
  
  yield();
}

void loop()
{
  getSerial();
  switch(serialdata)
  {
  case 1:
    {
       getSerial();
      switch (serialdata)
      {
        case 1:
        {
           //servo position
           getSerial();
           servoPin = serialdata;
           Serial.println(servoPoses[servoPin]);
           break;
        }
        case 2:
        {
           //servo scan
           getSerial();
           servoPin = serialdata;
           getSerial();
           servoPose = serialdata;
           if (attachedServos[servoPin] == 1)
           {
             scan();
             Serial.println(getDistance());
           }
           if (attachedServos[servoPin] == 0)
           {
             
           }
           servoPoses[servoPin] = servoPose;
           break;
        }
        case 3:
        {
          //servo stop
          getSerial();
          servoPin = serialdata;
          if (attachedServos[servoPin] == 1)
          {
            servoStop();
            attachedServos[servoPin] = 0;  
          }
        }
      }
    break;
    }
  }
}

long getSerial()
{
  serialdata = 0;
  while (inbyte != '/')
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != '/')
    {
      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000;
  pulse /= pulselength;
  Serial.println(pulse);
  servo.setPWM(n, 0, pulse);
}


void scan()
{
  for(uint16_t pulselen = min; pulselen < max; pulselen++){
    servo.setPWM(servonum, 0, pulselen);
    Serial.println(pulselen);
  }
  delay(500);
  for(uint16_t pulselen = max; pulselen > min; pulselen--){
    servo.setPWM(servonum, 0, pulselen);
    Serial.println(pulselen);
  }
  delay(500);

}

void servoStop()
{
  servo.setPWM(servonum, 0, 0);
}

int getDistance()
{
  int dist = myLidarLite.distance(true,true,0x66);
  //Serial.println(myLidarLite.distance(true,true,0x66))
  return dist;
}  



