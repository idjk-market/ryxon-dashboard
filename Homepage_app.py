# ---- DASHBOARD PAGE ----
def dashboard_page():
    # Persistent sidebar implementation
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = True
    
    # Sidebar toggle button in main content
    if st.button("☰" if st.session_state.sidebar_expanded else "☰", key="sidebar_toggle"):
        st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
        st.rerun()
    
    # Navigation sidebar
    if st.session_state.sidebar_expanded:
        with st.sidebar:
            st.image("https://via.placeholder.com/150x50?text=Ryxon", width=150)
            st.markdown("## Navigation")
            
            if st.button("📊 Dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            if st.button("📂 Upload Trades"):
                st.session_state.current_page = "upload"
                st.rerun()
            
            if st.button("✍️ Manual Entry"):
                st.session_state.current_page = "manual"
                st.rerun()
            
            if st.button("📈 Analytics"):
                st.session_state.current_page = "analytics"
                st.rerun()
            
            if st.button("⚙️ Settings"):
                st.session_state.current_page = "settings"
                st.rerun()
            
            st.markdown("---")
            if st.button("🔒 Logout"):
                st.session_state.auth = False
                st.session_state.current_page = "login"
                st.rerun()
            
            # Dark mode toggle
            st.markdown("---")
            dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
            if dark_mode != st.session_state.dark_mode:
                st.session_state.dark_mode = dark_mode
                set_app_style()
                st.rerun()

    # Main content with back button
    with st.container():
        st.title("📊 Trading Dashboard")
        
        # Back button (hidden on dashboard since we're already here)
        if st.session_state.current_page != "dashboard":
            if st.button("← Back to Dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        # Rest of your existing dashboard content...
        # Stats cards, recent trades table, etc.

# ---- FILE UPLOAD ----
def upload_page():
    # Persistent sidebar toggle
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = True
    
    if st.button("☰" if st.session_state.sidebar_expanded else "☰", key="sidebar_toggle"):
        st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
        st.rerun()
    
    if st.session_state.sidebar_expanded:
        with st.sidebar:
            # Same sidebar content as dashboard_page
            pass
    
    with st.container():
        st.title("📂 Trade File Upload")
        
        # Back button
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        # Rest of your existing upload page content...

# ---- MANUAL ENTRY ----
def manual_page():
    # Persistent sidebar toggle
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = True
    
    if st.button("☰" if st.session_state.sidebar_expanded else "☰", key="sidebar_toggle"):
        st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
        st.rerun()
    
    if st.session_state.sidebar_expanded:
        with st.sidebar:
            # Same sidebar content as dashboard_page
            pass
    
    with st.container():
        st.title("✍️ Manual Trade Entry")
        
        # Back button
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        # Rest of your existing manual entry content...

# Similarly update analytics_page(), settings_page(), and processing_page() with:
# 1. The persistent sidebar toggle logic
# 2. Back button at the top of main content
# 3. Consistent sidebar content

# ---- MAIN APP ----
def main():
    set_app_style()
    
    if not st.session_state.auth:
        login_page()
    else:
        # Initialize sidebar state if not exists
        if 'sidebar_expanded' not in st.session_state:
            st.session_state.sidebar_expanded = True
            
        if st.session_state.current_page == "dashboard":
            dashboard_page()
        elif st.session_state.current_page == "upload":
            upload_page()
        elif st.session_state.current_page == "manual":
            manual_page()
        elif st.session_state.current_page == "analytics":
            analytics_page()
        elif st.session_state.current_page == "settings":
            settings_page()
        elif st.session_state.current_page == "processing":
            processing_page()

if __name__ == "__main__":
    main()
