// Switch LED between an external LED or the on-board LED
//#define LED LED_BUILTIN
#define LED 8

void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  Serial.begin(115200);
  delay(1000);
  Serial.println("Start blinky");
}

void loop() {
  ledON();
  delay(1000);

  ledOFF();
  delay(1000);
}

void ledON() {
  Serial.println("LED ON");
  digitalWrite(LED, LOW);
}

void ledOFF() {
  Serial.println("LED OFF");
  digitalWrite(LED, HIGH);
}