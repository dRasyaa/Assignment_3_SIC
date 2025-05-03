import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import time
import os
from PIL import Image
from sklearn.cluster import DBSCAN
import numpy as np
import opencv as cv2
import plotly.express as px

st.set_page_config(
    page_title="NeoCane Dashboard",     
    page_icon="🦯",                       
    layout="wide",                        
    initial_sidebar_state="auto",         
)
 
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
    url7 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/face_recognition/lv"
    url8 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/longitude/lv"
    url9 = f"https://industrial.api.ubidots.com/api/v1.6/devices/{LABEL}/latitude/lv"
 
    try:
        response_jarak_kanan = requests.get(url3, headers=my_headers)
        response_jarak_kiri = requests.get(url4, headers=my_headers)
        response_jarak_tengah = requests.get(url5, headers=my_headers)
        response_ai_vision = requests.get(url6, headers=my_headers)
        response_face_recognition = requests.get(url7, headers=my_headers)
        response_longitude = requests.get(url8, headers=my_headers)
        response_latitude = requests.get(url9, headers=my_headers)  
 
        response_jarak_kanan.raise_for_status()
        response_jarak_kiri.raise_for_status()
        response_jarak_tengah.raise_for_status()
        response_ai_vision.raise_for_status()
        response_face_recognition.raise_for_status()
        response_longitude.raise_for_status()
        response_latitude.raise_for_status()
 
        jarak_kanan = float(response_jarak_kanan.text)
        jarak_tengah = float(response_jarak_tengah.text)
        jarak_kiri = float(response_jarak_kiri.text)
        ai_vision = int(float(response_ai_vision.text))
        face_recognition = int(float(response_face_recognition.text))
        longitude = float(response_longitude.text)
        latitude = float(response_latitude.text)
 
        return {
            "jarak_kanan": jarak_kanan,
            "jarak_tengah": jarak_tengah,
            "jarak_kiri": jarak_kiri,
            "ai_vision": ai_vision,
            "face_recognition": face_recognition,
            "longitude": longitude,
            "latitude" : latitude
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
    # Di bagian Featured Features (ganti yang existing):
    st.markdown("""
    <style>
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
    .feature-box-purple { background-color: #8b5cf6; }
    .feature-box-blue { background-color: #3b82f6; }
    .feature-box-green { background-color: #10b981; }
    .feature-box-pink { background-color: #ec4899; }
    .feature-box-orange { background-color: #f97316; }
    </style>

    <h2 style="text-align: center;">🍿 Featured Features ↔️</h2>

    <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
        <div class="feature-box">🔍<br>Object Detection</div>
        <div class="feature-box feature-box-purple">🤖<br>AI Vision</div>
        <div class="feature-box feature-box-blue">🚀<br>Photo History</div>
        <div class="feature-box feature-box-green">📍<br>GPS Tracker</div>
        <div class="feature-box feature-box-pink">😀<br>Face Recognition</div>
        <div class="feature-box feature-box-orange">🆘<br>Emergency Log</div>
    </div>
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
        # Tampilan Information Button
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: white;'>💁‍♂️ Information</h2>", unsafe_allow_html=True)

    # Buat 3 baris dengan 3 kolom per baris
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    row3_col1, row3_col2 = st.columns([1, 2])  # Baris khusus untuk Emergency Log

    # Baris 1
    with row1_col1:
        if st.button("Object Detection Information"):
            st.session_state.show_obj = not st.session_state.get("show_obj", False)
        if st.session_state.get("show_obj"):
            st.info("Real-time object detection using ultrasonic sensors")

    with row1_col2:
        if st.button("Ai Vision Information"):
            st.session_state.show_ai = not st.session_state.get("show_ai", False)
        if st.session_state.get("show_ai"):
            st.info("Analyzes road conditions using computer vision")

    with row1_col3:
        if st.button("Photo History Information"):
            st.session_state.show_photo = not st.session_state.get("show_photo", False)
        if st.session_state.get("show_photo"):
            st.info("Stores journey photos for emergency reference")

    # Baris 2
    with row2_col1:
        if st.button("GPS Tracker Information"):
            st.session_state.show_gps = not st.session_state.get("show_gps", False)
        if st.session_state.get("show_gps"):
            st.info("Real-time tracking of user's location")

    with row2_col2:
        if st.button("Emergency Button Information"):
            st.session_state.show_sos = not st.session_state.get("show_sos", False)
        if st.session_state.get("show_sos"):
            st.info("Sends alerts to caregivers")

    with row2_col3:
        if st.button("Smart Wristband Information"):
            st.session_state.show_wrist = not st.session_state.get("show_wrist", False)
        if st.session_state.get("show_wrist"):
            st.info("Haptic feedback for obstacle detection")

    # Baris 3 - Khusus Face Recognition dan Emergency Log
    with row3_col1:
        if st.button("Face Recognition Information"):
            st.session_state.show_face = not st.session_state.get("show_face", False)
        if st.session_state.get("show_face"):
            st.info("Identifies registered family members")

    with row3_col2:
        if st.button("Emergency Log Information", key="emergency_log_button"):
            st.session_state.show_emergency = not st.session_state.get("show_emergency", False)
        if st.session_state.get("show_emergency"):
            st.info("Records emergency events with timestamps and locations")
 
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
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔎 Object Detection", "👁️ AI Vision", "📷 Photo History","😀 Family Face Recognition", "🗺️ GPS Tracking", "🆘 Emergency Log"])
 
        # Fitur Objek
        with tab1:
            st.subheader("🏯 Object Detection")
            
            # Initialize detection log with all sensors
            if "detection_log" not in st.session_state:
                st.session_state.detection_log = pd.DataFrame(columns=['timestamp', 'sensor', 'distance', 'status'])
                # Initialize with all sensors
                current_time = pd.Timestamp.now()
                for sensor in ['Left', 'Front', 'Right']:
                    st.session_state.detection_log = pd.concat([
                        st.session_state.detection_log,
                        pd.DataFrame({
                            'timestamp': [current_time],
                            'sensor': [sensor],
                            'distance': [0],
                            'status': ['Initializing']
                        })
                    ], ignore_index=True)

            if st.button("🧱 Refresh Detection"):
                st.rerun()

            # Get current sensor values
            right_distance = sensor_values["jarak_kanan"]
            middle_distance = sensor_values["jarak_tengah"]
            left_distance = sensor_values["jarak_kiri"]
            current_time = pd.Timestamp.now()

            # Enhanced status function
            def get_status(distance):
                if distance == -1:
                    return ("Sensor Error", "orange")
                elif distance < 50:
                    return ("Critical Danger", "darkred")
                elif distance < 100:
                    return ("Danger", "red")
                else:
                    return ("Safe", "green")

            col1, col2, col3 = st.columns(3)

            # Sensor processing function
            def process_sensor(sensor_name, distance, col):
                status, color = get_status(distance)
                
                with col:
                    # Enhanced metric display
                    st.metric(
                        label=f"🔵 {sensor_name}",
                        value=f"{distance:.1f} cm",
                    )
                    
                    # Status indicator with icon
                    status_icon = "⚠️" if "Danger" in status else "✅" if "Safe" in status else "❌"
                    st.markdown(
                        f"""<div style='background-color:#{color}20; padding:10px; border-radius:10px; 
                            border-left:5px solid {color}; text-align:center'>
                            <h4 style='color:{color}; margin:0;'>{status_icon} {status}</h4>
                        </div>""",
                        unsafe_allow_html=True
                    )
                
                # Log every reading (not just changes)
                new_log = pd.DataFrame({
                    'timestamp': [current_time],
                    'sensor': [sensor_name],
                    'distance': [distance],
                    'status': [status]
                })
                st.session_state.detection_log = pd.concat([st.session_state.detection_log, new_log], ignore_index=True)

            # Process all sensors
            process_sensor("Left", left_distance, col1)
            process_sensor("Front", middle_distance, col2)
            process_sensor("Right", right_distance, col3)

            # Enhanced detection log
            st.markdown("### 📜 Detection History")
            
            if len(st.session_state.detection_log) > 0:
                # Get last 10 unique entries per sensor
                recent_logs = st.session_state.detection_log.sort_values('timestamp', ascending=False)
                recent_logs = recent_logs.drop_duplicates(['sensor', 'status'], keep='first')
                
                # Format display
                display_log = recent_logs.head(30).copy()
                display_log['Time'] = display_log['timestamp'].dt.strftime('%H:%M:%S')
                display_log['Duration'] = display_log.groupby('sensor')['timestamp'].diff().dt.total_seconds().fillna(0)
                display_log['Duration'] = display_log['Duration'].apply(
                    lambda x: f"{int(x//3600)}h {int((x%3600)//60)}m {int(x%60)}s" if x > 60 else f"{int(x)}s"
                )

                # Color coding
                def color_status(status):
                    if "Danger" in status: return "red"
                    elif "Safe" in status: return "green"
                    else: return "orange"
                
                # Display table
                st.dataframe(
                    display_log.sort_values('timestamp', ascending=False)[['Time', 'sensor', 'distance', 'status', 'Duration']],
                    column_config={
                        "Time": "🕒 Time",
                        "sensor": "📍 Sensor",
                        "distance": "📏 Distance (cm)",
                        "status": st.column_config.TextColumn(
                            "🛡️ Status",
                            help="Safety status of detection",
                            width="medium"
                        ),
                        "Duration": "⏱️ Since Last Change"
                    },
                    use_container_width=True,
                    hide_index=True,
                    column_order=["Time", "sensor", "distance", "status", "Duration"]
                )

                # Enhanced visualization
                st.markdown("### 📊 Detection Patterns")
                
                tab_a, tab_b = st.tabs(["Timeline", "Statistics"])
                
                with tab_a:
                    fig = px.scatter(
                        display_log,
                        x='timestamp',
                        y='distance',
                        color='sensor',
                        symbol='status',
                        title='Object Detection Timeline',
                        labels={'distance': 'Distance (cm)', 'timestamp': 'Time'},
                        hover_data=['Duration'],
                        color_discrete_map={
                            'Left': '#636EFA',
                            'Front': '#EF553B', 
                            'Right': '#00CC96'
                        }
                    )
                    fig.update_layout(
                        hovermode="x unified",
                        xaxis_title="Time",
                        yaxis_title="Distance (cm)",
                        legend_title="Sensor"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab_b:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Detections", len(st.session_state.detection_log))
                        danger_count = len(st.session_state.detection_log[st.session_state.detection_log['status'].str.contains('Danger')])
                        st.metric("Danger Alerts", danger_count)
                    
                    with col2:
                        avg_distance = st.session_state.detection_log['distance'].mean()
                        st.metric("Average Distance", f"{avg_distance:.1f} cm")
                        last_alert = st.session_state.detection_log[st.session_state.detection_log['status'].str.contains('Danger')]['timestamp'].max()
                        st.metric("Last Alert", last_alert.strftime('%H:%M:%S') if not pd.isnull(last_alert) else "None")
            else:
                st.info("No detection history yet. Sensors are initializing...")

            # Raw data debug (can be commented out in production)
            with st.expander("Debug: Raw Sensor Data"):
                st.write("Latest sensor values:", sensor_values)
                st.write("Full detection log:", st.session_state.detection_log)
                # Fitur AI Vision
        with tab2:
            st.subheader("🛣️ AI Vision - Jalan")
            
            # 1. Initialize session_state untuk simpan semua data
            if "road_history" not in st.session_state:
                st.session_state.road_history = pd.DataFrame(columns=["timestamp", "status", "latitude", "longitude"])
            
            # 2. Ambil data sensor terbaru
            ai_status = sensor_values["ai_vision"]  # 0 = Aman, 1 = Bahaya
            current_time = pd.Timestamp.now()
            
            # 3. Tambahkan data baru ke history
            new_entry = pd.DataFrame({
                "timestamp": [current_time],
                "status": ["Aman" if ai_status == 0 else "Bahaya"],
                "latitude": [sensor_values["latitude"]],
                "longitude": [sensor_values["longitude"]]
            })
            
            st.session_state.road_history = pd.concat(
                [st.session_state.road_history, new_entry], 
                ignore_index=True
            )
            
            # 4. Tampilkan status terkini (sama seperti sebelumnya)
            col_status, col_action = st.columns([1, 3])
            with col_status:
                if ai_status == 0:
                    st.success("✅ Jalan Aman")
                else:
                    st.error("🚧 Jalan Bermasalah")
            
            with col_action:
                if ai_status == 0:
                    st.markdown("**Kondisi:** Permukaan jalan normal")
                else:
                    st.markdown("**Peringatan:** Deteksi lubang/retakan!")
                    st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3"></audio>""", 
                            unsafe_allow_html=True)
            
            # 5. Tabel 5 Data Terakhir
            st.markdown("### 📋 5 Deteksi Terakhir")
            st.dataframe(
                st.session_state.road_history.sort_values("timestamp", ascending=False).head(5),
                column_config={
                    "timestamp": "Waktu",
                    "status": "Status",
                    "latitude": "Latitude",
                    "longitude": "Longitude"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # 6. Grafik History (Semua Data)
            st.markdown("### 📊 Trend Deteksi Jalan")
            if len(st.session_state.road_history) > 1:
                # Hitung jumlah insiden per menit
                df_plot = st.session_state.road_history.copy()
                df_plot["time_bin"] = df_plot["timestamp"].dt.floor("5min")  # Kelompokkan per 5 menit
                df_plot = df_plot[df_plot["status"] == "Bahaya"].groupby("time_bin").size().reset_index(name="count")
                
                fig = px.line(
                    df_plot, 
                    x="time_bin", 
                    y="count",
                    title="Frekuensi Jalan Bermasalah",
                    labels={"time_bin": "Waktu", "count": "Jumlah Insiden"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Belum ada cukup data untuk grafik")
            
            # 7. Opsi Download Full Data
            st.download_button(
                label="⬇️ Download Full History (CSV)",
                data=st.session_state.road_history.to_csv(index=False),
                file_name="neocane_road_history.csv",
                mime="text/csv"
            )
 
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
        
        with tab4:
            st.subheader("👨‍👩‍👧‍👦 Family Face Recognition")
            
            # Get face recognition status from Ubidots
            face_status = sensor_values["face_recognition"]
            
            if st.button("🌪️ Refresh Face Recognition"):
                st.rerun()
            
            # Display status
            if face_status == 1:
                st.success("## ✅ Family Member Detected")
                st.balloons()
                st.markdown("""
                <audio autoplay>
                <source src="https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3">
                </audio>
                """, unsafe_allow_html=True)
            else:
                st.warning("## ❌ No Family Member Detected")
                st.markdown("""
                <audio autoplay>
                <source src="https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3">
                </audio>
                """, unsafe_allow_html=True)
            
            # Debug info
            with st.expander("🔧 Technical Details"):
                st.write(f"Raw face_recognition value from Ubidots: {face_status}")
                st.write("0 = Unknown, 1 = Family")
            
        with tab5:
            st.subheader("🗺 GPS Tracking & Frequent Locations")
            
            # Refresh Button
            if st.button("📍 Refresh GPS Data"):
                st.session_state.sensor_values = load_sensor_value(TOKEN)
                sensor_values = st.session_state.sensor_values
            
            # Current Location
            latitude = sensor_values["latitude"]
            longitude = sensor_values["longitude"]
            st.write(f"**Current Location:** ({latitude}, {longitude})")
            
            # Peta Real-Time
            st.markdown("### 🌍 Live Location")
            st.map(pd.DataFrame({'lat': [latitude], 'lon': [longitude]}))
            
            # Simpan riwayat GPS ke session_state
            if "gps_history" not in st.session_state:
                st.session_state.gps_history = []
                st.session_state.location_history = pd.DataFrame(columns=['timestamp', 'lat', 'lon'])
            
            # Tambahkan lokasi baru ke history 
            new_location = (latitude, longitude)
            current_time = pd.Timestamp.now()
            
            # Cek jika lokasi berbeda dari sebelumnya atau sudah 1 menit berlalu
            if (len(st.session_state.gps_history) == 0 or 
                new_location != st.session_state.gps_history[-1] or
                (current_time - pd.to_datetime(st.session_state.location_history['timestamp'].iloc[-1])).seconds > 60 if len(st.session_state.location_history) > 0 else True):
                
                st.session_state.gps_history.append(new_location)
                new_entry = pd.DataFrame({
                    'timestamp': [current_time],
                    'lat': [latitude],
                    'lon': [longitude]
                })
                st.session_state.location_history = pd.concat([st.session_state.location_history, new_entry], ignore_index=True)
            
            # Tampilkan Travel Log
            # Tampilkan Travel Log
                st.markdown("### 🚶 Travel Log")

                if len(st.session_state.location_history) > 0:
                    # Hitung waktu antara titik-titik (tidak perlu disimpan di dataframe)
                    time_diff = st.session_state.location_history['timestamp'].diff().dt.total_seconds().fillna(0)
                    
                    # Format waktu untuk display
                    display_df = st.session_state.location_history.copy()
                    display_df['Time'] = display_df['timestamp'].dt.strftime('%H:%M:%S')  # Format jam:menit:detik
                    display_df['Time Since Last'] = time_diff.apply(lambda x: f"{int(x)} detik" if x < 60 else f"{int(x/60)} menit")
                    
                    # Tampilkan tabel perjalanan (tanpa kolom speed dan time_elapsed)
                    st.dataframe(
                        display_df.sort_values('timestamp', ascending=False).head(10)[['Time', 'lat', 'lon', 'Time Since Last']],
                        column_config={
                            "Time": "Waktu Pencatatan",
                            "lat": "Latitude",
                            "lon": "Longitude",
                            "Time Since Last": "Selisih Waktu"
                        },
                        use_container_width=True
                    )
                
                # Visualisasi rute perjalanan
                st.markdown("### 🛣️ Travel Route")
                if len(st.session_state.location_history) > 1:
                    st.pydeck_chart(pdk.Deck(
                        map_style='mapbox://styles/mapbox/light-v9',
                        initial_view_state=pdk.ViewState(
                            latitude=latitude,
                            longitude=longitude,
                            zoom=13
                        ),
                        layers=[
                            pdk.Layer(
                                'PathLayer',
                                data=st.session_state.location_history,
                                get_path=['[lon, lat]'],
                                get_color='[200, 30, 0, 160]',
                                get_width=5,
                                pickable=True
                            ),
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=st.session_state.location_history,
                                get_position=['lon', 'lat'],
                                get_color='[0, 140, 255, 200]',
                                get_radius=100,
                                pickable=True
                            )
                        ]
                    ))
            
            # Analisis Tempat Favorit
            st.markdown("### ⭐ Frequently Visited Places")
            
            # Deteksi tempat favorit (jika ada minimal 5 data)
            if len(st.session_state.gps_history) > 5:
                # Konversi ke numpy array
                coords = np.array(st.session_state.gps_history)
                
                # Clustering dengan DBSCAN 
                kms_per_radian = 6371.0088
                epsilon = 0.05 / kms_per_radian  
                
                db = DBSCAN(
                    eps=epsilon, 
                    min_samples=3,  
                    metric='haversine'
                ).fit(np.radians(coords))
                
                # Hitung frekuensi kunjungan per cluster
                clusters = pd.Series(db.labels_)
                freq_spots = clusters.value_counts().reset_index()
                freq_spots.columns = ['cluster_id', 'visit_count']
                
                # Ambil centroid tiap cluster
                freq_spots['lat'] = freq_spots['cluster_id'].apply(
                    lambda x: coords[clusters == x][:, 0].mean()
                )
                freq_spots['lon'] = freq_spots['cluster_id'].apply(
                    lambda x: coords[clusters == x][:, 1].mean()
                )
                
                # Filter cluster valid (bukan noise)
                freq_spots = freq_spots[freq_spots['cluster_id'] != -1]
                
                # Tampilkan hasil
                if not freq_spots.empty:
                    st.success(f"Found {len(freq_spots)} frequent locations!")
                    
                    # Tabel ranking
                    st.dataframe(
                        freq_spots.sort_values('visit_count', ascending=False)
                        .reset_index(drop=True)
                        .style.background_gradient(cmap='YlOrRd'),
                        column_config={
                            "lat": "Latitude",
                            "lon": "Longitude",
                            "visit_count": "Total Visits"
                        }
                    )
                    
                    # Peta heatmap
                    st.pydeck_chart(pdk.Deck(
                        map_style='mapbox://styles/mapbox/light-v9',
                        initial_view_state=pdk.ViewState(
                            latitude=latitude,
                            longitude=longitude,
                            zoom=13
                        ),
                        layers=[
                            pdk.Layer(
                                'HeatmapLayer',
                                data=freq_spots,
                                get_position=['lon', 'lat'],
                                get_weight='visit_count',
                                radius=100,
                                intensity=1
                            )
                        ]
                    ))
                    
                    # Analisis pola perjalanan
                    st.markdown("### 🧭 Travel Patterns")
                    
                    # Hitung waktu yang dihabiskan di setiap lokasi favorit
                    if len(st.session_state.location_history) > 1:
                        # Gabungkan data lokasi dengan cluster
                        location_df = st.session_state.location_history.copy()
                        location_df['cluster'] = db.labels_
                        
                        # Hitung waktu yang dihabiskan di setiap cluster
                        cluster_time = location_df[location_df['cluster'] != -1].groupby('cluster')['time_elapsed'].sum().reset_index()
                        cluster_time = cluster_time.merge(freq_spots, left_on='cluster', right_on='cluster_id')
                        
                        # Tampilkan sebagai pie chart
                        fig = px.pie(cluster_time, 
                                    values='time_elapsed', 
                                    names='cluster_id',
                                    title='Time Spent at Each Frequent Location',
                                    hover_data=['lat', 'lon'])
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No frequent locations detected yet.")
            else:
                st.info("Collecting more location data... (min 5 locations needed)")
                    
                # Fitur Emergency Button (Coming Soon)
                with tab6:
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
        "photo": "Anakya.jpg",
        "job": "Sketch & Smart Wirstband",
        "quote": "Teknologi terbaik adalah yang mampu menyatukan manusia. -Matt Mullenweg"
    },
    "Bilal Khawarizmi": {
        "photo": "Bilal.jpg", 
        "job": "Streamlit & Ubidots Platform",
        "quote": "Di tengah kesulitan, selalu ada peluang. -Albert Einstein"
    },
    "Denivo Rasya Abiyyu": {
        "photo": "Denivo.jpg",
        "job": "Ai Vision & Obstacle Classification",
        "quote": "Kekuatan terbesar dari teknologi adalah ketika ia digunakan untuk memanusiakan manusia. -B.J Habibie"
    },
    "Rhaka Reza Rayvaldi": {
        "photo": "Rhaka.jpg",
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
                image = f"https://raw.githubusercontent.com/dRasyaa/Assignment_3_SIC/refs/heads/main/photo_member/{member['photo']}"
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