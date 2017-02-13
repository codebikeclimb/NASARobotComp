#include <LIDARLite.h>

#include <Wire.h>

#include <Servo.h>

unsigned long serialdata;
int inbyte;
int servoPose;
int servoPoses[80] = {};
int attachedServos[80] = {};
int servoPin;



Servo myservo[] = {};
Servo myservo1;
LIDARLite myLidarLite;

void setup()
{
  Serial.begin(115200);
  myLidarLite.begin();
  myLidarLite.changeAddress(0x66,false);
  
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
             myservo[servoPin].write(servoPose);
           }
           if (attachedServos[servoPin] == 0)
           {
             Servo s1;
             myservo[servoPin] = s1;
             myservo[servoPin].attach(servoPin);
             myservo[servoPin].write(servoPose);
             attachedServos[servoPin] = 1;
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
            myservo[servoPin].detach();
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

void scan()
{
  myservo1.attach(9);
  for(int pos = 0; pos < 180; pos += 1) // goes from 0 degrees to 180 degrees
  { // in steps of 1 degree
  
  myservo1.write(pos); // tell servo to go to position in variable 'pos'
  
  delay(15); // waits 15ms for the servo to reach the position
  }
  for(int pos = 180; pos>=1; pos-=1) // goes from 180 degrees to 0 degrees
  {
  
  myservo1.write(pos); // tell servo to go to position in variable 'pos'
  
  delay(15); // waits 15ms for the servo to reach the
  }

}

void servoStop()
{
  myservo1.detach();
}

int getDistance()
{
  int dist = myLidarLite.distance(true,true,0x66);
  //Serial.println(myLidarLite.distance(true,true,0x66))
  return dist;
}  



