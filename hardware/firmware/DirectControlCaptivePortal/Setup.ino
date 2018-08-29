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
  //allows serving of files from SPIFFS
  SPIFFS.begin();

  if (SPIFFS.exists("/booting.txt"))
    WiFi.disconnect();
  else
    SPIFFS.open("/booting.txt", "w");

  strip.begin();
  strip.setBrightness(255);

  //strip.show();

  clearEverything();
    flashAll(128,0,0);

  Serial.begin(115200);
  while (!Serial) {
    ; // wait for port to be ready
  }

  // Tell the computer that we're ready for data
  Serial.println("INIT: OK");

  // Run scheduler
  run();
}
