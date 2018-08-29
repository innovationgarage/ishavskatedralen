void ParseMode(byte r, byte g, byte b)
{
  isConnected = true;
  for (int i = 0; i < NUM_LEDS; i++)
  {
    //strip.setPixelColor(i, 0, templates[t][i], 0);

    if (r == 255)
    {

    }
    else
    {
      /*if (r < 254)
        newColors[0 + i * 3] = r == 0 ? 0 : templates_R[r - 1][i] / 2;

      if (g < 254)
        newColors[1 + i * 3] = g == 0 ? 0 : templates_G[g - 1][i];

      if (b < 254)
        newColors[2 + i * 3] = b == 0 ? 0 : templates_B[b - 1][i];
      
        Serial.print("PARSER,RGB=");
              Serial.print(newColors[i*3]);
              Serial.print(",");
              Serial.print(newColors[i*3+1]);
              Serial.print(",");
              Serial.println(newColors[i*3+2]);*/
    }
  }

  //newColors[0 + NUM_LEDS * 3] = newColors[0 * 3];
  //  newColors[1 + NUM_LEDS * 3] = newColors[1 * 3] ;
  //  newColors[2 + NUM_LEDS * 3] = newColors[2 * 3] ;

  Serial.print("R");
  Serial.print(r);
  Serial.print(" G");
  Serial.print(g);
  Serial.print(" B");
  Serial.print(b);
  Serial.println(" - SET TEMPLATE: OK");
}

// ***************************************************************
// ***************************************************************
class CheckSerial : public Task {
  protected:
    void loop()  {
      if (Serial.available() > 2)
        ParseMode(Serial.read(), Serial.read(), Serial.read());
    }
} serial_task;

// ***************************************************************
// ***************************************************************
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

// ***************************************************************
// ***************************************************************

// ***************************************************************
// ***************************************************************


// ***************************************************************
// ***************************************************************
class Downloader : public Task {
  protected:
    void setup() {
      //delay(1000 * 15);
      //ConnectToWifi();
    }

    void loop() {
      Serial.println("Downloading...");

      String host = "auroreal.innovationgarage.no";
      WiFiClient client;

      if (client.connect(host, 80)) {
        client.print(String("GET ") + "/status" + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "Connection: close\r\n\r\n");

        unsigned long timeout = millis();
        while (client.available() == 0) {
          if (millis() - timeout > 45000) {
            Serial.println(">>> Client Timeout !");
            client.stop();

            clearEverything();
            isConnected = false;
          }
        }

        while (client.available() > 3)
          client.read();

        // Set RGB
        ParseMode(client.read(), client.read(), client.read());
      }
      else
        Serial.println("Connection failed.");

      Serial.println("Waiting now.");
      delay(1000 * 5);
    }
} downloader_task;

void run()
{
  Scheduler.start(&serial_task);
  Scheduler.start(&monitor_task);
  Scheduler.start(&fader_task);
  Scheduler.start(&sparkler_task);
  Scheduler.start(&downloader_task);
  Scheduler.begin();
}

