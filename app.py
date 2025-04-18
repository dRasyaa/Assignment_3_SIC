import streamlit as st
import requests
import time
import os
from PIL import Image
 
# Konfigurasi Ubidots
TOKEN = "BBUS-dUnnmdDGegd40VNGBKuCOnpvAbO9eJ"
LABEL = "neocane-dashboard"
 
# Fungsi buat nge-fetch data
def load_sensor_value(token):
    my_headers = {"X-Auth-Token": TOKEN}
    url3 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kanan/lv"
    url4 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_kiri/lv"
    url5 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/jarak_tengah/lv"
    url6 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/ai_vision/lv"
 
    try:
        response_jarak_kanan = requests.get(url3, headers=my_headers)
        response_jarak_kiri = requests.get(url4, headers=my_headers)
        response_jarak_tengah = requests.get(url5, headers=my_headers)
        response_ai_vision = requests.get(url6, headers=my_headers)
 
        response_jarak_kiri.raise_for_status()
        response_jarak_tengah.raise_for_status()
        response_ai_vision.raise_for_status()
 
        jarak_kanan = float(response_jarak_kanan.text)
        jarak_tengah = float(response_jarak_tengah.text)
        jarak_kiri = float(response_jarak_kiri.text)
        ai_vision = int(float(response_ai_vision.text))
 
        return {
            "jarak_kanan": jarak_kanan,
            "jarak_tengah": jarak_tengah,
            "jarak_kiri": jarak_kiri,
            "ai_vision": ai_vision
        }
    except Exception as e:
        st.error(f"Failed to collect the data: {e}")
        return None
 
# Inisialisasi session_state buat sensor values
if "sensor_values" not in st.session_state:
    st.session_state.sensor_values = load_sensor_value(TOKEN)
 
# Sidebar Menu
st.sidebar.title("📂 NeoCane Menu")
menu = st.sidebar.radio("Select View:", ["🏠 Home", "📊 Data", "ℹ️ About NeoCane", "👉 About Us"])
 
# Home Page
if menu == "🏠 Home":
 
    # Tampilan Header
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to NeoCane 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-style: italic; color: #ccc;'>An AI & IoT-Based Smart Cane for the Visually Impaired</p>", unsafe_allow_html=True)
 
    # Tampilan Featured Features
    st.markdown("---")
    st.markdown("""
    <style>
    a {
    text-decoration: none !important;
    color: inherit !important;}
    .feature-box {
        background-color: #ff6b6b;
        color: white;
        width: 200px;
        height: 120px;
        border-radius: 20px;
        text-align: center;
        padding-top: 30px;
        display: inline-block;
        margin: 10px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-box:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
    }     
    .feature-box-purple {
        background-color: #8b5cf6;
    }
    .feature-box-blue {
        background-color: #3b82f6;
    }
    .feature-box-green {
        background-color: #10b981;
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
    }
    </style>
 
    <h2 style="text-align: center;">🍿 Featured Features ↔️</h2>
 
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
        <div class="feature-box">🔍<br>Object Detection</div>
        <div class="feature-box feature-box-purple">🤖<br>AI Vision</div>
        <div class="feature-box feature-box-blue">🚀<br>Photo History</div>
    </div>
 
    <p><div class="feature-box feature-box-green">📍<br>GPS Tracker</div></p>
    """, unsafe_allow_html=True)
 
    # Tampilan Additional Tools
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: white;'>🛠️ Additional Tools</h2>", unsafe_allow_html=True)
 
    colA, colB = st.columns(2)
 
    # EB Border
    with colA:
        st.markdown(
            """
            <style>
            .hover-box:hover {
                transform: scale(1.05);
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                transition: 0.3s ease;
            }
            </style>
            <p style='text-decoration: none;'>
            <div class='hover-box' style='background-color: #ff8c00; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 15px;'>
                <p style='font-size: 24px; color: white; margin: 0;'>🆘</p>
                <p style='font-size: 20px; color: white; margin: 5px 0 0 0;'>Emergency Button</p>
            </div>
            </p>
            """, unsafe_allow_html=True)
 
    # WB Border
    with colB:
        st.markdown(
            """
            <style>
            .hover-box:hover {
                transform: scale(1.05);
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                transition: 0.3s ease;
            }
            </style>
            <p style='text-decoration: none;'>
            <div class='hover-box' style='background-color: #28b886; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 15px;'>
                <p style='font-size: 24px; color: white; margin: 0;'>⌚</p>
                <p style='font-size: 20px; color: white; margin: 5px 0 0 0;'>Smart Wristband</p>
            </div>
            </p>
            """, unsafe_allow_html=True)
 
    # Tampilan Information Button
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: white;'>💁‍♂️ Information</h2>", unsafe_allow_html=True)
 
 
    for key in ["show_obj", "show_ai", "show_photo", "show_gps", "show_sos", "show_wrist"]:
        if key not in st.session_state:
            st.session_state[key] = False
 
 
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
 
    # OD
    with col1:
        if st.button("Object Detection Information"):
            st.session_state.show_obj = not st.session_state.show_obj
        if st.session_state.show_obj:
            st.info("This feature allows real-time object detection using a camera and AI model to assist users in identifying obstacles.")
 
    # AI
    with col2:
        if st.button("Ai Vision Information"):
            st.session_state.show_ai = not st.session_state.show_ai
        if st.session_state.show_ai:
            st.info("The AI Vision system recognizes environments, objects, and contexts for advanced navigation support.")
 
    # PH
    with col3:
        if st.button("Photo History Information"):
            st.session_state.show_photo = not st.session_state.show_photo
        if st.session_state.show_photo:
            st.info("Automatically stores the last 5 journey photos to help in emergency tracking or loss prevention")
 
    # GPS
    with col4:
        if st.button("GPS Tracker"):
            st.session_state.show_gps = not st.session_state.show_gps
        if st.session_state.show_gps:
            st.info("(COMING SOON) This feature allows real-time tracking of the user's location, providing safety and security.")
 
    # EB
    with col5:
        if st.button("Emergency Button"):
            st.session_state.show_sos = not st.session_state.show_sos
        if st.session_state.show_sos:
            st.info("(COMING SOON) Button that sends an alert to caregivers or monitoring systems in case of emergencies.")
 
    # WB
    with col6:
        if st.button("Smart Wristband"):
            st.session_state.show_wrist = not st.session_state.show_wrist
        if st.session_state.show_wrist:
            st.info("A tools to get feedback from the cane, providing haptic feedback and sound notification for obstacle detection.")
 
