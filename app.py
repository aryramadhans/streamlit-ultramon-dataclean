import streamlit as st
from dashboard_logic import display_data_cleaning_page, ultramon_genie_clean, genie_clean, genie_p95, genie_ref_clean, ultramon, zabbix_clean
from dashboard_view import display_home_page

# ==================== Configuration ====================
st.set_page_config(page_title="CNOP Data Cleaning Services", layout="wide", page_icon="img/logo_ultramon.jpg")

# ==================== Sidebar Setup ====================
st.sidebar.markdown(
    """
    <style>
        .sidebar.sidebar-content { padding-top: 0; }
        .logo-container { text-align: left; margin-bottom: 0px; }
        .logo-container img { width: auto; height: auto; }
    </style>
    <div class="logo-container">
        <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("**CNOP DATA CLEANING**", divider="orange")

# ==================== Navigation Menu ====================
def render_sidebar_menu():
    """Create sidebar navigation menu"""
    pages = {}
    
    # Home button
    if st.sidebar.button("Home", use_container_width=True, key="homepage_btn"):
        pages['home'] = True
    
    # ULTRAMON section
    with st.sidebar.expander("**ULTRAMON**", expanded=False):
        if st.button("Backbone", use_container_width=True, key="ultramon_btn"):
            pages['ultramon'] = True
        if st.button("UltraGen P95", use_container_width=True, key="ultramon_gen_btn"):
            pages['ultramon_genie'] = True
        if st.button("Reference", use_container_width=True, key="ultramon_ref_btn"):
            pages['ultramon_ref'] = True
    
    # GENIE section
    with st.sidebar.expander("**GENIE**", expanded=False):
        if st.button("ATOM", use_container_width=True, key="genie_atom_btn"):
            pages['genie_clean'] = True
        if st.button("NON-ATOM", use_container_width=True, key="genie_nonatom_btn"):
            pages['genie_clean'] = True
        if st.button("P95 Data Cleaning", use_container_width=True, key="genie_p95_btn"):
            pages['genie_p95'] = True
        if st.button("Reference", use_container_width=True, key="genie_ref_btn"):
            pages['genie_ref'] = True
    
    # ZABBIX section
    with st.sidebar.expander("**ZABBIX**", expanded=False):
        if st.button("ATOM", use_container_width=True, key="zabbix_btn"):
            pages['zabbix_clean'] = True
        if st.button("Reference", use_container_width=True, key="zabbix_ref_btn"):
            pages['zabbix_ref'] = True
    
    # TREATMENT section
    st.sidebar.subheader("**TREATMENT**")
    if st.sidebar.button("PE-MOBILE (HR)", use_container_width=True, key="pemobile_btn"):
        pages['pemobile'] = True
    if st.sidebar.button("PE-TRANSIT (IX)", use_container_width=True, key="petransit_btn"):
        pages['petransit'] = True
    
    return pages

# ==================== Session State Management ====================
def init_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
        st.session_state.last_page = None

def reset_page_state():
    """Reset page-specific state when navigating"""
    if st.session_state.current_page != st.session_state.last_page:
        keys_to_remove = ['edit_mode', 'data_editor', 'merged_cleaned_data', 'download_format', 'file_name_input', 'uploaded_files']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.last_page = st.session_state.current_page

# ==================== Page Display ====================
def center_title(title):
    """Display centered title"""
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)

# Page configuration mapping
PAGES = {
    'home': {'title': '', 'func': display_home_page, 'data_func': None},
    'ultramon': {'title': 'ULTRAMON DATA CLEANING', 'func': display_data_cleaning_page, 'data_func': ultramon},
    'ultramon_genie': {'title': 'ULTRAMON x GENIE P95 DATA CLEANING', 'func': display_data_cleaning_page, 'data_func': ultramon_genie_clean},
    'ultramon_ref': {'title': 'ULTRAMON REFERENCE CLEANING', 'func': None, 'data_func': None},
    'genie_clean': {'title': 'GENIE DATA CLEANING', 'func': display_data_cleaning_page, 'data_func': genie_clean},
    'genie_p95': {'title': 'GENIE P95 DATA', 'func': display_data_cleaning_page, 'data_func': genie_p95},
    'genie_ref': {'title': 'GENIE REFERENCE', 'func': display_data_cleaning_page, 'data_func': genie_ref_clean},
    'zabbix_clean': {'title': 'ZABBIX DATA CLEANING', 'func': display_data_cleaning_page, 'data_func': zabbix_clean},
    'zabbix_ref': {'title': 'ZABBIX REFERENCE', 'func': None, 'data_func': None},
    'pemobile': {'title': 'PE-MOBILE TREATMENT CHECK', 'func': None, 'data_func': None},
    'petransit': {'title': 'PE-TRANSIT TREATMENT CHECK', 'func': None, 'data_func': None},
}

def render_page(page_key):
    """Render the current page"""
    page_config = PAGES.get(page_key)
    
    if not page_config:
        return
    
    # Display title if exists
    if page_config['title']:
        center_title(page_config['title'])
    
    # Display page content
    if page_config['data_func']:
        display_data_cleaning_page(page_config['data_func'])
    elif page_config['func']:
        page_config['func']()

# ==================== Main App Logic ====================
def main():
    """Main application logic"""
    init_session_state()
    reset_page_state()
    
    # Render sidebar and get navigation
    pages = render_sidebar_menu()
    
    # Update current page from navigation
    for page_key in pages:
        st.session_state.current_page = page_key
        st.rerun()
    
    # Render current page
    render_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
