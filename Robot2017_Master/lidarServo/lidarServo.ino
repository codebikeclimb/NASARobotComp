
#include <Wire.h>
#include <LIDARLite.h>
#include <Servo.h>


Servo myservo; // create servo object to control a servo
int pos = 0; // variable to store the servo position
LIDARLite myLidarLite;


void setup() {
  Serial.begin(115200);
  myLidarLite.begin();
  myservo.attach(9); // attaches the servo on pin 9 to the servo object
 
  // We assign the sensor the address of 0x66, and the false flag
  // tells the sensor to stop responding to 0x62

  myLidarLite.changeAddress(0x66,false);
}

void loop() {

  for(pos = 0; pos < 180; pos += 1) // goes from 0 degrees to 180 degrees
  { // in steps of 1 degree
  myservo.write(pos); // tell servo to go to position in variable 'pos'
  Serial.println(myLidarLite.distance(true,true,0x66));
  delay(15); // waits 15ms for the servo to reach the position
  }
  for(pos = 180; pos>=1; pos-=1) // goes from 180 degrees to 0 degrees
  {
  myservo.write(pos); // tell servo to go to position in variable 'pos'
  Serial.println(myLidarLite.distance(true,true,0x66));
  delay(15); // waits 15ms for the servo to reach the
  }
  // In order to talk to the sensor at the new address, we need
  // to set that value in the distance function. The first two "true"
  // bools tell the function to use its default values for dc stabilization
  // and reference

 //Serial.println(myLidarLite.distance(true,true,0x66));
}
