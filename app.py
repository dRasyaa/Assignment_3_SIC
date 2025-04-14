import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import os
from PIL import Image

# Connect with ubidots
TOKEN = "BBUS-dUnnmdDGegd40VNGBKuCOnpvAbO9eJ"
LABEL = "neocane-dashboard"

# Cached Function
@st.cache_data(ttl=2, show_spinner=False)

# Function to get the data
def load_sensor_value(token):
    my_headers = {"X-Auth-Token": TOKEN}

    url1 = f"https://industrial.api.ubidots.com/api/v1.6/devices/neocane-dashboard/jarak/lv"
    url2 = f"https://industrial.api.ubidots.com/api/v1.6/devices/neocane-dashboard/ai_vision/lv"
    url3 = f"https://industrial.api.ubidots.com/api/v1.6/devices/neocane-dashboard/emergency/lv"

    try:
        response_jarak = requests.get(url1, headers=my_headers)
        response_ai_vision = requests.get(url2, headers=my_headers)
        response_emergency = requests.get(url3, headers=my_headers)
        
        response_jarak.raise_for_status()
        response_ai_vision.raise_for_status()
        response_emergency.raise_for_status()

        jarak_value = float(response_jarak.text)
        vision_value = int(response_ai_vision.text)
        emergency_value = int(response_emergency.text)

        return {
            "jarak" : jarak_value,
            "ai_vision" : vision_value,
            "emergency" : emergency_value 
        }
    
    except Exception as e:
        print(f"Failed to collect the data: {e}")
        return None

with st.spinner("⏳ Loading real-time sensor data..."):
    sensor_values = load_sensor_value(TOKEN)
if sensor_values:
    print(sensor_values)



# Sidebar Menu
st.sidebar.title("📂 NeoCane Menu")
menu = st.sidebar.radio("Select View:", ["Home", "Data", "📷 Photo History", "About NeoCane"])


# Home Page
if menu == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to NeoCane</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>_An AI & IoT-Based Smart Cane for the Visually Impaired_</p>", unsafe_allow_html=True)

# Data Page
elif menu == "Data":
    st.title('📊 Real-Time NeoCane Monitoring')

    if st.button("🔄 Refresh Data"):
        with st.spinner("Refreshing....."):
            st.rerun()
    
    if sensor_values:
        tab1, tab2, tab3 = st.tabs(["Object Detection", "AI Vision", "Emergency Log"])

        with tab1:
            st.subheader("Object Detection")
            distance = sensor_values['jarak']
            delta_value= distance - 50 
            st.metric(
                label="Distance",
                value=f"{distance:.2f} cm",
                delta=f"{delta_value:.2f} cm",
                delta_color="inverse",
                help="Distance measured by ultrasonic sensor"
            )

        with tab2:
            st.subheader("AI Vision")
            ai_status = "Critical Hole" if sensor_values["ai_vision"] == 1 else "Safe"  
            st.metric(
                label="AI Detection",
                value=ai_status,
                help="Detection result from AI camera"
            )

        with tab3:
            st.subheader("Emergency Button Log")
            emergency_status = "Active" if sensor_values["emergency"] == 1 else "Inactive"  # 1 means active, 0 means inactive
            st.metric(
                label="Emergency Status",
                value=emergency_status,
                help="Current state of the emergency button"
            )
        time.sleep(2)
        st.rerun()
    else:
        st.error("Failed to retrieve data from Ubidots.")

elif menu == "📷 Photo History":
    st.title("📷 Photo History")
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


# About Page
elif menu == "About NeoCane":
    st.title("ℹ️ About NeoCane")
    st.markdown("""
    **NeoCane** is an AI & IoT-powered smart cane designed to assist the visually impaired in navigating safely.
    
    - Equipped with ultrasonic sensors and AI camera
    - Detects obstacles and road holes
    - Emergency button & haptic feedback via smart bracelet
    """)
