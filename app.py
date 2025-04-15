import streamlit as st
import numpy as np
import requests
import time
import os
from PIL import Image
 
# Konfigurasi Ubidots
TOKEN = "BBUS-dUnnmdDGegd40VNGBKuCOnpvAbO9eJ"
LABEL = "neocane-dashboard"
 
# Fungsi untuk mengambil data sensor
def load_sensor_value(token):
    my_headers = {"X-Auth-Token": TOKEN}
    url3 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kanan/lv"
    url4 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kiri/lv"
    url5 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_tengah/lv"
    try:
        response_jarak_kanan = requests.get(url3, headers=my_headers)
        response_jarak_kiri = requests.get(url4, headers=my_headers)
        response_jarak_tengah = requests.get(url5, headers=my_headers)
 
        response_jarak_kiri.raise_for_status()
        response_jarak_tengah.raise_for_status()
 
        jarak_kanan = float(response_jarak_kanan.text)
        jarak_tengah = float(response_jarak_tengah.text)
        jarak_kiri = float(response_jarak_kiri.text)
        return {
            "jarak_kanan": jarak_kanan,
            "jarak_tengah": jarak_tengah,
            "jarak_kiri": jarak_kiri
        }
    except Exception as e:
        st.error(f"Failed to collect the data: {e}")
        return None
 
# Inisialisasi sensor_values di st.session_state (jika belum ada)
if "sensor_values" not in st.session_state:
    st.session_state.sensor_values = load_sensor_value(TOKEN)
 
# Sidebar Menu
st.sidebar.title("📂 NeoCane Menu")
menu = st.sidebar.radio("Select View:", ["Home", "Data", "About NeoCane"])
 
# Halaman Home
if menu == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to NeoCane</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>_An AI & IoT-Based Smart Cane for the Visually Impaired_</p>", unsafe_allow_html=True)
 
# Halaman Data
elif menu == "Data":
    st.title('📊 Real-Time NeoCane Monitoring')
 
    # Tombol Refresh Data: update data tanpa merestart halaman (tanpa st.rerun())
    if st.button("🔄 Refresh Data"):
        with st.spinner("Refreshing..."):
            # Update sensor_values di session state
            st.session_state.sensor_values = load_sensor_value(TOKEN)
            # Opsional: kasih delay kecil agar loading terasa smooth
            time.sleep(1)
 
    sensor_values = st.session_state.sensor_values
 
    if sensor_values:
        # Buat tab untuk Object Detection dan AI Vision
        tab1, tab2, tab3 = st.tabs(["Object Detection", "AI Vision", "📷 Photo History"])
 
        with tab1:
            st.subheader("Object Detection")
            right_distance = sensor_values["jarak_kanan"]
            middle_distance = sensor_values["jarak_tengah"]
            left_distance = sensor_values["jarak_kiri"]
 
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⬅️ Left", f"{left_distance:.2f} cm")
                status_l = "<h5 style='color: red;'>⚠️ Danger</h5>" if left_distance < 100 else "<h5 style='color: green;'>✅ Safe</h5>"
                st.markdown(status_l, unsafe_allow_html=True)
            with col2:
                st.metric("⬆️ Front", f"{middle_distance:.2f} cm")
                status_m = "<h5 style='color: red;'>⚠️ Danger</h5>" if middle_distance < 100 else "<h5 style='color: green;'>✅ Safe</h5>"
                st.markdown(status_m, unsafe_allow_html=True)
            with col3:
                st.metric("➡️ Right", f"{right_distance:.2f} cm")
                status_r = "<h5 style='color: red;'>⚠️ Danger</h5>" if right_distance < 100 else "<h5 style='color: green;'>✅ Safe</h5>"
                st.markdown(status_r, unsafe_allow_html=True)
 
        with tab2: 
            st.subheader("Ai Vision")
        
        with tab3:
            st.subheader("📷 Photo History")
            st.markdown("Berikut adalah 5 foto terakhir yang diambil oleh ESP32-CAM.")
 
            if st.button("🔄 Refresh Galeri"):
                st.rerun() 
 
            PHOTO_FOLDER = "saved_photos"
            cols = st.columns(5)
 
            for i in range(1, 6):
                path = os.path.join(PHOTO_FOLDER, f"photo_{i}.jpg")
                if os.path.exists(path):
                    with cols[i - 1]:
                        st.image(Image.open(path), caption=f"photo_{i}.jpg", use_container_width=True)
                else:
                    with cols[i - 1]:
                        st.warning(f"photo_{i}.jpg not found", icon="⚠️")
 
 
    else:
        st.error("❌ Failed to retrieve data from Ubidots.")
 
# Halaman About
elif menu == "About NeoCane":
    st.title("ℹ️ About NeoCane")
    st.markdown("""
    **NeoCane** is an AI & IoT-powered smart cane designed to assist the visually impaired in navigating safely.
 
    - Equipped with ultrasonic sensors and AI camera
    - Detects obstacles and road holes in real-time
    - Future potential to support other types of disabilities
    """)