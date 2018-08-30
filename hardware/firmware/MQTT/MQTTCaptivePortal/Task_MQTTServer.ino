#include "mqtt_settings.h"

WiFiClient espClient;
PubSubClient client(espClient); 

// Warning: Remember to edit MQTT_MAX_PACKET_SIZE to a bigger value in PubSubClient library

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  if (length < NUM_LEDS * 3)
  {
    client.publish(mqttPublishTo, "Invalid message");
  }
  else
  {
    Serial.println("Setting leds.");
    
    for (int i = 0; i < NUM_LEDS * 3; i++)
    {
      newColors[i] = payload[i];
      Serial.print(i);
      Serial.print("=");
      Serial.print(payload[i]);
      Serial.print(", ");
    }
     
    //memcpy(newColors, payload, sizeof(newColors[0])*length);
  }
}

class MQTTServer : public Task {
  protected:
    void keepConnected() {
      while (!client.connected()) {
        Serial.println("Connecting to MQTT...");

        client.setServer(mqttServer, mqttPort);
        client.setCallback(callback);

        String will = "Cathedral-" + String(ESP.getChipId()) + " down! rAvenge me!";
        if (client.connect(mqttDevice, mqttUser, mqttPassword, mqttPublishTo, 1, 1, will.c_str())) {

          Serial.println("connected");
          String msg = "Hi there, this is Cathedral-" + String(ESP.getChipId()) + " reporting for duty.";
          client.publish(mqttPublishTo, msg.c_str());
          client.subscribe(mqttSubscribeTo);

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
