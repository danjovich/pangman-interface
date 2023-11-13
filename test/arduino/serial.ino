char *input;
int inputSize = 0;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

// the loop routine runs over and over again forever:
void loop() {
  if (Serial.available()) {
    char inByte = Serial.read();
    char *newInput = (char *)malloc(++inputSize);
    if (newInput == nullptr) {
      Serial.println("malloc failed");
      return;
    }

    for (int i = 0; i < inputSize; i++) {
      newInput[i] = input[i];
    }
    input = newInput;

    input[inputSize - 1] = inByte;

    input[inputSize] = '\0';
  }

  if (input[0] == 'W' && input[1] == 'i' && input[2] == 'n') {
    Serial.println(input);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
  }
}
