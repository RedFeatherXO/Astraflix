int pwmPin1 = 9;  // PWM-fähiger Ausgangspin //ESP32 Supermini -> A0
int pwmPin2 = 6;  // PWM-fähiger Ausgangspin //ESP32 Supermini -> A1
int pwmPin3 = 5;  // PWM-fähiger Ausgangspin //ESP32 Supermini -> A2
int pwmPin4 = 3;  // PWM-fähiger Ausgangspin //ESP32 Supermini -> A3
int pwmValue = 255; // Variable für den PWM-Wert //ESP32 Supermini -> A4

void setup() {
  Serial.begin(9600);   // Serielle Kommunikation starten
  pinMode(pwmPin1, OUTPUT); 
  pinMode(pwmPin2, OUTPUT); 
  pinMode(pwmPin3, OUTPUT); 
  pinMode(pwmPin4, OUTPUT); 
  pinMode(A0, INPUT); 
  Serial.println("Gib einen PWM-Wert zwischen 0 und 255 ein:");
}

void loop() {
  //Serial.println(analogRead(A0)/4);
  pwmValue = analogRead(A0)/4;
  
  analogWrite(pwmPin1, pwmValue);          // 100% des Eingabewerts
  analogWrite(pwmPin2, pwmValue * 0.075);   // 75% des Eingabewerts
  analogWrite(pwmPin3, pwmValue * 0.05);    // 50% des Eingabewerts
  analogWrite(pwmPin4, pwmValue * 0.01);   // 25% des Eingabewerts
}

  /*
  if (Serial.available() > 0) {
    int inputValue = Serial.parseInt();  // Eingabe lesen und in eine Zahl umwandeln

    if (inputValue >= 0 && inputValue <= 255) {
      pwmValue = inputValue;

      // Angepasste Werte mit größerem Unterschied
      analogWrite(pwmPin1, pwmValue);          // 100% des Eingabewerts
      analogWrite(pwmPin2, pwmValue * 0.075);   // 75% des Eingabewerts
      analogWrite(pwmPin3, pwmValue * 0.05);    // 50% des Eingabewerts
      analogWrite(pwmPin4, pwmValue * 0.01);   // 25% des Eingabewerts

      Serial.print("PWM-Wert auf Pins gesetzt. Eingabe: ");
      Serial.println(pwmValue);
    } else {
      Serial.println("Ungültiger Wert! Bitte gib eine Zahl zwischen 0 und 255 ein.");
    }
  }*/
