import streamlit as st

def display_home_page():
    st.title("Welcome to the Data Cleaning Dashboard")
    st.write("Use the sidebar to navigate to the Data Cleaning page or other sections.")
    st.image("img/Telkom Indonesia.png", width=500)
    st.markdown("### Features:")
    st.write("- Upload and clean your CSV files")
    st.write("- Preview the cleaned data")
    st.write("- Download the cleaned data")
    st.write("Start by navigating to **Data Cleaning** in the sidebar.")