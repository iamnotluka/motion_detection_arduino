// deeclare input buttons
const int in_frame_led = 12;
const int motion_led = 13;

int value;
// setup everything
void setup() {
   // begin serial connection
   Serial.begin(9600); 

   // declare pins and write LOW [turn off LEDs]
   pinMode(in_frame_led, OUTPUT);
   pinMode(motion_led, OUTPUT);
   digitalWrite (in_frame_led, LOW);
   digitalWrite (motion_led, LOW);

   // print to serial to confirm connection
   Serial.println("Connection established...");
}

// do
void loop() {
   // while serial is available [python code is running]
   while (Serial.available()) {
      // read value from serial output and store it in 'value'
      value = Serial.read();
      
      // according to value perform functions
      if (value == '3') {
         digitalWrite(in_frame_led, LOW);
         digitalWrite(motion_led, LOW);
      } else if (value == '1') {
         digitalWrite(in_frame_led, HIGH);
         digitalWrite(motion_led, LOW);
      } if (value == '2') {
         digitalWrite(in_frame_led, HIGH);
         digitalWrite(motion_led, HIGH);
      }
    
   }
}