# Data Page
elif menu == "📊 Data":
    st.title('📊 Real-Time NeoCane Monitoring')
 
    # Refresh Button Umum
    if st.button("🔄 Refresh All Data"):
        with st.spinner("Refreshing..."):
            st.session_state.sensor_values = load_sensor_value(TOKEN)
            time.sleep(1)
 
    sensor_values = st.session_state.sensor_values
 
    if sensor_values:
        # 4 Tab Fitur
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Object Detection", "👁️ AI Vision", "📷 Photo History", "🗺️ GPS Tracking", "🆘 Emergency Log"])
 
        # Fitur Objek
        with tab1:
            st.subheader("Object Detection")
            if st.button("🧱 Refresh Detection"):
                st.rerun()
 
            right_distance = sensor_values["jarak_kanan"]
            middle_distance = sensor_values["jarak_tengah"]
            left_distance = sensor_values["jarak_kiri"]
 
            col1, col2, col3 = st.columns(3)
 
            # Sensor Kiri
            with col1:
                st.metric("⬅️ Left", f"{left_distance:.2f} cm")
                if left_distance == -1:
                    st.markdown("<h5 style='color: orange;'>❌ Sensor Error</h5>", unsafe_allow_html=True)
                elif left_distance < 100:
                    st.markdown("<h5 style='color: red;'>⚠️ Danger</h5>", unsafe_allow_html=True)
                else:
                    st.markdown("<h5 style='color: green;'>✅ Safe</h5>", unsafe_allow_html=True)
 
            # Sensor Depan
            with col2:
                st.metric("⬆️ Front", f"{middle_distance:.2f} cm")
                if middle_distance == -1:
                    st.markdown("<h5 style='color: orange;'>❌ Sensor Error</h5>", unsafe_allow_html=True)
                elif middle_distance < 100:
                    st.markdown("<h5 style='color: red;'>⚠️ Danger</h5>", unsafe_allow_html=True)
                else:
                    st.markdown("<h5 style='color: green;'>✅ Safe</h5>", unsafe_allow_html=True)
 
            # Sensor Kanan
            with col3:
                st.metric("➡️ Right", f"{right_distance:.2f} cm")
                if right_distance == -1:
                    st.markdown("<h5 style='color: orange;'>❌ Sensor Error</h5>", unsafe_allow_html=True)
                elif right_distance < 100:
                    st.markdown("<h5 style='color: red;'>⚠️ Danger</h5>", unsafe_allow_html=True)
                else:
                    st.markdown("<h5 style='color: green;'>✅ Safe</h5>", unsafe_allow_html=True)
 
 
        # Fitur AI Vision
        with tab2: 
            st.subheader("AI Vision")
 
            if st.button("🤖 Refresh AI Vision"):
                st.rerun() 
 
            if sensor_values["ai_vision"] == 1:
                st.error("🚧 Damaged road detected! Please proceed with caution.")
            else:
                st.success("✅ The path is safe.")
 
        # Fitur Photo History
        with tab3:
            st.subheader("📸 Photo History")
            st.markdown("Here are the last 5 photos captured by the ESP32-CAM.")
 
            if st.button("🌌 Refresh Gallery"):
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
 
        # Fitur GPS (Coming Soon)
        with tab4:
            st.subheader("🗺 GPS Tracking")
            st.markdown("GPS tracking feature is coming soon! Stay tuned for updates.")
 
        # Fitur Emergency Button (Coming Soon)
        with tab5:
            st.subheader("🆘 Emergency Log")
            st.markdown("Emergency log feature is coming soon! Stay tuned for updates.")
 
    else:
        st.error("❌ Failed to retrieve data from Ubidots")
 
