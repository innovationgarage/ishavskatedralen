void flashAll(uint32_t color) {
  // Do a quick test/demo to show that things are working
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

void setup() {

  strip.begin();
  strip.show();

  for (int i = 0; i < 120; i++) {
    flashAll(strip.Color((i % 20) * 2, i % 30, i % 60));
    delay(10);
  }

  memset(newColors, 0, sizeof(newColors));
  memset(currentColors, 0, sizeof(currentColors));

  Serial.begin(115200);
  while (!Serial) {
    ; // wait for port to be ready
  }

  // Tell the computer that we're ready for data
  Serial.println("INIT: OK");

  // Run scheduler
  run();
}
