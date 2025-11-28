"""
High Level Design Page
Displays high-level architecture slides from PowerPoint presentation
"""

import streamlit as st
import os
from PIL import Image

def show_high_level_architecture():
    """Display high-level architecture slides"""
    
    st.title("📐 High Level Architecture")
    
    st.markdown("""
    This section presents the high-level design of the Enterprise Agent Platform, 
    showing the overall architecture, components, and data flows at a conceptual level.
    """)
    
    # Slide directory - use relative path
    slide_dir = os.path.join(os.path.dirname(__file__), "hld_slides")
    
    # Check if slides exist
    if not os.path.exists(slide_dir):
        st.error("High-level design slides not found. Please ensure the slides have been converted.")
        return
    
    # Get list of slide images
    slide_files = sorted([f for f in os.listdir(slide_dir) if f.endswith('.png')])
    
    if not slide_files:
        st.error("No slide images found. Please convert the PowerPoint presentation first.")
        return
    
    # Slide titles (customize based on actual content)
    slide_titles = {
        "slide_1.png": "Enterprise Agent Platform - Overview",
        "slide_2.png": "System Architecture",
        "slide_3.png": "Component Interactions",
        "slide_4.png": "Data Flow Diagram"
    }
    
    # Navigation
    st.markdown("---")
    
    # Slide selector
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        slide_index = st.select_slider(
            "Select Slide",
            options=list(range(len(slide_files))),
            format_func=lambda x: f"Slide {x+1} of {len(slide_files)}",
            key="hld_slide_selector"
        )
    
    # Display current slide
    current_slide = slide_files[slide_index]
    slide_path = os.path.join(slide_dir, current_slide)
    
    # Slide title
    slide_title = slide_titles.get(current_slide, f"Slide {slide_index + 1}")
    st.markdown(f"### {slide_title}")
    
    # Display image
    try:
        image = Image.open(slide_path)
        st.image(image)
    except Exception as e:
        st.error(f"Error loading slide: {e}")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⏮️ First"):
            st.session_state.hld_slide_selector = 0
            st.rerun()
    
    with col2:
        if st.button("◀️ Previous", disabled=(slide_index == 0)):
            st.session_state.hld_slide_selector = max(0, slide_index - 1)
            st.rerun()
    
    with col3:
        st.metric("Current", f"{slide_index + 1} / {len(slide_files)}")
    
    with col4:
        if st.button("Next ▶️", disabled=(slide_index == len(slide_files) - 1)):
            st.session_state.hld_slide_selector = min(len(slide_files) - 1, slide_index + 1)
            st.rerun()
    
    with col5:
        if st.button("Last ⏭️"):
            st.session_state.hld_slide_selector = len(slide_files) - 1
            st.rerun()
    
    # Slide overview
    st.markdown("---")
    st.markdown("### 📑 All Slides")
    
    # Display all slides as thumbnails
    cols = st.columns(4)
    for i, slide_file in enumerate(slide_files):
        with cols[i % 4]:
            slide_path = os.path.join(slide_dir, slide_file)
            try:
                image = Image.open(slide_path)
                # Create thumbnail
                image.thumbnail((300, 300))
                
                slide_title = slide_titles.get(slide_file, f"Slide {i + 1}")
                st.markdown(f"**{slide_title}**")
                
                if st.button(f"View", key=f"view_slide_{i}"):
                    st.session_state.hld_slide_selector = i
                    st.rerun()
                
                st.image(image)
            except Exception as e:
                st.error(f"Error loading thumbnail: {e}")
    
    # Download section
    st.markdown("---")
    st.markdown("### 💾 Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Download Original PowerPoint:**
        
        Get the original High Level Design presentation in PowerPoint format.
        """)
        
        # Provide download button for original PPTX
        pptx_path = os.path.join(os.path.dirname(__file__), "hld_slides", "High_Level_Design_v5.pptx")
        if os.path.exists(pptx_path):
            with open(pptx_path, "rb") as f:
                st.download_button(
                    label="📥 Download PPTX",
                    data=f,
                    file_name="High_Level_Design_v5.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
    
    with col2:
        st.markdown("""
        **Download as PDF:**
        
        Get the presentation in PDF format for easy sharing and viewing.
        """)
        
        # Provide download button for PDF
        pdf_path = os.path.join(os.path.dirname(__file__), "hld_slides", "High_Level_Design_v5.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF",
                    data=f,
                    file_name="High_Level_Design_v5.pdf",
                    mime="application/pdf"
                )
    
    # Information
    st.markdown("---")
    with st.expander("ℹ️ About High Level Design"):
        st.markdown("""
        ### High Level Design (HLD)
        
        The High Level Design provides a conceptual view of the Enterprise Agent Platform architecture:
        
        **Purpose:**
        - Communicate overall system structure to stakeholders
        - Show major components and their relationships
        - Illustrate data flows at a high level
        - Provide context for detailed design decisions
        
        **Audience:**
        - Executive leadership
        - Product managers
        - Business analysts
        - Technical architects
        - External partners
        
        **Complement with:**
        - **Full Architecture** - Detailed component diagram
        - **Request Flow Simulator** - Runtime behavior
        - **Component Explorer** - Individual component details
        - **Use Cases** - Real-world scenarios
        
        **Navigation Tips:**
        - Use the slider to move between slides
        - Click thumbnail images to jump to specific slides
        - Use arrow buttons for sequential navigation
        - Download PPTX or PDF for offline viewing
        """)

if __name__ == "__main__":
    show_high_level_architecture()
