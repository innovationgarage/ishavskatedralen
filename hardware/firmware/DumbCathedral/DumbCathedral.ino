#include <WS2812FX.h>
#include "frames.h"
#include <avr/pgmspace.h>

#define LED_COUNT 11
#define LED_PIN D8

WS2812FX  ws2812fx = WS2812FX(
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
    ws2812fx.setPixelColor(i, r, g, b);
  }
  ws2812fx.show();
}

void setup() {
  Serial.begin(9600);
  ws2812fx.init();
  ws2812fx.setBrightness(255);
  ws2812fx.setSpeed(1000);
  //ws2812fx.setMode(12);
  //ws2812fx.setCustomMode(mode_aurora_cycle);
  //ws2812fx.start();
}

// This gets the length of an array at compile time
template< typename T, size_t N > constexpr size_t ArrayLength(T (&)[N])
{
  return N;
}

void loop() {
  /*flashAll(255, 90, 0);
    delay(100);
    flashAll(0, 255, 255);
    delay(100);*/

  //ws2812fx.service();

  for (int i = 0; i < ArrayLength(frame); i++)
  {
    for (byte b = 0; b < 11; b++)
    {
      ws2812fx.setPixelColor(b, pgm_read_byte_near(&frame[i][b * 3 + 0]), pgm_read_byte_near(&frame[i][b * 3 + 1]), pgm_read_byte_near(&frame[i][b * 3 + 2]));
      ws2812fx.show();
    }
    delay(150);
  }
}
