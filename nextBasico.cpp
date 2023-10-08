#include <Arduino.h>
#include <HCSR04.h>
#include <WiFi.h>

// variáveis referentes ao sensor de ultrassom
const byte triggerPin = 26;
const byte echoPin = 25;
const int maxCm = 405;

UltraSonicDistanceSensor sensorUltrassom(triggerPin, echoPin, maxCm);

// variáveis referentes ao sensor infravermelho
const byte sensorInfra = 33;

// leds
const byte r = 15;
const byte g = 4;
const byte b = 5;

void setup()
{
  Serial.begin(9600);

  pinMode(sensorInfra, INPUT);
  pinMode(32, INPUT);
  pinMode(15, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  delay(500);

  digitalWrite(LED_BUILTIN, HIGH);

  float distance = sensorUltrassom.measureDistanceCm();
  bool infra = !digitalRead(sensorInfra);

  Serial.println("Distância: " + String(distance));
  Serial.println("Infra: " + String(infra));
  Serial.println("Infra2: " + String(!digitalRead(32)));
  analogWrite(r, 255 - map(distance, 19, 80, 0, 255));
  analogWrite(g, map(distance, 19, 80, 0, 255));
}

// tirar variáveis de dentro do loop