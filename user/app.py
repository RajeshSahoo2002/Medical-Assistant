import streamlit as st
from components.upload import render_upload
from components.chatUI import render_chat
from components.download_history import render_download_history

st.set_page_config(page_title="HealthSage", layout="centered")
st.title("🩺 HealthSage: Your AI Assistant")

render_upload()
render_chat()
render_download_history()