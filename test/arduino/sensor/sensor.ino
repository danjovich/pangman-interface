int pinTrigger = 2;
int pinEcho = 3;
float echoElapsed = 0;
const float soundSpeed_mpus = 0.000340;
int angle = 20;
bool increaseAngle = true;
char data[4];

void setup() {
  pinMode(pinTrigger, OUTPUT);
  digitalWrite(pinTrigger, LOW);
  pinMode(pinEcho, INPUT);
  Serial.begin(115200);
  delay(100);
}

void loop() {
  activateTrigger();
  echoElapsed = pulseIn(pinEcho, HIGH);

  toThreeChars(angle);
  Serial.print(data);
  Serial.print(",");
  toThreeChars((int)calculateDistance(echoElapsed * 100));
  Serial.print(data);
  Serial.print("#");

  updateAngle();
  delay(500);
}

void activateTrigger() {
  digitalWrite(pinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrigger, LOW);
}

float calculateDistance(float tempo_us) {
  return ((tempo_us * soundSpeed_mpus) / 2);
}

void toThreeChars(int value) {
  data[0] = (value / 100) + '0';
  value -= (value / 100) * 100;
  data[1] = value / 10 + '0';
  value -= (value / 10) * 10;
  data[2] = value + '0';
  data[3] = '\0';
}

void updateAngle() {
  if (increaseAngle) {
    angle += 20;
  } else {
    angle -= 20;
  }

  increaseAngle =
      (increaseAngle && angle < 160) || (!increaseAngle && angle == 20);
}