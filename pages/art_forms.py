import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from utils.data_loader import load_art_forms_data, load_india_geojson
from utils.visualization import create_india_map, create_choropleth_map, create_bar_chart, create_scatter_map

def show_art_forms_page(map_focus=False):
    """
    Display the Traditional Art Forms page.
    
    Parameters:
        map_focus (bool): If True, emphasizes the map visualization (for Cultural Map Explorer).
                         If False, emphasizes the database aspect (for Art Forms Database).
    """
    st.title("🎨 Traditional Art Forms of India")
    
    st.write("""
    India's cultural landscape is adorned with a rich tapestry of traditional art forms that have evolved over centuries.
    These art forms reflect the diversity, heritage, and spiritual essence of different regions across the country.
    
    """)
    
    # Load data
    art_forms_data = load_art_forms_data()
    india_geojson = load_india_geojson()
    
    if art_forms_data is None:
        st.error("Unable to load art forms data. Please try again later.")
        return
    
    # Dynamically adjust title based on mode
    if map_focus:
        st.title("🗺️ Cultural Map Explorer")
        st.write("""
        Explore the geographical distribution of India's rich cultural heritage through this interactive map.
        Discover traditional art forms, historical sites, and cultural hotspots across different regions of India.
        Use the filters below to customize your exploration.
        """)
    else:
        st.title("🎨 Art Forms Database")
        st.write("""
        Browse our comprehensive database of India's traditional art forms. This searchable catalog
        provides detailed information, images, and descriptions of various art forms across India.
        Use the search and filter options to discover specific art forms of interest.
        """)
    
    # Create tabs for different visualizations - show different tabs based on mode
    if map_focus:
        # Only show map-related tabs for map focus mode
        tabs = st.tabs(["Interactive Map", "Regional Distribution"])
        tab1, tab4 = tabs
        # Initialize empty placeholders for the other tabs to avoid reference errors
        tab2 = None
        tab3 = None
        
        # Set variables that might be referenced in database mode to avoid errors
        search_query = ""
        sort_by = "Name (A-Z)"
    else:
        # Add search functionality for the database view
        st.write("### Search Art Forms")
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_query = st.text_input("Search by name, type, or region", "")
        
        with search_col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Name (A-Z)", "Popularity", "Cultural Significance"],
                index=0
            )
        
        # Create tabs for the database view
        tabs = st.tabs(["Art Forms Catalog", "Art Forms by Type", "Cultural Significance", "Regional Distribution"])
        tab1, tab2, tab3, tab4 = tabs
    
    with tab1:
        # Different content based on mode
        if map_focus:
            st.subheader("Interactive Map of Indian Cultural Heritage")
            
            # Filters for the map
            col1, col2 = st.columns(2)
            with col1:
                selected_types = st.multiselect(
                    "Filter by Art Type",
                    options=sorted(art_forms_data['type'].unique()),
                    default=[]
                )
            
            with col2:
                selected_states = st.multiselect(
                    "Filter by State",
                    options=sorted(art_forms_data['state'].unique()),
                    default=[]
                )
            
            # Apply filters
            filtered_data = art_forms_data
            if selected_types:
                filtered_data = filtered_data[filtered_data['type'].isin(selected_types)]
            if selected_states:
                filtered_data = filtered_data[filtered_data['state'].isin(selected_states)]
            
            # Create and display map with larger size for map focus mode
            if not filtered_data.empty:
                st.write(f"Displaying {len(filtered_data)} cultural locations")
                india_map = create_india_map(filtered_data)
                st_folium(india_map, width=1000, height=600)
                
                # Add descriptions of selected points below the map
                st.write("### Featured Cultural Sites")
                for _, row in filtered_data.head(5).iterrows():
                    st.markdown(f"""
                    <div style="padding: 10px; margin-bottom: 10px; background-color: #f5f5f5; border-radius: 5px;">
                        <h4 style="color: #FF9800;">{row['art_form']}</h4>
                        <p><strong>Location:</strong> {row['state']}</p>
                        <p><strong>Type:</strong> {row['type']}</p>
                        <p>{row['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No cultural sites match the selected filters. Please adjust your selection.")
        else:
            # Database catalog view
            st.subheader("Indian Art Forms Catalog")
            
            # Apply search filter
            filtered_data = art_forms_data
            if search_query:
                # Case insensitive search across multiple columns
                filtered_data = filtered_data[
                    filtered_data['art_form'].str.lower().str.contains(search_query.lower()) | 
                    filtered_data['type'].str.lower().str.contains(search_query.lower()) | 
                    filtered_data['state'].str.lower().str.contains(search_query.lower()) |
                    filtered_data['description'].str.lower().str.contains(search_query.lower())
                ]
            
            # Apply sorting
            if sort_by == "Name (A-Z)":
                filtered_data = filtered_data.sort_values('art_form')
            elif sort_by == "Popularity":
                filtered_data = filtered_data.sort_values('visitors_annual', ascending=False)
            elif sort_by == "Cultural Significance":
                # Create a mapping for significance levels
                significance_map = {"Low": 1, "Medium": 2, "High": 3}
                filtered_data['significance_score'] = filtered_data['cultural_significance'].map(significance_map)
                filtered_data = filtered_data.sort_values(['significance_score', 'art_form'], ascending=[False, True])
                filtered_data = filtered_data.drop('significance_score', axis=1)
            
            # Display results
            st.write(f"Found {len(filtered_data)} art forms")
            
            # Display art forms in a grid with card-like appearance
            cols = st.columns(2)
            for i, (_, row) in enumerate(filtered_data.iterrows()):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="padding: 15px; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 10px; border-left: 5px solid #FF9800;">
                        <h3 style="color: #FF9800; margin-top: 0;">{row['art_form']}</h3>
                        <p><strong>Origin:</strong> {row['state']}</p>
                        <p><strong>Type:</strong> {row['type']}</p>
                        <p><strong>Cultural Significance:</strong> {row['cultural_significance']}</p>
                        <p><strong>Annual Visitors:</strong> {row['visitors_annual']:,}</p>
                        <p>{row['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # No results message
            if filtered_data.empty:
                st.info("No art forms match your search criteria. Try different keywords or clear the search.")
                
            # Advanced search options
            with st.expander("Advanced Search Options"):
                adv_col1, adv_col2 = st.columns(2)
                
                with adv_col1:
                    significance_filter = st.multiselect(
                        "Filter by Cultural Significance",
                        options=["Low", "Medium", "High"],
                        default=[]
                    )
                
                with adv_col2:
                    min_visitors = st.slider(
                        "Minimum Annual Visitors",
                        min_value=0,
                        max_value=int(art_forms_data['visitors_annual'].max()),
                        value=0,
                        step=1000
                    )
    
    # Only show these tabs in database mode (not map mode)
    if not map_focus and tab2 is not None:
        with tab2:
            st.subheader("Traditional Art Forms by Type")
            
            # Count art forms by type
            type_counts = art_forms_data['type'].value_counts().reset_index()
            type_counts.columns = ['Art Type', 'Count']
            
            # Create bar chart
            fig = create_bar_chart(
                type_counts,
                'Art Type',
                'Count',
                title="Distribution of Traditional Art Forms by Type"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show descriptions by type
            selected_type = st.selectbox(
                "Select an art form type to learn more",
                options=sorted(art_forms_data['type'].unique())
            )
            
            st.write(f"### About {selected_type}")
            
            type_data = art_forms_data[art_forms_data['type'] == selected_type]
            for _, row in type_data.iterrows():
                st.write(f"**{row['art_form']} ({row['state']})**")
                st.write(row['description'])
                st.write("---")
    
    if not map_focus and tab3 is not None:
        with tab3:
            st.subheader("Cultural Significance and Popularity")
            
            # Create a scatter plot of visitors vs cultural significance
            fig = px.scatter(
                art_forms_data,
                x="visitors_annual",
                y="cultural_significance",
                color="type",
                size="visitors_annual",
                hover_name="art_form",
                hover_data=["state", "description"],
                labels={
                    "visitors_annual": "Annual Visitors",
                    "cultural_significance": "Cultural Significance",
                    "type": "Art Form Type"
                },
                title="Relationship Between Visitor Numbers and Cultural Significance"
            )
            
            # Update the y-axis to display categories correctly
            fig.update_layout(
                yaxis=dict(
                    categoryorder="array",
                    categoryarray=["Low", "Medium", "High"]
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("""
            This visualization shows the relationship between a traditional art form's annual visitors (popularity)
            and its cultural significance. Art forms in the upper right are both highly significant culturally
            and popular with visitors.
            """)
            
            # Top 5 most visited art forms
            st.write("### Top 5 Most Visited Art Forms")
            top_visited = art_forms_data.sort_values('visitors_annual', ascending=False).head(5)
            for i, (_, row) in enumerate(top_visited.iterrows(), 1):
                st.write(f"**{i}. {row['art_form']} ({row['state']})**")
                st.write(f"Annual Visitors: {row['visitors_annual']:,}")
                st.write(f"Cultural Significance: {row['cultural_significance']}")
                st.write(row['description'])
                st.write("---")
    
    with tab4:
        st.subheader("Regional Distribution of Art Forms")
        
        # Create a choropleth map of art forms by state
        if india_geojson:
            # Aggregate data by state
            state_counts = art_forms_data.groupby('state').size().reset_index(name='count')
            
            # Create and display the map
            choropleth_map = create_choropleth_map(
                state_counts,
                india_geojson,
                'count',
                'Number of Traditional Art Forms'
            )
            
            st_folium(choropleth_map, width=1000, height=500)
        else:
            st.warning("Unable to load geographical data for India. Displaying alternative visualization.")
            
            # Create a bar chart as an alternative
            state_counts = art_forms_data.groupby('state').size().reset_index(name='count')
            state_counts = state_counts.sort_values('count', ascending=False)
            
            fig = create_bar_chart(
                state_counts,
                'state',
                'count',
                title="Number of Traditional Art Forms by State"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display scatter map of art forms
        st.write("### Geographic Distribution of Art Forms")
        scatter_map = create_scatter_map(
            art_forms_data,
            'latitude',
            'longitude',
            'art_form',
            size_column='visitors_annual',
            color_column='type',
            title="Location of Traditional Art Forms"
        )
        st.plotly_chart(scatter_map, use_container_width=True)
    
    # Download options
    st.subheader("Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = art_forms_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Art Forms Data as CSV",
            data=csv,
            file_name="india_traditional_art_forms.csv",
            mime="text/csv"
        )
    
    with col2:
        st.write("""
        This data includes geographical locations, descriptions, visitor numbers,
        and cultural significance ratings for various traditional art forms across India.
        """)
