import streamlit as st
from logic import display_data_cleaning_page, ultramon_genie_clean, genie_clean, genie_p95, genie_ref_clean, ultramon, zabbix_clean
from session import init_session_state, reset_page_state
from ui import display_home_page, display_auth_page, setup_sidebar, display_user_info, display_logout_button, logout_confirmation, center_title

# ==================== Configuration ====================
st.set_page_config(
    page_title="CNOP Data Wrangler",
    layout="wide",
    page_icon="img/logo_ultramon.jpg"
)

# Initialize session state
init_session_state()

# ==================== Page Configuration ====================
PAGES = {
    'home': {'title': '', 'func': display_home_page, 'data_func': None},
    'ultramon': {'title': 'ULTRAMON DATA', 'func': display_data_cleaning_page, 'data_func': ultramon},
    'ultramon_genie': {'title': 'ULTRAMON x GENIE P95 DATA', 'func': display_data_cleaning_page, 'data_func': ultramon_genie_clean},
    'ultramon_ref': {'title': 'ULTRAMON REFERENCE', 'func': None, 'data_func': None},
    'genie_clean': {'title': 'GENIE DATA', 'func': display_data_cleaning_page, 'data_func': genie_clean},
    'genie_p95': {'title': 'GENIE P95 DATA', 'func': display_data_cleaning_page, 'data_func': genie_p95},
    'genie_ref': {'title': 'GENIE REFERENCE', 'func': display_data_cleaning_page, 'data_func': genie_ref_clean},
    'zabbix_clean': {'title': 'ZABBIX DATA', 'func': display_data_cleaning_page, 'data_func': zabbix_clean},
    'zabbix_ref': {'title': 'ZABBIX REFERENCE', 'func': None, 'data_func': None},
}

# ==================== Navigation Menu ====================
def render_sidebar_menu():
    """Render sidebar navigation menu"""
    pages = {}
    
    if st.sidebar.button("Home", use_container_width=True, key="home_btn"):
        pages['home'] = True
    
    with st.sidebar.expander("**ULTRAMON**", expanded=False):
        if st.button("Backbone", use_container_width=True, key="ultramon_btn"):
            pages['ultramon'] = True
        if st.button("Ultramon ATOM & NON-ATOM P95 Data", use_container_width=True, key="ultramon_gen_btn"):
            pages['ultramon_genie'] = True
        if st.button("Reference", use_container_width=True, key="ultramon_ref_btn"):
            pages['ultramon_ref'] = True
    
    with st.sidebar.expander("**GENIE**", expanded=False):
        if st.button("Genie ATOM & NON-ATOM", use_container_width=True, key="genie_atom_btn"):
            pages['genie_clean'] = True
        if st.button("Genie P95 Data", use_container_width=True, key="genie_p95_btn"):
            pages['genie_p95'] = True
        if st.button("Reference", use_container_width=True, key="genie_ref_btn"):
            pages['genie_ref'] = True
    
    with st.sidebar.expander("**ZABBIX**", expanded=False):
        if st.button("ATOM", use_container_width=True, key="zabbix_btn"):
            pages['zabbix_clean'] = True
        if st.button("Reference", use_container_width=True, key="zabbix_ref_btn"):
            pages['zabbix_ref'] = True
    
    return pages


def render_page(page_key):
    """Render the selected page"""
    page_config = PAGES.get(page_key)
    
    if not page_config:
        return
    
    if page_config['title']:
        center_title(page_config['title'])
    
    if page_config['data_func']:
        display_data_cleaning_page(page_config['data_func'])
    elif page_config['func']:
        page_config['func']()


# ==================== Main Application ====================
def main():
    """Main application logic"""
    # Show auth page if not authenticated
    if not st.session_state.authenticated:
        display_auth_page()
        return
    
    # User is authenticated - show dashboard
    reset_page_state()
    
    # Setup sidebar
    setup_sidebar()
    display_user_info()
    st.sidebar.markdown("---")
    
    # Render navigation menu
    pages = render_sidebar_menu()
    
    # Handle navigation
    for page_key in pages:
        st.session_state.current_page = page_key
        st.rerun()
    
    # Render current page
    render_page(st.session_state.current_page)
    
    # Logout section
    display_logout_button()
    logout_confirmation()


if __name__ == "__main__":
    main()
