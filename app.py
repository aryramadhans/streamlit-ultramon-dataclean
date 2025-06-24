import streamlit as st
from dashboard_logic import display_data_cleaning_page, genie_clean, genie_p95, genie_ref_clean, ultramon, zabbix_clean
from dashboard_view import display_home_page

# Streamlit app configuration
st.set_page_config(page_title="Ultramon Data Cleaning Dashboard", layout="wide", page_icon="img/logo_ultramon.jpg")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar setup
st.sidebar.markdown(
    """
    <style>
        .sidebar.sidebar-content {
            padding-top: 0;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 0px;
        }
        .logo-container img {
            width: auto;
            height: auto;
        }
    </style>
    <div class="logo-container">
        <img src="img/logo_ultramon.jpg" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("**ULTRAMON DATA CLEANING DASHBOARD**", divider="orange", )

# Sidebar for navigation
homepage_btn = st.sidebar.button("Home", use_container_width=True, key="homepage_btn")

st.sidebar.subheader("**Data Cleaning**")
with st.sidebar.expander("**ULTRAMON**", expanded=False):
    ultramon_btn = st.button("Backbone", use_container_width=True, key="ultramon_btn")
    ultramon_ref_btn = st.button("Reference", use_container_width=True, key="ultramon_ref_btn")

with st.sidebar.expander("**GENIE**", expanded=False):
    genie_atom_btn = st.button("ATOM", use_container_width=True, key="genie_atom_btn")
    genie_nonatom_btn = st.button("NON-ATOM", use_container_width=True, key="genie_nonatom_btn")
    genie_p95_btn = st.button("P95 Data Cleaning", use_container_width=True, key="genie_p95_btn")
    genie_ref_btn = st.button("Reference", use_container_width=True, key="genie_ref_btn")

with st.sidebar.expander("**ZABBIX**", expanded=False):
    zabbix_btn = st.button("ATOM", use_container_width=True, key="zabbix_btn")
    zabbix_ref_btn = st.button("Reference", use_container_width=True, key="zabbix_ref_btn")

st.sidebar.subheader("**TREATMENT**")
pemobile_btn = st.sidebar.button("PE-MOBILE (HR)", use_container_width=True, key="pemobile_btn")
petransit_btn = st.sidebar.button("PE-TRANSIT (IX)", use_container_width=True, key="petransit_btn")

# Handle Navigation
if homepage_btn:
    st.session_state.current_page = 'home'
elif ultramon_btn:
    st.session_state.current_page = 'ultramon'
elif ultramon_ref_btn:
    st.session_state.current_page = 'ultramon_ref'
elif genie_atom_btn or genie_nonatom_btn:
    st.session_state.current_page = 'genie_clean'
elif genie_p95_btn:
    st.session_state.current_page = 'genie_p95'
elif genie_ref_btn:
    st.session_state.current_page = 'genie_ref'
elif zabbix_btn:
    st.session_state.current_page = 'zabbix_clean'
elif zabbix_ref_btn:
    st.session_state.current_page = 'zabbix_ref'
elif pemobile_btn:
    st.session_state.current_page = 'pemobile'
elif petransit_btn:
    st.session_state.current_page = 'petransit'

# Display current page
if st.session_state.current_page == 'home':
    st.empty()
    display_home_page()
elif st.session_state.current_page == 'ultramon':
    st.title("Ultramon Data Cleaning")
    display_data_cleaning_page(ultramon)
elif st.session_state.current_page == 'ultramon_ref':
    st.title("Ultramon Reference")
    # Add Ultramon reference content here
elif st.session_state.current_page == 'genie_clean':
    st.title("Genie Data Cleaning")
    display_data_cleaning_page(genie_clean)
elif st.session_state.current_page == 'genie_p95':
    st.title("Genie P95 Data")
    display_data_cleaning_page(genie_p95)
elif st.session_state.current_page == 'genie_ref':
    st.title("Genie Reference")
    display_data_cleaning_page(genie_ref_clean)
elif st.session_state.current_page == 'zabbix_clean':
    st.title("Zabbix Data Cleaning")
    display_data_cleaning_page(zabbix_clean)
elif st.session_state.current_page == 'zabbix_ref':
    st.title("Zabbix Reference")
    # Add Zabbix reference content here
elif st.session_state.current_page == 'pemobile':
    st.title("PE-MOBILE Treatment Check")
    # Add treatment check content here
elif st.session_state.current_page == 'petransit':
    st.title("PE-TRANSIT Treatment Check")
    # Add treatment check content here