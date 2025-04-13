import streamlit as st

st.success('This is a success message!', icon="✅")
st.error('No no no')
st.warning('hohoho')
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Distance", value="45 cm")

with col2:
    st.metric(label="AI Vision", value="Bahaya")

