#include <esp_now.h>
#include <WiFi.h>
#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>
  
// Struct data dari pengirim (sensor jarak)
typedef struct struct_message {
  float depan;
  float kiri;
  float kanan;
} struct_message;

struct_message dataSensor;

// DFPlayer setup
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

  // Cek apakah struct atau string
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
  } else {
    String msg = "";
    for (int i = 0; i < len; i++) {
      msg += (char)incomingData[i];
    }
    Serial.print("📩 Pesan string diterima: ");
    Serial.println(msg);

    if (msg == "rusak") {
      Serial.println("🚨 Jalan rusak terdeteksi! Mainkan suara DFPlayer...");
      player.play(1);
    }
  }
}


void setup() {
  Serial.begin(115200);
  Serial.println("ESP-NOW Receiver siap...");
  WiFi.mode(WIFI_STA);  
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

void loop() {
  
}
