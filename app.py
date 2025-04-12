import streamlit as st
import pandas as pd
import numpy as np
import requests

# Sidebar Menu
st.sidebar.title("📂 NeoCane Menu")
menu = st.sidebar.radio("Select View:", ["Home", "Data", "About NeoCane"])

# Home Page
if menu == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to NeoCane</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>_An AI & IoT-Based Smart Cane for the Visually Impaired_</p>", unsafe_allow_html=True)

# Data Page
elif menu == "Data":
    tab1, tab2, tab3 = st.tabs(["Object Detection", "AI Vision", "Emergency Log"])

    with tab1:
        st.subheader("Object Detection")
        st.metric(
            label="Distance",
            value="45 cm",
            delta="-5 cm",
            delta_color="inverse",
            help="Distance measured by ultrasonic sensor"
        )

    with tab2:
        st.subheader("AI Vision")
        st.metric(
            label="AI Detection",
            value="Critical Hole",
            help="Detection result from AI camera"
        )

    with tab3:
        st.subheader("Emergency Button Log")
        st.metric(
            label="Emergency Status",
            value="Active",
            help="Current state of the emergency button"
        )

# About Page
elif menu == "About NeoCane":
    st.title("ℹ️ About NeoCane")
    st.markdown("""
    **NeoCane** is an AI & IoT-powered smart cane designed to assist the visually impaired in navigating safely.
    
    - Equipped with ultrasonic sensors and AI camera
    - Detects obstacles and road holes
    - Emergency button & haptic feedback via smart bracelet
    """)
