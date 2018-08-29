class Monitor : public Task {
  private:
    char pos = 0;
    bool forward = false;
    long last = 0;
  public:
    void setup() {

      DEBUG_PRINT("Setting up server");
      flashAll(255, 0, 0);
      setupServer();

      SPIFFS.remove("/booting.txt");

      DEBUG_PRINT("Done. Connecting to wifi...");
      //ConnectToWifi();
    }
    void loop() {
      dnsServer.processNextRequest();
      server.handleClient();

      if (!isConnected)
      {
        for (int i = 0; i < NUM_LEDS; i++)
        {
          if (millis() > last)
          {
            if (pos + 2 >= NUM_LEDS || pos - 1 < 0)
              forward = !forward;

            pos += forward ? 1 : -1;
            last = millis() + 100;
          }
          currentColors[(i * 3) + 0] = i == pos ? (i == pos - 1 || i == pos + 1 ? 20 : 0) : 255;
          currentColors[(i * 3) + 1] = 0;
          currentColors[(i * 3) + 2] = 0;
        }
      }
    }
} monitor_task;

