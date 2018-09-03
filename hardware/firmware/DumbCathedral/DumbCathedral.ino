#include <WS2812FX.h>
#include "frames.h"
#include <avr/pgmspace.h>

#define LED_COUNT 11
#define BYTES_PER_LED 3
#define LED_PIN D8

WS2812FX  strip = WS2812FX(
                    LED_COUNT,             // Number of pixels in strip
                    LED_PIN,                   // Pin number (most are valid)
                    NEO_GRB + NEO_KHZ800  //  pixel type flags, add together as needed:
                    //   NEO_RGB     Pixels are wired for RGB bitstream
                    //   NEO_GRB     Pixels are wired for GRB bitstream
                    //   NEO_KHZ400  400 KHz bitstream (e.g. Old FLORA pixels)
                    //   NEO_KHZ800  800 KHz bitstream (e.g. New FLORA pixels and most WS2811 strips)
                  );

void flashAll(byte r, byte g, byte b) {
  // Do a quick test/demo to show that things are working
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
}

double currentColors[LED_COUNT * 3];
double newColors[LED_COUNT * 3];


void clearEverything()
{
  // Initialize
  memset(newColors, 0, sizeof(newColors));
  memset(currentColors, 0, sizeof(currentColors));
  // memset(currentEffects, 0, sizeof(currentEffects));
}

void setup() {
  //Serial.begin(9600);
  strip.init();
  strip.setBrightness(255);
  strip.setSpeed(1000);
  //strip.setMode(12);
  //strip.setCustomMode(mode_aurora_cycle);
  //strip.start();
  clearEverything();
}

// This gets the length of an array at compile time
template< typename T, size_t N > constexpr size_t ArrayLength(T (&)[N])
{
  return N;
}

const double changeSpeed = 0.01;

void loop() {
  /*flashAll(255, 90, 0);
    delay(100);
    flashAll(0, 255, 255);
    delay(100);*/

  //strip.service();

  // Read colors
  for (int frame = 0; frame < ArrayLength(frames); frame++)
  {
    for (byte led = 0; led < LED_COUNT; led++)
      for (byte b = 0; b < BYTES_PER_LED; b++)
        newColors[led * BYTES_PER_LED + b] = pgm_read_byte_near(&frames[frame][led * BYTES_PER_LED + b]);

    // Fade here
    const byte totalSteps = 100;
    for (byte steps = 0; steps < totalSteps; steps++)
    {
      for (int ii = 0; ii < LED_COUNT; ii++)
      {
        int i = ii * BYTES_PER_LED;

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

        strip.setPixelColor(ii, max(0, (int)(currentColors[i] )),
                            max(0, (int)(currentColors[i + 1] )),
                            max(0, (int)(currentColors[i + 2] )));
      }

      strip.show();
      delay(5);
    }
  }
}

