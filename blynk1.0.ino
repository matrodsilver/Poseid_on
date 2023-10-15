//variaveis blynk
#define BLYNK_TEMPLATE_ID "TMPL2KONIB4C3"
#define BLYNK_TEMPLATE_NAME "projeto 1"
#define BLYNK_AUTH_TOKEN "B6KZpnTAt6jPWdWNAV4MqJfh5shFlEiM"
#define BLYNK_PRINT Serial
#include <Arduino.h>
#include <HCSR04.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
// senha de wifi utilizado
char ssid[] = "nome da rede";//trocar para utilizar
char pass[] = "senha da rede";//trocar para utilizar
// variáveis referentes ao sensor de ultrassom
const byte triggerPin = 26;
const byte echoPin = 25;

const byte triggerPin2 = 21;
const byte echoPin2 = 19;

const int maxCm = 404;

UltraSonicDistanceSensor sensorUltrassom(triggerPin, echoPin, maxCm);
UltraSonicDistanceSensor sensorUltrassom2(triggerPin2, echoPin2, maxCm);

float distancia;
float distancia2;

float mudarDistancia;
float mudarDistancia2;

// variáveis referentes ao sensor infravermelho
const byte sensorInfra = 33;
const byte sensorInfra2 = 32;

bool infra;
bool infra2;

bool mudarInfra;
bool mudarInfra2;

// variáveis referentes ao sensor de nível de água
const byte sensorAgua = 35;

float agua;

float mudarAgua;

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
  WiFi.begin(ssid, pass);
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
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);//inicializa o blynk
}

void loop()

{

  if (tempo % 500 == 0)
  {
    distancia = sensorUltrassom.measureDistanceCm();
    distancia2 = sensorUltrassom2.measureDistanceCm();

    if (distancia != mudarDistancia)
    {
      Serial.println("Distância-pré manipulação: " + String(distancia));

      mudarDistancia = distancia;
    }
    if (distancia2 != mudarDistancia2 && distancia2 > 19)
    {
      Serial.println("Distância2-pré manipulação: " + String(distancia2));

      mudarDistancia2 = distancia2;
    }

    if (distancia < 19)
    {
      distancia = 19;
    }
    else if (distancia > 57)
    {
      distancia = 57;
    }

    if (distancia2 < 19)
    {
      distancia2 = 19;
    }
    else if (distancia2 > 57)
    {
      distancia2 = 57;
    }

    if (distancia != mudarDistancia)
    {
      Serial.println("Distância-pós manipulação: " + String(distancia));

      mudarDistancia = distancia;
    }

    if (distancia2 != mudarDistancia2 && distancia2 > 19)
    {
      Serial.println("Distância2-pós manipulação: " + String(distancia2));

      mudarDistancia2 = distancia2;
    }

    analogWrite(r, 255 - map(distancia, 19, 57, 0, 255));
    analogWrite(g, map(distancia, 19, 57, 0, 255));

    if (tempo % 20000 == 0)
    {
      if (client.connect("api.thingspeak.com", 80))
      {
        digitalWrite(b, HIGH);

        infra = !digitalRead(sensorInfra);
        infra2 = !digitalRead(sensorInfra2);
        agua = analogRead(sensorAgua);

        if (infra != mudarInfra)
        {
          Serial.println("Infra: " + String(infra));

          mudarInfra = infra;
        }
        if (infra2 != mudarInfra2)
        {
          Serial.println("Infra2: " + String(infra2));

          mudarInfra2 = infra2;
        }
        if (agua != mudarAgua)
        {
          Serial.println("Nível de Água: " + String(agua));

          mudarAgua = agua;
        }

        request_string = thingSpeakAddress;
        request_string += "&field1=";
        request_string += agua;
        request_string += "&field2=";
        request_string += distancia;
        request_string += "&field3=";
        request_string += infra;
        request_string += "&field4=";
        request_string += infra2;
        request_string += "&field5=";
        if (distancia2 > 19)
        {
          request_string += distancia2;
        }
        else
        {
          request_string += 0;
        }


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
  blynkL();
  
  delay(1);
  tempo++;
  Blynk.run();
}

void blynkL() {
  Blynk.virtualWrite(V0, mudarDistancia);
  Blynk.virtualWrite(V1, distancia2);
  Blynk.virtualWrite(V2, infra);
  Blynk.virtualWrite(V3, infra2);
  Blynk.virtualWrite(V4, agua);
}
