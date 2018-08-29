class Fader : public Task {
  private:
    long nextChange = 0;
    const int speed = 20;
    const double changeSpeed = 0.01;

  public:
    void loop() {
      long t = millis() + speed;
      for (int ii = 0; ii < NUM_LEDS; ii++)
      {
        int i = ii * 3;

        currentColors[i + 0] = currentColors[i + 0] * (1 - changeSpeed) + newColors[i + 0] * (changeSpeed);
        currentColors[i + 1] = currentColors[i + 1] * (1 - changeSpeed) + newColors[i + 1] * (changeSpeed);
        currentColors[i + 2] = currentColors[i + 2] * (1 - changeSpeed) + newColors[i + 2] * (changeSpeed);

        strip.setPixelColor(ii, max(0, (int)(currentColors[i] + currentEffects[i])),
                            max(0, (int)(currentColors[i + 1] + currentEffects[i + 1])),
                            max(0, (int)(currentColors[i + 2] + currentEffects[i + 2])));
        /*
          Serial.print("FADER,RGB=");
                Serial.print(newColors[i]);
                Serial.print(",");
                Serial.print(newColors[i+1]);
                Serial.print(",");
                Serial.println(newColors[i+2]);*/
      }

      // Scroll
      /*  if (millis() > nextChange)
        {
          nextChange = millis() + random(4000, 6000);

          // Advance one

          for (int i = -1; i < NUM_LEDS + 1; i++)
            for (int j = 0; j < 3; j++)
            {
              if (i == -1)
                newColors[(NUM_LEDS * 3) + j] = newColors[j];
              else
                newColors[j + i * 3] = newColors[j + (i + 1) * 3];
            }
        }*/

      strip.show();

      // Wait until next cycle
      delay(max(0, (int)(t - millis())));
    }
} fader_task;
