import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_hidden_gems_data
from utils.visualization import create_bar_chart, create_scatter_map

def show_hidden_gems_page(recommendation_mode=False):
    """
    Display the Hidden Cultural Gems page or Recommendation System.
    
    Parameters:
        recommendation_mode (bool): If True, displays the page as a recommendation system.
                                  If False, displays the original hidden gems page.
    """
    if recommendation_mode:
        st.title("🧭 Cultural Site Recommendation System")
        
        st.write("""
        Discover cultural sites in India that match your interests and preferences. 
        This recommendation system will suggest cultural destinations based on your preferences
        for art forms, cultural experiences, and travel interests.
        """)
    else:
        st.title("💎 Hidden Cultural Gems of India")
        
        st.write("""
        Beyond the well-trodden tourist paths lie India's hidden cultural treasures — places of immense
        cultural significance yet to be discovered by mass tourism. This section showcases these lesser-known
        destinations, their unique art forms, and the authentic cultural experiences they offer.
        
        
        """)
    
    # Load data
    hidden_gems_data = load_hidden_gems_data()
    
    if hidden_gems_data is None:
        st.error("Unable to load hidden gems data. Please try again later.")
        return
    
    # Modify interface based on mode
    if recommendation_mode:
        # Recommendation system interface
        st.write("### What kind of cultural experience are you looking for?")
        
        # Preference form
        with st.form("recommendation_preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                preferred_art_forms = st.multiselect(
                    "Art Forms of Interest",
                    options=sorted(hidden_gems_data['art_form'].unique()),
                    default=[]
                )
                
                accessibility_pref = st.select_slider(
                    "Accessibility Preference",
                    options=["Easy", "Moderate", "Challenging"],
                    value="Moderate"
                )
                
                preferred_region = st.multiselect(
                    "Preferred Regions",
                    options=["North India", "South India", "East India", "West India", "Northeast India", "Central India"],
                    default=[]
                )
            
            with col2:
                crowd_preference = st.slider(
                    "Crowd Level (1: Secluded, 10: Popular)",
                    min_value=1,
                    max_value=10,
                    value=5
                )
                
                visit_duration = st.number_input(
                    "How many days can you spend?",
                    min_value=1,
                    max_value=30,
                    value=7
                )
                
                season = st.selectbox(
                    "When do you plan to visit?",
                    options=["Summer (Mar-Jun)", "Monsoon (Jul-Sep)", "Winter (Oct-Feb)"],
                )
            
            interest_level = {
                "History": st.slider("Interest in Historical Sites (1-10)", 1, 10, 5),
                "Religion": st.slider("Interest in Religious Sites (1-10)", 1, 10, 5),
                "Art": st.slider("Interest in Art & Crafts (1-10)", 1, 10, 5),
                "Nature": st.slider("Interest in Natural Beauty (1-10)", 1, 10, 5),
                "Food": st.slider("Interest in Culinary Experiences (1-10)", 1, 10, 5)
            }
            
            submitted = st.form_submit_button("Get Personalized Recommendations")
        
        # Process recommendations when form is submitted
        if submitted:
            # Set session state to track that recommendations have been submitted
            st.session_state.recommendations_submitted = True
            st.write("### Your Personalized Recommendations")
            
            # Very simple recommendation algorithm (in a real app, this would be more sophisticated)
            # Score each destination based on how well it matches preferences
            scores = {}
            
            for idx, row in hidden_gems_data.iterrows():
                score = 0
                
                # Match art form preferences
                if preferred_art_forms and row['art_form'] in preferred_art_forms:
                    score += 3
                
                # Match accessibility preferences
                if row['accessibility'] == accessibility_pref:
                    score += 2
                
                # Match crowd preferences (inverse relationship with visitor numbers)
                normalized_visitors = row['visitors_annual'] / hidden_gems_data['visitors_annual'].max() * 10
                crowd_score = 10 - abs(crowd_preference - normalized_visitors)
                score += crowd_score / 2
                
                # Add other scoring factors based on interests
                # (In a real app, we'd have more detailed data about each attribute)
                
                scores[row['name']] = score
            
            # Sort destinations by score
            recommended_destinations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Display recommendations
            for i, (name, score) in enumerate(recommended_destinations, 1):
                dest_data = hidden_gems_data[hidden_gems_data['name'] == name].iloc[0]
                
                st.markdown(f"""
                <div style="padding: 15px; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 10px; border-left: 5px solid #FF9800;">
                    <h3 style="color: #FF9800; margin-top: 0;">#{i}: {name}</h3>
                    <p><strong>State:</strong> {dest_data['state']}</p>
                    <p><strong>Art Form:</strong> {dest_data['art_form']}</p>
                    <p><strong>Accessibility:</strong> {dest_data['accessibility']}</p>
                    <p><strong>Best Time to Visit:</strong> {dest_data['best_time_to_visit']}</p>
                    <p>{dest_data['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display map of recommendations
            st.write("### Map of Recommended Destinations")
            recommended_names = [name for name, _ in recommended_destinations]
            recommended_data = hidden_gems_data[hidden_gems_data['name'].isin(recommended_names)]
            
            m = folium.Map(location=[22.5937, 78.9629], zoom_start=4, tiles="OpenStreetMap")
            
            # Add markers for recommended destinations
            for idx, row in recommended_data.iterrows():
                popup_text = f"""
                <strong>{row['name']}</strong><br>
                <strong>State:</strong> {row['state']}<br>
                <strong>Art Form:</strong> {row['art_form']}<br>
                <strong>Description:</strong> {row['description']}<br>
                """
                
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['name'],
                    icon=folium.Icon(icon="star", prefix="fa", color="orange")
                ).add_to(m)
            
            st_folium(m, width=1000, height=500)
            
            # Travel planning tips
            st.write("### Planning Your Cultural Journey")
            st.write("""
            Here are some tips for planning your visit to these cultural sites:
            
            1. **Research local customs** before visiting these cultural sites
            2. **Learn a few local phrases** to enhance your experience and show respect
            3. **Check for local festivals** that might coincide with your visit
            4. **Support local artisans** by purchasing directly from them
            5. **Consider hiring local guides** who can provide deeper cultural context
            """)
    else:
        # Original hidden gems interface with tabs
        tab1, tab2, tab3 = st.tabs(["Map Explorer", "Destination Finder", "Detailed Profiles"])
    
    # Only show these tabs in the original hidden gems mode (not recommendation mode)
    if not recommendation_mode and 'tab1' in locals():
        with tab1:
            st.subheader("Map of Hidden Cultural Gems")
            
            # Create and display interactive map
            scatter_map = create_scatter_map(
                hidden_gems_data,
                'latitude',
                'longitude',
                'name',
                size_column='visitors_annual',
                color_column='art_form',
                title="Location of Hidden Cultural Gems"
            )
            st.plotly_chart(scatter_map, use_container_width=True)
            
            st.write("""
            The map above shows the geographical distribution of lesser-known cultural destinations across India.
            The size of each point represents the annual number of visitors, while the color indicates the
            primary art form associated with the destination.
            
            Click on points to learn more about each hidden gem.
            """)
            
            # Create a folium map with more detailed popups
            m = folium.Map(location=[22.5937, 78.9629], zoom_start=4, tiles="OpenStreetMap")
            
            # Add markers for each hidden gem
            for idx, row in hidden_gems_data.iterrows():
                popup_text = f"""
                <strong>{row['name']}</strong><br>
                <strong>State:</strong> {row['state']}<br>
                <strong>Art Form:</strong> {row['art_form']}<br>
                <strong>Description:</strong> {row['description']}<br>
                <strong>Annual Visitors:</strong> {row['visitors_annual']:,}<br>
                <strong>Accessibility:</strong> {row['accessibility']}<br>
                <strong>Best Time to Visit:</strong> {row['best_time_to_visit']}
                """
                
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['name'],
                    icon=folium.Icon(icon="gem", prefix="fa", color="purple")
                ).add_to(m)
            
            st_folium(m, width=1000, height=500)
    
    if not recommendation_mode and 'tab2' in locals():
        with tab2:
            st.subheader("Find Hidden Gems by Preference")
            
            # Create filters
            col1, col2 = st.columns(2)
            
            with col1:
                selected_accessibility = st.selectbox(
                    "Accessibility Level",
                    options=["All"] + sorted(hidden_gems_data['accessibility'].unique())
                )
            
            with col2:
                selected_art_form = st.selectbox(
                    "Art Form of Interest",
                    options=["All"] + sorted(hidden_gems_data['art_form'].unique())
                )
            
            # Additional filters
            col3, col4 = st.columns(2)
            
            with col3:
                max_visitors = st.slider(
                    "Maximum Annual Visitors",
                    min_value=0,
                    max_value=int(hidden_gems_data['visitors_annual'].max()),
                    value=int(hidden_gems_data['visitors_annual'].max()),
                    step=1000
                )
            
            with col4:
                selected_region = st.selectbox(
                    "Region of India",
                    options=["All", "North", "South", "East", "West", "Northeast", "Central"]
                )
                
                # Create a mapping of states to regions (simplified for demonstration)
                region_mapping = {
                    "North": ["Jammu and Kashmir", "Himachal Pradesh", "Punjab", "Uttarakhand", "Haryana", "Delhi", "Uttar Pradesh"],
                    "South": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana"],
                    "East": ["West Bengal", "Odisha", "Bihar", "Jharkhand"],
                    "West": ["Rajasthan", "Gujarat", "Maharashtra", "Goa"],
                    "Northeast": ["Assam", "Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura"],
                    "Central": ["Madhya Pradesh", "Chhattisgarh"]
                }
            
            # Apply filters
            filtered_data = hidden_gems_data
            
            if selected_accessibility != "All":
                filtered_data = filtered_data[filtered_data['accessibility'] == selected_accessibility]
            
            if selected_art_form != "All":
                filtered_data = filtered_data[filtered_data['art_form'] == selected_art_form]
            
            filtered_data = filtered_data[filtered_data['visitors_annual'] <= max_visitors]
            
            if selected_region != "All":
                filtered_data = filtered_data[filtered_data['state'].isin(region_mapping.get(selected_region, []))]
            
            # Display results
            if filtered_data.empty:
                st.warning("No destinations match your criteria. Try adjusting the filters.")
            else:
                st.write(f"Found {len(filtered_data)} destinations matching your criteria:")
                
                # Create columns for card-like display
                for i in range(0, len(filtered_data), 2):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if i < len(filtered_data):
                            row = filtered_data.iloc[i]
                            st.subheader(row['name'])
                            st.write(f"**State:** {row['state']}")
                            st.write(f"**Art Form:** {row['art_form']}")
                            st.write(f"**Accessibility:** {row['accessibility']}")
                            st.write(f"**Best Time to Visit:** {row['best_time_to_visit']}")
                            st.write(f"**Annual Visitors:** {row['visitors_annual']:,}")
                            st.write(row['description'])
                    
                    with col2:
                        if i + 1 < len(filtered_data):
                            row = filtered_data.iloc[i + 1]
                            st.subheader(row['name'])
                            st.write(f"**State:** {row['state']}")
                            st.write(f"**Art Form:** {row['art_form']}")
                            st.write(f"**Accessibility:** {row['accessibility']}")
                            st.write(f"**Best Time to Visit:** {row['best_time_to_visit']}")
                            st.write(f"**Annual Visitors:** {row['visitors_annual']:,}")
                            st.write(row['description'])
                    
                    st.markdown("---")
    
    if not recommendation_mode and 'tab3' in locals():
        with tab3:
            st.subheader("Detailed Profiles of Hidden Cultural Gems")
            
            # Create a selection for specific destinations
            selected_destination = st.selectbox(
                "Select a Destination to Explore",
                options=sorted(hidden_gems_data['name'])
            )
            
            # Display detailed information about the selected destination
            destination_data = hidden_gems_data[hidden_gems_data['name'] == selected_destination].iloc[0]
            
            st.write(f"## {destination_data['name']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"### About {destination_data['name']}")
                st.write(destination_data['description'])
                
                st.write("### Cultural Significance")
                st.write(f"""
                {destination_data['name']} is known for its {destination_data['art_form']}, which represents
                an important aspect of the cultural heritage of {destination_data['state']}. This is one of
                India's lesser-known cultural treasures, receiving only about {destination_data['visitors_annual']:,}
                visitors annually, which helps preserve its authenticity and traditional character.
                """)
            
            with col2:
                st.write("### Visitor Information")
                st.write(f"**State:** {destination_data['state']}")
                st.write(f"**Art Form:** {destination_data['art_form']}")
                st.write(f"**Accessibility:** {destination_data['accessibility']}")
                st.write(f"**Best Time to Visit:** {destination_data['best_time_to_visit']}")
                st.write(f"**Annual Visitors:** {destination_data['visitors_annual']:,}")
                
                # Create a mini map for just this destination
                m = folium.Map(location=[destination_data['latitude'], destination_data['longitude']], zoom_start=8)
                folium.Marker(
                    location=[destination_data['latitude'], destination_data['longitude']],
                    tooltip=destination_data['name'],
                    icon=folium.Icon(icon="gem", prefix="fa", color="purple")
                ).add_to(m)
                
                st_folium(m, width=400, height=300)
            
            st.write("### Explore Nearby Hidden Gems")
            
            # Calculate distances to other destinations
            def haversine_distance(lat1, lon1, lat2, lon2):
                """Calculate the great circle distance between two points in kilometers."""
                R = 6371  # Earth radius in kilometers
                
                lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                c = 2 * np.arcsin(np.sqrt(a))
                
                return R * c
            
            # Calculate distances from selected destination to all others
            distances = []
            for idx, row in hidden_gems_data.iterrows():
                if row['name'] != selected_destination:
                    distance = haversine_distance(
                        destination_data['latitude'], destination_data['longitude'],
                        row['latitude'], row['longitude']
                    )
                    distances.append((row['name'], distance, row['state'], row['art_form']))
            
            # Sort by distance and get the closest 3
            distances.sort(key=lambda x: x[1])
            closest_destinations = distances[:3]
            
            # Display closest destinations
            for name, distance, state, art_form in closest_destinations:
                st.write(f"**{name}** ({state}) - {distance:.1f} km away")
                st.write(f"Known for: {art_form}")
                st.write("---")
    
    # Only show comparison chart and downloads in non-recommendation mode
    if not recommendation_mode:
        # Comparison chart
        st.subheader("Comparing Visitor Numbers at Hidden Gems")
        
        # Create a bar chart of visitor numbers
        visitor_data = hidden_gems_data[['name', 'visitors_annual']].sort_values('visitors_annual')
        
        fig = create_bar_chart(
            visitor_data,
            'name',
            'visitors_annual',
            title="Annual Visitors to Hidden Cultural Gems"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        The chart above compares the annual visitor numbers across different hidden cultural gems.
        Lower visitor numbers often indicate more authentic and less commercialized cultural experiences,
        though they may come with challenges in accessibility or accommodations.
        """)
        
        # Download options
        st.subheader("Download Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = hidden_gems_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Hidden Gems Data as CSV",
                data=csv,
                file_name="india_hidden_cultural_gems.csv",
                mime="text/csv"
            )
        
        with col2:
            st.write("""
            This data includes information about lesser-known cultural destinations across India,
            including their locations, art forms, accessibility, and visitor numbers.
            """)
    else:
        # Show travel tips for recommendation mode at the end
        if not st.session_state.get('recommendations_submitted', False):
            st.info("Fill in your preferences and click 'Get Personalized Recommendations' to discover cultural destinations that match your interests.")
            
            # Add some information about what makes a good cultural travel experience
            st.subheader("Tips for Cultural Tourism in India")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
                    <h4 style="color: #FF9800;">Best Times to Visit</h4>
                    <p>October to March is generally the best time to visit most parts of India for cultural tourism, 
                    offering pleasant weather for exploration.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
                    <h4 style="color: #FF9800;">Cultural Etiquette</h4>
                    <p>Research local customs before your visit. When visiting religious sites, dress modestly 
                    and remove shoes when required.</p>
                </div>
                """, unsafe_allow_html=True)
