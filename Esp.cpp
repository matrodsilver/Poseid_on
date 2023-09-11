#include <Arduino.h>
#include <HCSR04.h>
#include <WiFi.h>

// variáveis referentes ao sensor de ultrassom
const byte triggerPin = 26;
const byte echoPin = 25;
const int maxCm = 404;

UltraSonicDistanceSensor sensorUltrassom(triggerPin, echoPin, maxCm);

float distancia;

// variáveis referentes ao sensor infravermelho
const byte sensorInfra = 32;

bool infra;

// variáveis referentes ao led
const byte r = 15;
const byte g = 4;
const byte b = 5;

byte intensidadeDaCor;

// variáveis da biblioteca de wifi
WiFiClient client;

String thingSpeakAddress = "HL7ZT6N5CYHFTCJY";
String tsfield1Name;
String request_string;
String apiKey = "HL7ZT6N5CYHFTCJY";

// listas de componentes
int out[3] = {r, g, b}; //, 4] = {r, g, b, LED_BUILTIN};
int in[1] = {sensorInfra};

unsigned int tempo; // variável para marcação do tempo

/*builtin*/

void setup()
{
  // conexão do wifi
  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("PAJOSIL2", "Margarida1951");
  while ((!(WiFi.status() == WL_CONNECTED)))
  {
    delay(300);
    Serial.print(".");
  }
  Serial.println("Conectado");

  // prontificação
  Serial.begin(9600);

  for (int n = 0; n < 3; n++)
  {
    pinMode(out[n], OUTPUT);
  }

  for (int n = 0; n < 1; n++)
  {
    pinMode(in[n], INPUT);
  }
}

void loop()
{
  if (digitalRead(sensorInfra) == LOW)
  {
    analogWrite(r, 0);
    analogWrite(g, 0);
    analogWrite(b, 0);

    Serial.println("detectado");

    for (int n = 0; n < 255; n++)
    {
      analogWrite(r, n);
      delay(10);
    }
    analogWrite(r, 0);
    delay(10);

    for (int n = 0; n < 255; n++)
    {
      analogWrite(g, n);
      delay(25);
    }
    analogWrite(g, 0);
    delay(25);

    for (int n = 0; n < 255; n++)
    {
      analogWrite(b, n);
      delay(25);
    }
    analogWrite(b, 0);
    delay(25);
  }

  else
  {
    if (tempo % 100 == 0)
    {
      distancia = sensorUltrassom.measureDistanceCm();
      infra = !digitalRead(sensorInfra);

      Serial.println("Distância: " + String(distancia));

      analogWrite(r, 255 - map(distancia, 19, 100, 0, 255));
      analogWrite(g, map(distancia, 19, 100, 0, 255));

      if (tempo % 20000 == 0)
      {
        if (client.connect("api.thingspeak.com", 80))
        {
          digitalWrite(b, HIGH);

          request_string = thingSpeakAddress;
          request_string += "&field1=";
          request_string += random(0, 400);
          request_string += "&field2=";
          request_string += distancia;
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

          Serial.println("Enviado com sucesso B^)");

          digitalWrite(b, LOW);
        }
        else
        {
          Serial.println("Deu ruim fml");

          delay(500);
          tempo += 500;
        }
      }
    }
  }

  delay(1);
  tempo++;
}