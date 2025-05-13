#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <esp_camera.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include "base64.h"

// =========================
// CONFIGURATION
// =========================
const char* ssid         = "Balai Diklat 2025";
const char* password     = "denivorasya";
const char* serverPredict = "http://192.168.155.11:5500/predict";
const char* serverSave    = "http://192.168.155.11:5500/save-photo";
const char* serverFace    = "http://192.168.155.11:5510/face-recognition";

// MAC address peer ESP-NOW (gelang)
const uint8_t receiverMAC[] = {0xF8, 0xB3, 0xB7, 0x7B, 0xDD, 0xD8};

// Interval kirim (ms)
const unsigned long SEND_INTERVAL = 5000;

// =========================
// HELPERS
// =========================
void sendESPNowMessage(const char* msg) {
  esp_err_t res = esp_now_send(receiverMAC, (uint8_t*)msg, strlen(msg));
  if (res == ESP_OK) {
    Serial.println(String("[ESP-NOW] Kirim sukses: ") + msg);
  } else {
    Serial.println(String("[ESP-NOW] Kirim gagal: ") + msg);
  }
}

bool sendToServer(const char* url, const String& payload, String* outResponse = nullptr) {
  HTTPClient http;
  Serial.println(String("[HTTP] Mulai koneksi ke: ") + url);
  if (!http.begin(url)) {
    Serial.println(String("[HTTP] Begin gagal: ") + url);
    return false;
  }
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(payload);
  Serial.println(String("[HTTP] Response code: ") + code);
  if (code > 0) {
    if (outResponse) {
      *outResponse = http.getString();
      Serial.println(String("[HTTP] Response: ") + *outResponse);
    }
    http.end();
    return true;
  } else {
    Serial.println(String("[HTTP] POST gagal ke: ") + url);
    http.end();
    return false;
  }
}

void ensureWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WiFi] Terputus, reconnecting...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
  }
}

// =========================
// INIT FUNCTIONS
// =========================
void initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = 5;
  config.pin_d1       = 18;
  config.pin_d2       = 19;
  config.pin_d3       = 21;
  config.pin_d4       = 36;
  config.pin_d5       = 39;
  config.pin_d6       = 34;
  config.pin_d7       = 35;
  config.pin_xclk     = 0;
  config.pin_pclk     = 22;
  config.pin_vsync    = 25;
  config.pin_href     = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn     = 32;
  config.pin_reset    = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_QQVGA;
  config.jpeg_quality = 15;
  config.fb_count     = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.println(String("[CAMERA] Inisialisasi gagal: ") + String(err));
  } else {
    Serial.println("[CAMERA] Inisialisasi sukses");
  }
}

void initESPNOW() {
  if (esp_now_init() != ESP_OK) {
    Serial.println("[ESP-NOW] Init gagal");
    return;
  }
  esp_now_register_send_cb([](const uint8_t *mac, esp_now_send_status_t status){
    Serial.println(String("[ESP-NOW] Status: ") + (status == ESP_NOW_SEND_SUCCESS ? "OK" : "FAIL"));
  });
  esp_now_peer_info_t peerInfo;
  memset(&peerInfo, 0, sizeof(peerInfo));
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("[ESP-NOW] Gagal tambah peer");
    return;
  }
  Serial.println("[ESP-NOW] Ready");
}

// =========================
// SETUP & LOOP
// =========================
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("[SETUP] Memulai sistem...");

  initCamera();

  Serial.println(String("[WiFi] Connecting to: ") + ssid);
  WiFi.begin(ssid, password);
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    retries++;
    if (retries > 20) {
      Serial.println("\n[WiFi] Gagal connect, restart...");
      ESP.restart();
    }
  }
  Serial.println("\n[WiFi] Connected!");
  Serial.println(String("[WiFi] IP Address: ") + WiFi.localIP().toString());

  initESPNOW();
}

void loop() {
  ensureWiFi();

  static unsigned long lastTime = 0;
  unsigned long now = millis();
  if (now - lastTime < SEND_INTERVAL) return;
  lastTime = now;

  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("[CAMERA] Gagal ambil frame");
    return;
  }
  Serial.println(String("[CAMERA] Frame captured, size: ") + fb->len);

  String img = base64::encode(fb->buf, fb->len);
  esp_camera_fb_return(fb);
  Serial.println("[BASE64] Encoding selesai");

  String payload = String("{\"image\":\"") + img + "\"}";
  String resp;

  // /predict
  Serial.println("[SERVER] Kirim ke /predict");
  if (sendToServer(serverPredict, payload, &resp)) {
    if (resp.indexOf("\"status\":\"jalan rusak\"") >= 0) {
      Serial.println("[DETECT] Jalan rusak terdeteksi");
      sendESPNowMessage("rusak");
    } else {
      Serial.println("[DETECT] Jalan aman");
    }
  }

  // /save-photo
  Serial.println("[SERVER] Kirim ke /save-photo");
  sendToServer(serverSave, payload);

  // /face-recognition
  Serial.println("[SERVER] Kirim ke /face-recognition");
  if (sendToServer(serverFace, payload, &resp)) {
    if (resp.indexOf("\"status\":\"keluarga\"") >= 0) {
      Serial.println("[DETECT] Keluarga terdeteksi");
      sendESPNowMessage("keluarga");
    }
  }
}
