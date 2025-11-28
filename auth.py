"""
Authentication Module
Handles user authentication for the architecture visualizer
"""

import streamlit as st
import hashlib

# Hardcoded credentials
VALID_USERNAME = "CCArchitecture"
VALID_PASSWORD = "DreamBig88$"

def hash_password(password):
    """Hash password for comparison"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    """Check if user is authenticated"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    
    # If already authenticated, return True
    if st.session_state.authenticated:
        return True
    
    # Show login form
    show_login_form()
    
    return False

def show_login_form():
    """Display login form"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>🏗️ Enterprise Agent Platform</h1>
            <h2>Architecture Visualizer</h2>
            <p style='color: #666; margin-top: 1rem;'>Please login to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if submit:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.login_attempts = 0
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    st.error(f"❌ Invalid credentials. Attempt {st.session_state.login_attempts}")
                    
                    if st.session_state.login_attempts >= 3:
                        st.warning("⚠️ Multiple failed attempts detected. Please contact administrator.")
        
        # Information
        with st.expander("ℹ️ About"):
            st.markdown("""
            ### Enterprise Agent Platform Visualizer
            
            This application provides comprehensive visualization of the Enterprise Agent Platform architecture:
            
            - **32 components** across 8 layers
            - **Interactive diagrams** with flow visualization
            - **Request flow simulation** with sample queries
            - **High-level architecture** slides
            - **Use case demonstrations**
            - **OpenAPI prompts** documentation
            
            **For access**, please contact your system administrator.
            """)
        
        # Footer
        st.markdown("""
        <div style='text-align: center; margin-top: 3rem; color: #999; font-size: 0.85rem;'>
            <p>© 2024 Enterprise Agent Platform | Version 2.0</p>
            <p>Secure Architecture Visualization System</p>
        </div>
        """, unsafe_allow_html=True)

def authenticate(username, password):
    """Authenticate user credentials"""
    return username == VALID_USERNAME and password == VALID_PASSWORD

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.login_attempts = 0
    st.rerun()

def show_logout_button():
    """Display logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**👤 User**: {VALID_USERNAME}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
