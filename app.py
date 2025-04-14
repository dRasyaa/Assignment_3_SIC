import streamlit as st
import pandas as pd
import requests

# Connect with Ubidots
TOKEN = "BBUS-dUnnmdDGegd40VNGBKuCOnpvAbO9eJ"
LABEL = "neocane-dashboard"

# Function to get the data
def load_sensor_value(token):
    my_headers = {"X-Auth-Token": TOKEN}

    url1 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/ai_vision/lv"
    url2 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/emergency/lv"
    url3 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kanan/lv"
    url4 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kiri/lv"
    url5 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_tengah/lv"

    try:
        response_ai_vision = requests.get(url1, headers=my_headers)
        response_emergency = requests.get(url2, headers=my_headers)
        response_jarak_kanan = requests.get(url3, headers=my_headers)
        response_jarak_kiri = requests.get(url4, headers=my_headers)
        response_jarak_tengah = requests.get(url5, headers=my_headers)
        
        response_ai_vision.raise_for_status()
        response_emergency.raise_for_status()
        response_jarak_kanan.raise_for_status()
        response_jarak_kiri.raise_for_status()
        response_jarak_tengah.raise_for_status()

        jarak_value = float(response_jarak.text)
        vision_value = int(response_ai_vision.text)
        emergency_value = int(response_emergency.text)

        return {
            "jarak": jarak_value,
            "ai_vision": vision_value,
            "emergency": emergency_value 
        }
    
    except Exception as e:
        st.error(f"Failed to collect the data: {e}")
        return None

# Sidebar Menu
st.sidebar.title("📂 NeoCane Menu")
menu = st.sidebar.radio("Select View:", ["Home", "Data", "About NeoCane"])

# Home Page
if menu == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to NeoCane</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>_An AI & IoT-Based Smart Cane for the Visually Impaired_</p>", unsafe_allow_html=True)

# Data Page
elif menu == "Data":
    st.title("📊 Real-Time NeoCane Monitoring")

    if st.button("🔄 Refresh Data"):
        sensor_values = load_sensor_value(TOKEN)
        
    if sensor_values:
        tab1, tab2, tab3 = st.tabs(["Object Detection", "AI Vision", "Emergency Log"])

        with tab1:
            st.subheader("Object Detection")
            distance = sensor_values["jarak"]
            delta_value = distance - 100  

            st.metric(
                label="Distance",
                value=f"{distance:.2f} cm",
                delta=f"{delta_value:.2f} cm",
                delta_color="inverse",
                help="Distance measured by ultrasonic sensor"
            )

            if distance < 100:
                st.markdown(
                    "<h4 style='color: red;'>⚠️ DANGER: Too Close!</h4>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<h4 style='color: green;'>✅ Safe Distance</h4>",
                    unsafe_allow_html=True
                )

        with tab2:
            st.subheader("AI Vision")
            ai_status = "⚠️ Critical Hole" if sensor_values["ai_vision"] == 1 else "✅ Safe"
            st.metric(
                label="AI Detection",
                value=ai_status,
                help="Detection result from AI camera"
            )

        with tab3:
            st.subheader("Emergency Button Log")
            emergency_status = "🚨 Active" if sensor_values["emergency"] == 1 else "✅ Inactive"
            st.metric(
                label="Emergency Status",
                value=emergency_status,
                help="Current state of the emergency button"
            )
    else:
        st.info("Click the refresh button to load sensor data.")

# About Page
elif menu == "About NeoCane":
    st.title("ℹ️ About NeoCane")
    st.markdown("""
    **NeoCane** is an AI & IoT-powered smart cane designed to assist the visually impaired in navigating safely.
    
    - Equipped with ultrasonic sensors and AI camera  
    - Detects obstacles and road holes  
    - Emergency button & haptic feedback via smart bracelet  
    """)
