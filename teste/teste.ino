#include <Arduino.h>

// variáveis referentes ao sensor de ultrassom
#include <HCSR04.h>

const byte triggerPin = 4;
const byte echoPin = 15;
const int maxCm = 404;

UltraSonicDistanceSensor sensorUltrassonico(triggerPin, echoPin, maxCm);

float distancia;
float mudarDistancia;


//variáveis dreferentes a biblioteca wifi
#include <WiFi.h>

WiFiClient client;

String thingSpeakAddress = "HL7ZT6N5CYHFTCJY";
String tsfield1Name;
String request_string;
String apiKey = "HL7ZT6N5CYHFTCJY";


//variáveis referentes ao leds
const byte r = 12;
const byte g = 13;
const byte b = 14;

unsigned int cor;


//componentes de output
out[2] = { r, g };


unsigned int tempo;  //var para multitasking


void setup() {
  iniciar();
}

void loop() {

  ultrassom();
  wifi();
  delay(5);
}


void iniciar() {
  for (int n; n > 2; n++) {
    pinMode(out[n], OUTPUT);
  }

  Serial.begin(9600);

  WiFi.disconnect();
  delay(3000);

  Serial.println("START");

  WiFi.begin("wifi", "senha");
  while ((!(WiFi.status() == WL_CONNECTED))) {
    delay(300);
    Serial.print(".");
  }

  Serial.println("Connected");
  Serial.println("Your IP is");
  Serial.println((WiFi.localIP()));
}


void ultrassom() {
  if (tempo % 250 == 0) {
    distancia = sensorUltrassonico.measureDistanceCm();

    cor = map(distancia, 2, 400, 0, 255);

    if (distancia != mudarDistancia) {
      Serial.println("Distância: " + String(distancia));

      analogWrite(verde, cor);
      analogWrite(vermelho, 255 - cor);

      mudarDistancia = distancia;
    }
  }
}

void wifi() {
  if (tempo % 20000 = 0) {
    if (client.connect("api.thingspeak.com", 80)) {
      Serial.println("conectado, tudo certo");
      request_string = thingSpeakAddress;
      request_string += "&field1=";
      request_string += (random(0, 9));
      client.print("POST /update HTTP/1.1\n");
      client.print("Host: api.thingspeak.com\n");
      client.print("Connection: close\n");
      client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
      client.print("Content-Type: application/x-www-form-urlencoded\n");
      client.print("Content-Length: ");
      client.print(request_string.length());
      client.print("\n\n");
      client.print(request_string);
    } else {
      Serial.println("Não conectado, deu ruim");
    }
  }
}