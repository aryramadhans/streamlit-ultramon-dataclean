"""
UI components - handles all frontend display logic
"""
import streamlit as st
from auth import validate_password, authenticate_user, register_user

def display_home_page():
    st.title("Ultramon Data Wrangler Dashboard")
    # st.image("img/logo_ultramon.jpg", width=500)
    st.markdown("### Features:")
    st.write("1. Upload files to clean your data")
    st.write("2. Preview the cleaned data")
    st.write("3. Download the cleaned data")
    st.write("Start by navigating to **Data Cleaning** in the sidebar.")

def display_login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pwd")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Login", use_container_width=True, type="primary", key="login_btn"):
            if not username or not password:
                st.error("Please enter username and password")
            elif authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Don't have an account? Register here", use_container_width=True, key="goto_register_btn"):
            st.session_state.auth_page = 'register'
            st.rerun()


def display_register_page():
    """Display registration page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Create Account</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username", key="reg_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="reg_pwd")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="reg_confirm")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Register", use_container_width=True, type="primary", key="reg_btn"):
            if not username or not password:
                st.error("Please fill all fields")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                is_valid, msg = validate_password(password)
                if is_valid:
                    success, msg = register_user(username, password)
                    if success:
                        st.success(msg)
                        # Clear form fields
                        st.session_state.reg_user = ""
                        st.session_state.reg_pwd = ""
                        st.session_state.reg_confirm = ""
                        st.info("Account created! Switching to login page...")
                        st.session_state.auth_page = 'login'
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.error(msg)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Already have an account? Login here", use_container_width=True, key="goto_login_btn"):
            st.session_state.auth_page = 'login'
            st.rerun()


def display_auth_page():
    """Display authentication page (login or register)"""
    if st.session_state.auth_page == 'register':
        display_register_page()
    else:
        display_login_page()


def setup_sidebar():
    """Setup sidebar with logo and title"""
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2:
        st.image("img/logo_ultramon.jpg", width=150)
    
    st.sidebar.markdown("<h3 style='text-align: center;'><b>CNOP DATA WRANGLER</b></h3>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <style>
            [data-testid="stSidebarContent"] button {
                text-align: center;
            }
            [data-testid="stSidebarContent"] .stButton {
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)


def display_user_info():
    """Display username and welcome message"""
    if 'username' in st.session_state:
        st.sidebar.markdown(f"<p style='text-align: center;'><b>Welcome, {st.session_state.username}!</b></p>", unsafe_allow_html=True)


def display_logout_button():
    """Display logout button"""
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True, key="logout_btn"):
        st.session_state.show_logout_confirm = True


def logout_confirmation():
    """Display logout confirmation dialog"""
    @st.dialog("Confirm Logout")
    def confirm_dialog():
        st.markdown("<h3 style='text-align: center;'>Are you sure?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes", use_container_width=True, key="logout_yes"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.show_logout_confirm = False
                st.rerun()
        with col2:
            if st.button("No", use_container_width=True, key="logout_no"):
                st.session_state.show_logout_confirm = False
                st.rerun()
    
    if st.session_state.show_logout_confirm:
        confirm_dialog()


def center_title(title):
    """Display centered title"""
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
