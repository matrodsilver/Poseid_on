#include <Arduino.h>

#include <WiFi.h>

WiFiClient client;

String thingSpeakAddress = "HL7ZT6N5CYHFTCJY";
String tsfield1Name;
String request_string;
String apiKey = "HL7ZT6N5CYHFTCJY";

int r = 12;
int g = 13;
int b = 14;

out[2] = { r, g };

unsigned int tempo;

void setup() {
  iniciar();
}

void loop() {
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
    delay(5000);
  }
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