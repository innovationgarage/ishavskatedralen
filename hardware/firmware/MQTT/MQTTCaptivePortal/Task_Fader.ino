class Fader : public Task {
  private:
    long nextChange = 0;
    const int speed = 20;
    const double changeSpeed = 0.05;

  public:
    void loop() {
      long t = millis() + speed;
      for (int ii = 0; ii < NUM_LEDS; ii++)
      {
        int i = ii * 3;

        currentColors[i + 0] = currentColors[i + 0] * (1 - changeSpeed) + newColors[i + 0] * (changeSpeed);
        currentColors[i + 1] = currentColors[i + 1] * (1 - changeSpeed) + newColors[i + 1] * (changeSpeed);
        currentColors[i + 2] = currentColors[i + 2] * (1 - changeSpeed) + newColors[i + 2] * (changeSpeed);

/*Serial.println("SETPIXEL ");
Serial.print(ii);
Serial.print("=");
Serial.print((int)(currentColors[i + 0] + currentEffects[i + 0]));
Serial.print(",");Serial.print((int)(currentColors[i + 1] + currentEffects[i + 1]));
Serial.print(",");Serial.print((int)(currentColors[i + 2] + currentEffects[i + 2]));
Serial.print("----END ");*/

        strip.setPixelColor(ii, max(0, (int)(currentColors[i] + currentEffects[i])),
                            max(0, (int)(currentColors[i + 1] + currentEffects[i + 1])),
                            max(0, (int)(currentColors[i + 2] + currentEffects[i + 2])));
      }

      strip.show();

      // Wait until next cycle
      delay(max(0, (int)(t - millis())));
    }
} fader_task;
