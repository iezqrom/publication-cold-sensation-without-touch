#include <Servo.h> // for the servo motor

// create objects
Servo myServo; // servo motor

//// SERVO variables
int angle; // angle we want the servo to move
int state;

// import libraries

//orange- signal
//red- vcc
//brown- ground

void setup() {
  Serial.begin(9600);
  myServo.attach(9); // SERVO: Telling arduino to what pin the servo is connected to
  
  angle = 0;
  myServo.write(angle);
  
}
 
void loop() {
 
  ////////////////////////////////////////////////////////
  ////////////// Servo motor///// ////////////////////////
  ////////////////////////////////////////////////////////

  if(Serial.available()){
   state = Serial.read(); // we read the desired state of the shutter from Python
   Serial.println(state);
   if (state == 0){
    angle = 180;
    myServo.write(angle);
    delay(1);

    }
    else if(state == 1){
      angle = 0;
      myServo.write(angle);
      delay(1);

  }}
}
