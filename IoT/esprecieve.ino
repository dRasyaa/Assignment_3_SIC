#include <esp_now.h>
#include <WiFi.h>
#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>
<<<<<<< Updated upstream
#include <esp_wifi.h>
 
// Struct data dari pengirim (sensor jarak)
typedef struct struct_message {
  float depan;
  float kiri;
  float kanan;
  bool bahaya; 
} struct_message;
 
struct_message dataSensor;
 
// DFPlayer setup
=======
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
>>>>>>> Stashed changes
HardwareSerial dfSerial(1);
#define RXD 17
#define TXD 16
DFRobotDFPlayerMini player;
 
// Callback ESP-NOW
void onReceiveData(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  char macStr[18];
  snprintf(macStr, sizeof(macStr),
           "%02X:%02X:%02X:%02X:%02X:%02X",
           recvInfo->src_addr[0], recvInfo->src_addr[1], recvInfo->src_addr[2],
           recvInfo->src_addr[3], recvInfo->src_addr[4], recvInfo->src_addr[5]);
 
  Serial.print("📡 Data diterima dari: ");
  Serial.println(macStr);
 
  if (len == sizeof(struct_message)) {
    memcpy(&dataSensor, incomingData, sizeof(dataSensor));
    Serial.println("✅ Data SENSOR diterima via ESP-NOW:");
    Serial.print("  Depan: ");
    Serial.print(dataSensor.depan);
    Serial.print(" cm | Kiri: ");
    Serial.print(dataSensor.kiri);
    Serial.print(" cm | Kanan: ");
    Serial.print(dataSensor.kanan);
    Serial.println(" cm");
 
    if (dataSensor.bahaya) {
      Serial.println("🚨 BAHAYA TERDETEKSI! Memainkan suara peringatan...");
      player.play(2);  
      delay(3000);     
    }
 
  } else {
    String msg = "";
    for (int i = 0; i < len; i++) {
      msg += (char)incomingData[i];
    }
 
    msg.trim();
    Serial.print("📩 Pesan string diterima: ");
    Serial.println(msg);
 
    if (msg.equalsIgnoreCase("rusak")) {
      Serial.println("🚨 Jalan rusak terdeteksi! Memainkan suara DFPlayer...");
      player.play(1);
      delay(3000);
    }
  }
}
 
 
 
void setup() {
  Serial.begin(115200);
<<<<<<< Updated upstream
  Serial.println("ESP-NOW Receiver siap...");
  WiFi.mode(WIFI_STA);  
 
  int wifi_channel = 6; 
=======
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
>>>>>>> Stashed changes
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_channel(wifi_channel, WIFI_SECOND_CHAN_NONE);
  esp_wifi_set_promiscuous(false);
  delay(50);           
  Serial.print("📡 MAC Address ESP32 Gelang: ");
  Serial.println(WiFi.macAddress());  
 
  // ESP-NOW init
  if (esp_now_init() != ESP_OK) {
    Serial.println("❌ ESP-NOW init gagal");
    return; 
  }
  esp_now_register_recv_cb(onReceiveData);
 
 // DFPlayer Mini init pakai HardwareSerial
  dfSerial.begin(9600, SERIAL_8N1, RXD, TXD);
  if (!player.begin(dfSerial)) {
    Serial.println("❌ DFPlayer gagal start");
  } else {
    Serial.println("✅ DFPlayer OK");
    player.volume(25);
  }
}
<<<<<<< Updated upstream
 
void loop() {
=======

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
>>>>>>> Stashed changes
}