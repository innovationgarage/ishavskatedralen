void flashAll(byte r, byte g, byte b) {
  // Do a quick test/demo to show that things are working
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
}

void clearEverything()
{
  // Initialize
  memset(newColors, 0, sizeof(newColors));
  memset(currentColors, 0, sizeof(currentColors));
  memset(currentEffects, 0, sizeof(currentEffects));
}

void setup() {
  strip.begin();
  strip.setBrightness(255);
  clearEverything();

  Serial.begin(115200);
  while (!Serial) {
    ; // wait for port to be ready
  }

  // Tell the computer that we're ready for data
  Serial.println("INIT: OK");

  WiFiManager wifiManager;

  WiFiManagerParameter custom_text("<p>This is just a text paragraph</p>");
  wifiManager.addParameter(&custom_text);

  flashAll(255, 90, 0);
  String ssid = "ArcticCathedral-" + String(ESP.getChipId());
  wifiManager.autoConnect(ssid.c_str());
  
  run();
}
