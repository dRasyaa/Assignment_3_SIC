import streamlit as st

st.success('This is a success message!', icon="✅")
st.error('No no no')
st.warning('hohoho')
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Distance", value="45 cm")

with col2:
    st.metric(label="AI Vision", value="Bahaya")

st.metric(
    label="Distance",
    value= f"{20} cm",
    delta=f"{-5} cm",
    delta_color="inverse",
    help="Distance measured by ultrasonic sensor"
)

st.metric(
    label= "Distance",
    value= f"{20} cm",
    delta=f"{-5} cm",
    delta_color="inverse",
    help="Distance measured by ultrasonic sensor"
)

st.metric(
    label= "Distance",
    value= f"{20} cm",
    delta=f"{-5} cm",
    delta_color="inverse",
    help="Distance measured by ultrasonic sensor"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="⬅️ Left", value=f"{20} cm")

with col2:
    st.metric(label="⬆️ Front", value=f"{20} cm")

with col3:
    st.metric(label="➡️ Right", value=f"{20} cm")