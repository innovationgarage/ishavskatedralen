class Sparkler : public Task {
  private:
    //long nextChange = 0;
    const int speed = 100, variance = 10, chance_to_be_selected = 3;
    const int green_variance = 3, blue_variance = 1, variance_divider = 10, gray_reduction = 20;

  public:
    void loop() {
      //if (millis() > nextChange)
      {
        //Serial.print("!");
        //nextChange = millis() + random(speed - variance, speed + variance);

        // Modify some green/blue channels at random
        for (int i = 0; i < NUM_LEDS; i++)
        {
          if (random(0, chance_to_be_selected) == 0)
          {
            int R = i * 3, G = R + 1, B = G + 1;

            // Read current color
            //currentColor[R] = ;
            //currentColor[G] = ;
            //currentColor[B] = ;
            double gray = (currentColors[R] + currentColors[G] + currentColors[B]) / 3;

            // Layer with effects
            //currentEffects[R] = 0; // Red channel stays the same
            currentEffects[G] = random(-green_variance, green_variance) * (gray / gray_reduction) / variance_divider; // Green channel
            currentEffects[B] = random(-blue_variance, blue_variance) * (gray / gray_reduction) / variance_divider; // Blue channel
          }
        }
        delay(random(speed - variance, speed + variance));
      }
    }
} sparkler_task;

