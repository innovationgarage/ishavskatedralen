#include <PersWiFiManager.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266SSDP.h>
#include <ESP8266WebServer.h>
#include <DNSServer.h>
#include <FS.h>
#include <Scheduler.h>
#include <Task.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_NeoPixel.h>
#include <EEPROM.h>
#include <PubSubClient.h>
#include "settings.h"


#define DEBUG_SERIAL //uncomment for Serial debugging statements

#ifdef DEBUG_SERIAL
#define DEBUG_BEGIN Serial.begin(115200)
#define DEBUG_PRINT(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_BEGIN
#endif

double currentColors[NUM_LEDS * 3];
double currentEffects[NUM_LEDS * 3];
double newColors[NUM_LEDS * 3];
bool isConnected = false;
ESP8266WiFiMulti wifiMulti;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(
  NUM_LEDS,             // Number of pixels in strip
  STRIP_PIN,                   // Pin number (most are valid)
  NEO_GRB + NEO_KHZ800  //  pixel type flags, add together as needed:
                        //   NEO_RGB     Pixels are wired for RGB bitstream
                        //   NEO_GRB     Pixels are wired for GRB bitstream
                        //   NEO_KHZ400  400 KHz bitstream (e.g. Old FLORA pixels)
                        //   NEO_KHZ800  800 KHz bitstream (e.g. New FLORA pixels and most WS2811 strips)
);
