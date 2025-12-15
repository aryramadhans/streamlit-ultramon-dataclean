"""
Session state management - handles session initialization and state reset
"""
import streamlit as st


def init_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'last_page' not in st.session_state:
        st.session_state.last_page = None
    if 'show_logout_confirm' not in st.session_state:
        st.session_state.show_logout_confirm = False
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'  # 'login' or 'register'


def reset_page_state():
    """Reset page-specific state when navigating"""
    if st.session_state.current_page != st.session_state.last_page:
        keys_to_remove = ['edit_mode', 'data_editor', 'merged_cleaned_data', 'download_format', 'file_name_input', 'uploaded_files']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.last_page = st.session_state.current_page
