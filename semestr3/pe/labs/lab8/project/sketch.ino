const int KEY1 = 1;  // GPIO1 -> IN першого ключа
const int KEY2 = 37; // GPIO37 -> IN другого ключа

void setup() {
  pinMode(KEY1, OUTPUT);
  pinMode(KEY2, OUTPUT);

  digitalWrite(KEY1, LOW); // ключі закриті, LEDи вимкнені
  digitalWrite(KEY2, LOW);
}

void loop() {
  // LED1 (червоний)
  digitalWrite(KEY1, HIGH); // відкриваємо ключ №1
  delay(500);
  digitalWrite(KEY1, LOW);  // закриваємо ключ №1
  delay(500);

  // LED2 (синій)
  digitalWrite(KEY2, HIGH); // відкриваємо ключ №2
  delay(500);
  digitalWrite(KEY2, LOW);  // закриваємо ключ №2
  delay(500);
}