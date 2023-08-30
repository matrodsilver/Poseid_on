#include <Arduino.h>
#include <HCSR04.h>
#include <WiFi.h>

// variáveis referentes ao sensor de ultrassom
const byte triggerPin = 26;
const byte echoPin = 25;
const int maxCm = 405;

UltraSonicDistanceSensor sensorUltrassom(triggerPin, echoPin, maxCm);

// variáveis referentes ao sensor infravermelho
const byte sensorInfra = 32;

// variáveis da biblioteca de wifi
WiFiClient client;

String thingSpeakAddress = "HL7ZT6N5CYHFTCJY";
String tsfield1Name;
String request_string;
String apiKey = "HL7ZT6N5CYHFTCJY";

void setup()
{
  Serial.begin(9600);

  pinMode(sensorInfra, INPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("MatRodNet", "11etrinta");
  while ((!(WiFi.status() == WL_CONNECTED)))
  {
    delay(300);
    Serial.print(".");
  }
  Serial.println("Conectado");
}

void loop()
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(25);

  if (client.connect("api.thingspeak.com", 80))
  {
    int teste = random(0, 9);
    float distance = sensorUltrassom.measureDistanceCm();
    bool infra = !digitalRead(sensorInfra);

    Serial.println("Conectado com sucesso B^)");
    Serial1.println("teste:" + String(teste));
    Serial.println("Distância: " + String(distance));
    Serial.println("Infra: " + String(infra));

    request_string = thingSpeakAddress;
    request_string += "&field1=";
    request_string += teste;
    request_string += "&field2=";
    request_string += distance;
    request_string += "&field3=";
    request_string += infra;

    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(request_string.length());
    client.print("\n\n");
    client.print(request_string);
  }
  else
  {
    Serial.println("Deu ruim fml");
  }
  digitalWrite(LED_BUILTIN, LOW);
  delay(20000);
}

// tirar variáveis de dentro do loop