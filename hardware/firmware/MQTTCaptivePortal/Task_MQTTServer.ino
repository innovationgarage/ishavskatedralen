#include "mqtt_settings.h"

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------");
}

class MQTTServer : public Task {
  protected:
    void keepConnected() {

      while (!isConnected)
      {
        Serial.println("Waiting for WIFI...");
        delay(2000);
      }

      while (!client.connected()) {
        Serial.println("Connecting to MQTT...");

        client.setServer(mqttServer, mqttPort);
        client.setCallback(callback);

        if (client.connect(mqttDevice, mqttUser, mqttPassword )) {

          Serial.println("connected");
          client.publish("cathedral/out", "Hi there!");
          client.subscribe("cathedral/leds/in");

        } else {

          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
        }
      }
    }

    void setup() {

    }

    void loop() {
      keepConnected();
      client.loop();
    }
} mqttserver_task;


/*
  void ParseMode(byte r, byte g, byte b)
  {
  isConnected = true;
  for (int i = 0; i < NUM_LEDS; i++)
  {
    //strip.setPixelColor(i, 0, templates[t][i], 0);

    if (r == 255)
    {

    }
    else
    {
      if (r < 254)
        newColors[0 + i * 3] = r == 0 ? 0 : templates_R[r - 1][i] / 2;

      if (g < 254)
        newColors[1 + i * 3] = g == 0 ? 0 : templates_G[g - 1][i];

      if (b < 254)
        newColors[2 + i * 3] = b == 0 ? 0 : templates_B[b - 1][i];

        Serial.print("PARSER,RGB=");
              Serial.print(newColors[i*3]);
              Serial.print(",");
              Serial.print(newColors[i*3+1]);
              Serial.print(",");
              Serial.println(newColors[i*3+2]);
  }

  //newColors[0 + NUM_LEDS * 3] = newColors[0 * 3];
  //  newColors[1 + NUM_LEDS * 3] = newColors[1 * 3] ;
  //  newColors[2 + NUM_LEDS * 3] = newColors[2 * 3] ;

  Serial.print("R");
  Serial.print(r);
  Serial.print(" G");
  Serial.print(g);
  Serial.print(" B");
  Serial.print(b);
  Serial.println(" - SET TEMPLATE: OK");
  }

    }*/
// ***************************************************************
// ***************************************************************
/*class CheckSerial : public Task {
  protected:
    void loop()  {
      if (Serial.available() > 2)
        ParseMode(Serial.read(), Serial.read(), Serial.read());
    }
  } serial_task;*/

