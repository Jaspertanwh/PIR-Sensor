const int led = 7; // Led positive terminal to the digital pin 7
const int sensor = 5; // Signal pin of sensor to digital pin 5
bool state = LOW;
int val = 0;

void setup() {
  // Void setup is run only once after each powerup or reset of the Arduino board.
  pinMode(led, OUTPUT); // Led is determined as an output here
  pinMode(sensor, INPUT); // PIR motion sensor is determined as an input here
  Serial.begin(9600);
}

void loop() {
  // Void loop is run over and over and consists of the main program.
  val = digitalRead(sensor);
  if (val == HIGH) {
    digitalWrite(led, HIGH);
    delay(500); // Delay of led is 500 ms
    
    if (state == LOW) {
      Serial.println("Motion detected");
      state = HIGH;
    }
  } else {
    digitalWrite(led, LOW);
    delay(500);

    if (state == HIGH) {
      Serial.println("The action/motion has stopped");
      state = LOW;
    }
  }
}
