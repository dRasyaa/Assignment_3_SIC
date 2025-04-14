#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include "base64.h"

// =========================
// Konfigurasi WiFi & Server
// =========================
const char* ssid = "Hidden";
const char* password = "denivorasya";
const char* serverURL = "http://192.168.74.12:5500/predict";

// ==========================
// Konfigurasi Kamera AI Thinker ESP32-CAM
// ==========================
#define PWDN_GPIO_NUM    32     // Untuk board AI Thinker, PWDN biasanya terhubung ke GPIO 32
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM     0
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27
#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      21
#define Y4_GPIO_NUM      19
#define Y3_GPIO_NUM      18
#define Y2_GPIO_NUM       5
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22

// ====================
// Fungsi Inisialisasi Kamera
// ====================
void initCamera() {
  camera_config_t config;
  
  // Konfigurasi channel LEDC untuk XCLK
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  
  // Konfigurasi pin data kamera
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;

  // Konfigurasi pin clock dan kontrol
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;

  // Frekuensi XCLK: 20 MHz
  config.xclk_freq_hz = 20000000;

  // Format pixel JPEG untuk efisiensi pengiriman data
  config.pixel_format = PIXFORMAT_JPEG;

  // Setting resolusi dan kualitas gambar:
  // FRAMESIZE_QQVGA memberikan resolusi rendah agar penggunaan RAM lebih efisien
  config.frame_size = FRAMESIZE_QQVGA;
  config.jpeg_quality = 15;  // Nilai ini bisa disesuaikan; semakin rendah nilainya, ukuran file akan semakin kecil
  config.fb_count = 1;       // Gunakan satu frame buffer untuk menghemat memori

  // Inisialisasi kamera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("❌ Kamera gagal inisialisasi: 0x%x\n", err);
  } else {
    Serial.println("✅ Kamera berhasil diinisialisasi!");
  }
}

// ====================
// Fungsi Setup
// ====================
void setup() {
  Serial.begin(115200);
  delay(1000); // Tunggu sejenak agar serial siap

  // 1. Inisialisasi kamera terlebih dahulu
  Serial.println("Inisialisasi kamera...");
  initCamera();
  delay(300);  // Tambahan delay agar kamera memiliki waktu untuk stabil

  // 2. Hubungkan ke WiFi
  Serial.println("Menghubungkan ke WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n📶 WiFi terhubung!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// ====================
// Fungsi Loop
// ====================
void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Ambil gambar menggunakan kamera
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("❌ Gagal mengambil gambar");
      delay(1000);
      return;
    }
    Serial.println("✅ Gambar berhasil diambil!");

    // Encode gambar ke format Base64 agar bisa dikirim via JSON
    String image_base64 = base64::encode(fb->buf, fb->len);
    // Kembalikan frame buffer agar memori kamera bisa di-reuse
    esp_camera_fb_return(fb);

    // Kirim gambar ke server menggunakan HTTP POST
    HTTPClient http;
    http.begin(serverURL); // inisialisasi koneksi ke URL server
    http.addHeader("Content-Type", "application/json");

    // Buat payload JSON dengan gambar encoded
    String payload = "{\"image\":\"" + image_base64 + "\"}";
    
    Serial.println("Mengirim gambar ke server...");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("✅ Response dari server: ");
      Serial.println(response);
    } else {
      Serial.print("❌ HTTP error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("❌ Tidak terhubung ke WiFi.");
  }

  delay(5000); // Kirim data tiap 5 detik
}
