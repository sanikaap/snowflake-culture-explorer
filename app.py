import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_art_forms_data, load_tourism_data
from utils.visualization import create_india_map, create_trend_chart

# Set page configuration
st.set_page_config(
    page_title="Indian Cultural Heritage Explorer",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom CSS for improved UI
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #FF9800;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 152, 0, 0.1);
        border-bottom: 2px solid #FF9800;
    }
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        text-align: center;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Define session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #FF9800;">Navigation</h1>
    <p style="font-size: 0.9rem; margin-top: -10px;">Explore India's Cultural Heritage</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS for the sidebar navigation
st.sidebar.markdown("""
<style>
div.row-widget.stRadio > div {
    display: flex;
    flex-direction: column;
}
div.row-widget.stRadio > div[role="radiogroup"] > label {
    padding: 10px 15px;
    margin: 4px 0;
    border-radius: 5px;
    background-color: #f9f9f9;
    transition: all 0.3s;
}
div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
    background-color: rgba(255, 152, 0, 0.1);
}
div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
    height: 20px;
    width: 20px;
}
div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    background-color: #FF9800;
}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Go to",
    ["Home", "Cultural Map Explorer", "Art Forms Database", "Tourism Analytics", "Recommendation System", "Responsible Tourism"],
    key="nav"
)

# Add some information about the app in the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About This App

This interactive application showcases India's rich cultural heritage, traditional art forms, and tourism opportunities. Explore the data visualizations to discover the diversity of India's cultural landscape.

**Data Sources:**
- Traditional art forms data
- Cultural tourism statistics
- Geographical information

""")

# Add a footer to the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem;">
    <p>© 2025 thesilicon muse</p>
</div>
""", unsafe_allow_html=True)

# Update current page in session state
st.session_state.current_page = page.lower().replace(" ", "_")

# Home page
if st.session_state.current_page == 'home':
    st.title("India's Cultural Heritage Explorer")
    
    st.write("""
    ## Welcome to India's Cultural Heritage Explorer
    
    Discover the rich tapestry of India's traditional art forms and cultural experiences through
    this interactive data-driven application. Explore the diverse cultural heritage, understand tourism
    trends, find hidden gems, and learn about responsible tourism opportunities.
    
    ### What you can explore:
    - **Cultural Map Explorer**: Interactive map of India showing cultural sites and tourism hotspots
    - **Art Forms Database**: Searchable catalog of traditional Indian art forms with images and descriptions
    - **Tourism Analytics**: Data-driven charts and graphs showing visitor patterns and trends to cultural sites
    - **Recommendation System**: Discover cultural sites to visit based on your preferences
    - **Responsible Tourism**: Guidelines and opportunities for culturally sensitive and sustainable tourism
    
    """)
    
    # Brief overview with key facts
    st.markdown("""
    <div style="margin: 20px 0;">
        <h3 style="margin-bottom: 15px;">Key Facts About India's Cultural Heritage</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h4 style="color: #FF9800; margin-bottom: 8px;">Recognized Art Forms</h4>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">100+</p>
            <p style="color: #666; margin-top: 5px;">Cultural Diversity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h4 style="color: #FF9800; margin-bottom: 8px;">UNESCO Heritage Sites</h4>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">40</p>
            <p style="color: #666; margin-top: 5px;">7 Natural, 33 Cultural</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h4 style="color: #FF9800; margin-bottom: 8px;">Languages & Dialects</h4>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">1600+</p>
            <p style="color: #666; margin-top: 5px;">22 Official Languages</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display a preview map
    st.subheader("Preview: Traditional Art Forms Across India")
    art_forms_data = load_art_forms_data()
    
    if art_forms_data is not None:
        india_map = create_india_map(art_forms_data)
        st_folium(india_map, width=1200, height=600)
    else:
        st.error("Unable to load art forms data. Please check your connection or try again later.")
    
    # How to use the app
    st.markdown("""
    <div style="margin: 30px 0 15px 0;">
        <h3 style="color: #FF9800;">How to Use This App</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("""
        <div class="metric-container" style="height: 170px;">
            <h4 style="color: #FF9800; margin-bottom: 8px;">🧭 Navigate</h4>
            <p>Use the sidebar to navigate between different sections of the app</p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">Each section focuses on a different aspect of India's cultural heritage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="metric-container" style="height: 170px;">
            <h4 style="color: #FF9800; margin-bottom: 8px;">🗺️ Explore Maps</h4>
            <p>Interact with the maps by hovering, zooming, and clicking</p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">Discover geographical distributions of art forms and cultural sites</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class="metric-container" style="height: 170px;">
            <h4 style="color: #FF9800; margin-bottom: 8px;">📊 Analyze Data</h4>
            <p>Use filters and controls to customize visualizations</p>
            <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">Download insights as CSV files for offline analysis</p>
        </div>
        """, unsafe_allow_html=True)

# Import and display other pages based on navigation
elif st.session_state.current_page == 'cultural_map_explorer':
    from pages.art_forms import show_art_forms_page
    # Use the existing art_forms page but modify for map focus
    show_art_forms_page(map_focus=True)

elif st.session_state.current_page == 'art_forms_database':
    from pages.art_forms import show_art_forms_page
    # Use the existing art_forms page with database focus
    show_art_forms_page(map_focus=False)

elif st.session_state.current_page == 'tourism_analytics':
    from pages.tourism_trends import show_tourism_trends_page
    show_tourism_trends_page()

elif st.session_state.current_page == 'recommendation_system':
    from pages.hidden_gems import show_hidden_gems_page
    # Repurpose hidden_gems as a recommendation system
    show_hidden_gems_page(recommendation_mode=True)

elif st.session_state.current_page == 'responsible_tourism':
    from pages.responsible_tourism import show_responsible_tourism_page
    show_responsible_tourism_page()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Data sourced from data.gov.in | Created with Streamlit | By thesiliconmuse</p>
</div>
""", unsafe_allow_html=True)
