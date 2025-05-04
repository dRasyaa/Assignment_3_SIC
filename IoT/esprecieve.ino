#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>
#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>
#include <HTTPClient.h>


// ----- Config -----
constexpr int WIFI_CHANNEL          = 6;
constexpr uint8_t DFPLAYER_RX_PIN   = 16;
constexpr uint8_t DFPLAYER_TX_PIN   = 17;
constexpr uint8_t DFPLAYER_VOLUME   = 25;
constexpr uint8_t BUTTON_PIN = 4;

constexpr uint8_t SOUND_ALERT       = 3;
constexpr uint8_t SOUND_ROAD_DAMAGE = 2;
constexpr uint8_t SOUND_FAMILY      = 4;

const char*EMERGENCY_URL = "http://192.168.155.11:5500/emergency";

unsigned long lastButtonCheck = 0;
const unsigned long BUTTON_CHECK_INTERVAL = 5000;

// ----- Data Struct -----
struct SensorData {
  float depan, kiri, kanan;
  bool  bahaya;
};

SensorData dataSensor;

// ----- DFPlayer -----
HardwareSerial dfSerial(1);
DFRobotDFPlayerMini player;

// ----- Prototypes -----
void initWiFi();
void initESPNOW();
void initDFPlayer();
void onReceiveData(const esp_now_recv_info_t*, const uint8_t*, int);
void handleSensorData();
void handleStringMessage(const String&);

// ----- Setup & Loop -----
void setup() {
  Serial.begin(115200);
  Serial.println("🔄 Starting...");

  initWiFi();
  initESPNOW();
  initDFPlayer();
  pinMode(BUTTON_PIN, INPUT_PULLUP); 

  Serial.println("🚀 System Ready!");
}

void loop() {
  unsigned long now = millis(); 
  if (now - lastButtonCheck >= BUTTON_CHECK_INTERVAL) {
    lastButtonCheck = now;
    if (digitalRead(BUTTON_PIN) == LOW) {
      Serial.println("🆘 Emergency button pressed!");
      sendEmergencyToServer();
    }
  }
}

// ----- Initializations -----
void initWiFi() {
  WiFi.mode(WIFI_STA);
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
  esp_wifi_set_promiscuous(false);
  delay(50);
  Serial.printf("📡 MAC: %s\n", WiFi.macAddress().c_str());
}

void initESPNOW() {
  if (esp_now_init() != ESP_OK) {
    Serial.println("❌ ESP-NOW init failed");
    return;
  }
  esp_now_register_recv_cb(onReceiveData);
  Serial.println("✅ ESP-NOW OK");
}

void initDFPlayer() {
  dfSerial.begin(9600, SERIAL_8N1, DFPLAYER_RX_PIN, DFPLAYER_TX_PIN);
  if (!player.begin(dfSerial)) {
    Serial.println("❌ DFPlayer init failed");
    return;
  }
  player.volume(DFPLAYER_VOLUME);
  Serial.println("✅ DFPlayer OK");
}

// ----- Callback & Handlers -----
void onReceiveData(const esp_now_recv_info_t* info, const uint8_t* data, int len) {
  char mac[18];
  snprintf(mac, sizeof(mac),
           "%02X:%02X:%02X:%02X:%02X:%02X",
           info->src_addr[0], info->src_addr[1], info->src_addr[2],
           info->src_addr[3], info->src_addr[4], info->src_addr[5]);
  Serial.printf("📡 From: %s\n", mac);

  if (len == sizeof(SensorData)) {
    memcpy(&dataSensor, data, sizeof(dataSensor));
    handleSensorData();
  } else {
    String msg;
    msg.reserve(len);
    for (int i = 0; i < len; i++) msg += char(data[i]);
    msg.trim();
    handleStringMessage(msg);
  }
}

void handleSensorData() {
  Serial.printf("🔍 Depan: %.2f cm | Kiri: %.2f cm | Kanan: %.2f cm\n",
                dataSensor.depan, dataSensor.kiri, dataSensor.kanan);
  if (dataSensor.bahaya) {
    Serial.println("🚨 BAHAYA DETECTED!");
    player.play(SOUND_ALERT);
    delay(3000);
  }
}

void handleStringMessage(const String& msg) {
  Serial.printf("📩 Msg: %s\n", msg.c_str());
  if (msg.equalsIgnoreCase("rusak")) {
    Serial.println("🚨 Road damage!");
    player.play(SOUND_ROAD_DAMAGE);
    delay(3000);
  } else if (msg.equalsIgnoreCase("keluarga")) {
    Serial.println("👨‍👩‍👧 Family recognized!");
    player.play(SOUND_FAMILY);
    delay(3000);
  }
}

void sendEmergencyToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(EMERGENCY_URL);
    http.addHeader("Content-Type", "application/json");
    
    String json = "{\"emergency\": true}";
    int resCode = http.POST(json);

    if (resCode > 0) {
      Serial.printf("✅ Emergency sent! Code: %d\n", resCode);
    } else {
      Serial.printf("❌ Failed to send emergency! Code: %d\n", resCode);
    }
    http.end();
  } else {
    Serial.println("❌ WiFi not connected!");
  }
}
