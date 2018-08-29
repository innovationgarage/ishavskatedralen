//const char *metaRefreshStr = "<head><meta http-equiv=\"refresh\" content=\"1; url=/\" /></head><body><a href=\"/\">redirecting...</a></body>";
const char *metaRefreshStr = "<script>window.location='/'</script><a href='/'>redirecting...</a>";

//server objects
ESP8266WebServer server(80);
DNSServer dnsServer;
PersWiFiManager persWM(server, dnsServer);

void ConnectToWifi()
{
  //WiFi.mode(WIFI_STA);
  //wifiMulti.addAP(WIFISSID, WIFIPASS);

  Serial.println();
  Serial.print("Wait for WiFi... ");

  if (wifiMulti.run() == WL_CONNECTED)
  {
    isConnected = true;
    clearEverything();

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    delay(500);
  }
}

//code from fsbrowser example, consolidated.
bool handleFileRead(String path) {
  DEBUG_PRINT("handlefileread" + path);
  if (path.endsWith("/")) path += "index.htm";
  String contentType;
  if (path.endsWith(".htm") || path.endsWith(".html")) contentType = "text/html";
  else if (path.endsWith(".css")) contentType = "text/css";
  else if (path.endsWith(".js")) contentType = "application/javascript";
  else if (path.endsWith(".png")) contentType = "image/png";
  else if (path.endsWith(".gif")) contentType = "image/gif";
  else if (path.endsWith(".jpg")) contentType = "image/jpeg";
  else if (path.endsWith(".ico")) contentType = "image/x-icon";
  else if (path.endsWith(".xml")) contentType = "text/xml";
  else if (path.endsWith(".pdf")) contentType = "application/x-pdf";
  else if (path.endsWith(".zip")) contentType = "application/x-zip";
  else if (path.endsWith(".gz")) contentType = "application/x-gzip";
  else if (path.endsWith(".json")) contentType = "application/json";
  else contentType = "text/plain";

  //split filepath and extension
  String prefix = path, ext = "";
  int lastPeriod = path.lastIndexOf('.');
  if (lastPeriod >= 0) {
    prefix = path.substring(0, lastPeriod);
    ext = path.substring(lastPeriod);
  }

  //look for smaller versions of file
  //minified file, good (myscript.min.js)
  if (SPIFFS.exists(prefix + ".min" + ext)) path = prefix + ".min" + ext;
  //gzipped file, better (myscript.js.gz)
  if (SPIFFS.exists(prefix + ext + ".gz")) path = prefix + ext + ".gz";
  //min and gzipped file, best (myscript.min.js.gz)
  if (SPIFFS.exists(prefix + ".min" + ext + ".gz")) path = prefix + ".min" + ext + ".gz";

  if (SPIFFS.exists(path)) {
    DEBUG_PRINT("sending file " + path);
    File file = SPIFFS.open(path, "r");
    if (server.hasArg("download"))
      server.sendHeader("Content-Disposition", " attachment;");
    if (server.uri().indexOf("nocache") < 0)
      server.sendHeader("Cache-Control", " max-age=172800");

    //optional alt arg (encoded url), server sends redirect to file on the web
    if (WiFi.status() == WL_CONNECTED && server.hasArg("alt")) {
      server.sendHeader("Location", server.arg("alt"), true);
      server.send ( 302, "text/plain", "");
    } else {
      //server sends file
      size_t sent = server.streamFile(file, contentType);
    }
    file.close();
    return true;
  } //if SPIFFS.exists
  return false;
} //bool handleFileRead

void setupServer()
{
  String ssid = "ArcticCathedral-" + String(ESP.getChipId());
  persWM.setApCredentials(ssid.c_str());
  persWM.begin();

  //serve files from SPIFFS
  server.onNotFound([]() {
    if (!handleFileRead(server.uri())) {
      server.sendHeader("Cache-Control", " max-age=172800");
      server.send(302, "text/html", metaRefreshStr);
    }
  }); //server.onNotFound
  /*
    //handles commands from webpage, sends live data in JSON format
    server.on("/api", []() {
      DEBUG_PRINT("server.on /api");
      if (server.hasArg("x")) {
        x = server.arg("x").toInt();
        DEBUG_PRINT(String("x: ") + x);
      } //if
      if (server.hasArg("y")) {
        y = server.arg("y");
        DEBUG_PRINT("y: " + y);
      } //if

      //build json object of program data
      StaticJsonBuffer<200> jsonBuffer;
      JsonObject &json = jsonBuffer.createObject();
      json["x"] = x;
      json["y"] = y;

      char jsonchar[200];
      json.printTo(jsonchar); //print to char array, takes more memory but sends in one piece
      server.send(200, "application/json", jsonchar);

    }); //server.on api
  */

  //SSDP makes device visible on windows network
  server.on("/description.xml", HTTP_GET, []() {
    SSDP.schema(server.client());
  });
  SSDP.setSchemaURL("description.xml");
  SSDP.setHTTPPort(80);
  SSDP.setName(ssid.c_str());
  SSDP.setURL("/");
  SSDP.begin();
  SSDP.setDeviceType("upnp:rootdevice");

  server.begin();
}