# About Neocane Page
elif menu == "ℹ️ About NeoCane":
 
    # Penjelasan Neocane
    st.title("ℹ️ About NeoCane")
    st.markdown("""
    **NeoCane** is a smart cane powered by AI and IoT, designed to help visually impaired individuals navigate safely and independently.
 
    - Equipped with ultrasonic sensors to detect obstacles in three directions (left, front, and right)
    - Integrated with an AI-powered camera to detect road holes or damaged pathways
    - Real-time monitoring via Streamlit dashboard with intuitive alerts and status updates
    - Emergency button feature that sends immediate alerts to caregivers or monitoring systems
    - Smart wristband with haptic feedback for obstacle notifications without requiring visual attention
    - Designed with future expandability to support broader disabilities and advanced navigation features
 
    NeoCane empowers users with increased safety, confidence, and independence during everyday mobility.
    """)
 
    # Quotes
    st.markdown("<p style= 'text-align: center; font-weight: bold; color: white;'>Because the best help doesn't just come from the a smart device, it comes from one that cares </p>", unsafe_allow_html=True)
    st.markdown("<p style= 'text-align: center;'>-Semen 1 Roda</p>", unsafe_allow_html=True)
 
# About Us Page
elif menu == "👉 About Us":
 
    # Mendefinisikan anggota tim
    team_members = {
    "Anakya Danke Cetta Akhbar": {
        "photo": "https://raw.githubusercontent.com/denivorasya/neocane-dashboard/main/photo_member/Anakya.jpg",
        "job": "Sketch & Smart Wirstband",
        "quote": "Teknologi terbaik adalah yang mampu menyatukan manusia. -Matt Mullenweg"
    },
    "Bilal Khawarizmi": {
        "photo": "https://raw.githubusercontent.com/denivorasya/neocane-dashboard/main/photo_member/Bilal.jpg", 
        "job": "Streamlit & Ubidots Platform",
        "quote": "Di tengah kesulitan, selalu ada peluang. -Albert Einstein"
    },
    "Denivo Rasya Abiyyu": {
        "photo": "https://raw.githubusercontent.com/denivorasya/neocane-dashboard/main/photo_member/Denivo.jpg",
        "job": "Ai Vision & Obstacle Classification",
        "quote": "Kekuatan terbesar dari teknologi adalah ketika ia digunakan untuk memanusiakan manusia. -B.J Habibie"
    },
    "Rhaka Reza Rayvaldi": {
        "photo": "https://raw.githubusercontent.com/denivorasya/neocane-dashboard/main/photo_member/Rhaka.jpg",
        "job": "Sensor & Cane Equipment",
        "quote": "Inovasi adalah kemampuan melihat apa yang dilihat semua orang, tapi berpikir dengan cara yang berbeda. -Albert Szent-Györgyi"
    }
}
 
    st.title("🛞 Semen 1 Roda")
    st.markdown(""" 
    Kami adalah Semen 1 Roda, sebuah tim beranggotakan 4 siswa MAN Insan Cendekia Sumedang yang dipersatukan oleh semangat inovasi dan kepedulian sosial melalui proyek NeoCane — tongkat pintar berbasis AI dan IoT yang dirancang untuk membantu penyandang tunanetra dalam bernavigasi dengan aman dan mandiri.
 
    Kenapa “Semen 1 Roda”? 
    Karena kami percaya bahwa satu roda pun bisa membawa kami terus melaju. 
    Roda yang bulat menggambarkan kesatuan, kelancaran, dan kesinambungan seperti kami sebagai sebuah tim. Dengan satu visi, satu tekad, dan saling percaya, kami melaju bersama, menembus tantangan, dan menciptakan solusi nyata untuk masyarakat.
    """)
    st.markdown("---")
    st.header("👥 Anggota Tim")
 
 
    # Membuat tombol untuk setiap anggota
    cols = st.columns(4)
    for i, (name, data) in enumerate(team_members.items()):
        with cols[i]:
            if st.button(name.split()[0]):
                if st.session_state.get("selected_member") == name:
                    st.session_state.selected_member = None  # toggle OFF
                else:
                    st.session_state.selected_member = name  # toggle ON
 
    # Menampilkan foto dan info anggota yang dipilih
    if st.session_state.get('selected_member'):
        member = team_members[st.session_state.selected_member]
 
        col1, col2 = st.columns([1, 2])
 
        with col1:
            try:
                image = f"https://raw.githubusercontent.com/denivorasya/neocane-dashboard/main/photo_member/{member['photo']}"
                st.image(image, width=200) 
            except:
                st.warning("Foto tidak ditemukan")
 
        with col2:
            st.subheader(st.session_state.selected_member)
            st.markdown(f"""
            **Peran:** {member["job"]}  
            **Motivasi:** {member["quote"]}
            """)
    st.markdown("---")