// Реалізація аналогового компаратора на базі ESP32-S3

const int ANALOG_PIN = 1;  // GPIO1 - вхід від потенціометра
const int LED_RED   = 36;  // GPIO36 - Червоний LED, коли напруга НИЖЧЕ порогу
const int LED_WHITE  = 0;  // GPIO0 - Білий LED, коли напруга ВИЩЕ порогу

const int threshold  = 2048;  // порогове значення, що еквівалентне 1.65 В

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_WHITE, OUTPUT);

  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_WHITE, LOW);
}

void loop() {
  int value = analogRead(ANALOG_PIN);  // зчитуємо аналоговий сигнал (0..4095)

  // Компаратор: порівнюємо із threshold
  if (value > threshold) { // вхідна напруга вище за порогову
    digitalWrite(LED_WHITE, HIGH);
    digitalWrite(LED_RED, LOW);
  } else { // вхідна напруга нижче або дорівнює пороговій напрузі
    digitalWrite(LED_WHITE, LOW);
    digitalWrite(LED_RED, HIGH);
  }

  delay(100);  // 100 мс між вимірюваннями
}