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
const byte sensorInfra = 33;
const byte sensorInfra2 = 32;

bool infra;
bool infra2;

// variáveis referentes ao sensor de nível de água
const byte sensorAgua = 35;

float agua;

// variáveis referentes ao led
const byte r = 15;
const byte g = 4;
const byte b = 5;

// variáveis da biblioteca de wifi
WiFiClient client;

String thingSpeakAddress = "HL7ZT6N5CYHFTCJY";
String apiKey = "HL7ZT6N5CYHFTCJY";
String tsfield1Name;
String request_string;

// listas de componentes
int out[3] = {r, g, b};
int inp[3] = {sensorInfra, sensorInfra2, sensorAgua}; // de ultrassom já é inicializado pela biblioteca

unsigned int tempo; // variável para marcação do tempo

/*Setup*/

void setup()
{
  Serial.begin(9600); // iniciando serial

  // conexão do wifi
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

  // prontificação
  for (int n = 0; n < 3; n++) // enquanto n < tamanhoDaLista out
  {
    pinMode(out[n], OUTPUT);
  }

  for (int n = 0; n < 3; n++) // enquanto n < tamanhoDaLista inp
  {
    pinMode(inp[n], INPUT);
  }
}

void loop()
{

  if (tempo % 500 == 0)
  {
    distancia = sensorUltrassom.measureDistanceCm();

    Serial.println("Distância-pré manipulação: " + String(distancia));

    if (distancia < 19)
    {
      distancia = 19;
    }
    else if (distancia > 80)
    {
      distancia = 80;
    }

    Serial.println("Distância-pós manipulação: " + String(distancia));

    analogWrite(r, 255 - map(distancia, 19, 80, 0, 255));
    analogWrite(g, map(distancia, 19, 80, 0, 255));

    if (tempo % 20000 == 0)
    {
      if (client.connect("api.thingspeak.com", 80))
      {
        digitalWrite(b, HIGH);

        infra = !digitalRead(sensorInfra);
        infra2 = !digitalRead(sensorInfra2);
        agua = analogRead(sensorAgua);
        

        Serial.println("Infra1: " + String(infra));
        Serial.println("Infra2: " + String(infra2));
        Serial.println("Nível de Água: " + String(agua));

        request_string = thingSpeakAddress;
        request_string += "&field1=";
        request_string += agua;
        request_string += "&field2=";
        request_string += distancia;
        request_string += "&field3=";
        request_string += infra;
        request_string += "&field4=";
        request_string += infra2;

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

  delay(1);
  tempo++;
}