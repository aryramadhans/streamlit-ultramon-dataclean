import streamlit as st

def display_home_page():
    st.title("Ultramon Data Cleaning Dashboard")
    # st.image("img/logo_ultramon.jpg", width=500)
    st.markdown("### Features:")
    st.write("1. Upload files to clean your data")
    st.write("2. Preview the cleaned data")
    st.write("3. Download the cleaned data")
    st.write("Start by navigating to **Data Cleaning** in the sidebar.")