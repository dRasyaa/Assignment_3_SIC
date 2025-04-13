#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

#define TRIG_DEPAN 14
#define ECHO_DEPAN 27
#define TRIG_KIRI  12
#define ECHO_KIRI  13
#define TRIG_KANAN 33
#define ECHO_KANAN 32

float readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // timeout 30ms
  if (duration == 0) return -1;
  float distance = duration * 0.034 / 2;
  return distance;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_DEPAN, OUTPUT); pinMode(ECHO_DEPAN, INPUT);
  pinMode(TRIG_KIRI, OUTPUT);  pinMode(ECHO_KIRI, INPUT);
  pinMode(TRIG_KANAN, OUTPUT); pinMode(ECHO_KANAN, INPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("NeoCane 3 Sensor");
  delay(2000);
  lcd.clear();
}

void loop() {
  float depan = readDistance(TRIG_DEPAN, ECHO_DEPAN);
  float kiri  = readDistance(TRIG_KIRI, ECHO_KIRI);
  float kanan = readDistance(TRIG_KANAN, ECHO_KANAN);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("D:");
  lcd.print(depan > 0 ? String(depan, 1) + "cm" : "Err");
  lcd.print(" K:");
  lcd.print(kiri > 0 ? String(kiri, 1) + "cm" : "Err");

  lcd.setCursor(0, 1);
  lcd.print("Ka:");
  lcd.print(kanan > 0 ? String(kanan, 1) + "cm" : "Err");

  delay(700); // Gak terlalu cepat, biar LCD bisa kebaca
}
