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

#include "templates.h"
#include "credentials.h"

#define STRIP_PIN D7

static const int CHECK_DELAY = 1000,NUM_LEDS = 11;
double currentColors[NUM_LEDS * 3];
double currentEffects[NUM_LEDS * 3];
double newColors[NUM_LEDS * 3];

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
