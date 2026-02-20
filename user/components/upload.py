import streamlit as st
from utils.api import upload_pdfs_api

def render_upload():
    #Below function is to create a sidebar in the main homepage
    st.sidebar.header("📁 Upload Medical Documents .(PDFs)")
    uploaded_files=st.sidebar.file_uploader("upload multiple medical pdfs",accept_multiple_files=True)
    if st.sidebar.button("Upload DB") and uploaded_files:
        #Below response variable is capturing the response from upload_pdf/api when hit both incase of failure and success and displaying the message to the user accordingly
        response=upload_pdfs_api(uploaded_files)
        if response.status_code==200:
            st.sidebar.success("✅ Files uploaded successfully")
        else:
            st.sidebar.error(f"❌ Error:{response.text}")
        