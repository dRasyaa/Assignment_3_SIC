#include <esp_now.h>
#include <WiFi.h>

// Struct data dari pengirim
typedef struct struct_message {
  float depan;
  float kiri;
  float kanan;
} struct_message;

struct_message dataSensor;

// Callback ketika data diterima
void onReceiveData(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  memcpy(&dataSensor, incomingData, sizeof(dataSensor));
  Serial.println("✅ Data DITERIMA via ESP-NOW:");
  Serial.print("  Depan: ");
  Serial.print(dataSensor.depan);
  Serial.print(" cm | Kiri: ");
  Serial.print(dataSensor.kiri);
  Serial.print(" cm | Kanan: ");
  Serial.print(dataSensor.kanan);
  Serial.println(" cm");

  // Tambahin logika sesuai kebutuhan (vibrator, LCD, dll.)
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.println("ESP-NOW Receiver siap...");

  if (esp_now_init() != ESP_OK) {
    Serial.println("❌ ESP-NOW init gagal");
    return;
  }

  // Daftar callback versi baru
  esp_now_register_recv_cb(onReceiveData);
}

void loop() {
  // Tidak perlu isi apa-apa, callback jalan otomatis
}
