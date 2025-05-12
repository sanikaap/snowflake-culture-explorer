import pandas as pd
import numpy as np
import requests
import json
import os
import streamlit as st

# Cache the data loading to improve performance
@st.cache_data(ttl=3600)
def load_art_forms_data():
    """
    Load data about Indian traditional art forms from data.gov.in or a similar source.
    If the API call fails, return sample data with a warning.
    
    Returns:
        pandas.DataFrame: DataFrame containing art forms data
    """
    try:
        # Try to fetch data from data.gov.in
        # This URL should be replaced with the actual API endpoint
        api_url = "https://api.data.gov.in/resource/cultural-art-forms"
        
        # Attempt to get data from API
        try:
            # For actual implementation, use your API key from environment variables
            # api_key = os.getenv("DATA_GOV_IN_API_KEY")
            # response = requests.get(api_url, headers={"api-key": api_key})
            
            # Since we don't have actual API access in this example,
            # we'll create a structured DataFrame similar to what we'd expect
            data = {
                "state": [
                    "Rajasthan", "Gujarat", "West Bengal", "Kerala", "Uttar Pradesh",
                    "Maharashtra", "Tamil Nadu", "Odisha", "Assam", "Karnataka",
                    "Madhya Pradesh", "Andhra Pradesh", "Telangana", "Bihar", "Punjab",
                    "Jammu and Kashmir", "Himachal Pradesh", "Uttarakhand", "Goa",
                    "Manipur", "Nagaland", "Tripura", "Meghalaya", "Arunachal Pradesh"
                ],
                "art_form": [
                    "Kathputli", "Patola", "Chhau Dance", "Kathakali", "Nautanki",
                    "Warli", "Bharatanatyam", "Pattachitra", "Bihu", "Yakshagana",
                    "Gond Art", "Kalamkari", "Bidri", "Madhubani", "Phulkari",
                    "Pashmina", "Kangra Painting", "Aipan", "Goan Folk Dance",
                    "Manipuri Dance", "Naga Wood Carving", "Risa Textile", "Khasi Bamboo Work", "Monpa Mask Making"
                ],
                "type": [
                    "Puppetry", "Textile", "Dance", "Dance", "Theater",
                    "Painting", "Dance", "Painting", "Dance", "Theater",
                    "Painting", "Textile", "Metal Craft", "Painting", "Embroidery",
                    "Textile", "Painting", "Folk Art", "Dance", 
                    "Dance", "Wood Craft", "Textile", "Craft", "Mask Making"
                ],
                "description": [
                    "Traditional string puppet theater of Rajasthan",
                    "Ancient art of double ikat weaving in Gujarat",
                    "Traditional martial dance-drama from eastern India",
                    "Classical dance-drama known for elaborate costumes and makeup",
                    "Folk theater tradition of northern India",
                    "Tribal art form featuring geometric patterns",
                    "One of India's oldest classical dance traditions",
                    "Ancient scroll painting tradition of Odisha",
                    "Folk dance associated with the Bihu festival of Assam",
                    "Traditional theater form of Karnataka",
                    "Indigenous art style of central India",
                    "Hand-painted or block-printed cotton textile",
                    "Metal handicraft with silver inlay work",
                    "Distinctive painting style using natural dyes",
                    "Traditional embroidery technique of Punjab",
                    "Fine wool textile craftsmanship",
                    "Miniature painting tradition of Himachal Pradesh",
                    "Ritual folk art using rice paste",
                    "Vibrant folk dance traditions",
                    "Classical dance form with graceful movements",
                    "Intricate wood carving traditions",
                    "Traditional handwoven textile",
                    "Traditional bamboo craftsmanship",
                    "Religious and cultural mask making tradition"
                ],
                "latitude": [
                    26.9124, 22.2587, 23.6102, 10.8505, 27.5706,
                    19.7515, 13.0827, 20.9517, 26.2006, 13.2856,
                    22.9734, 15.9129, 17.3850, 25.0961, 31.1471,
                    34.0837, 32.2196, 30.0668, 15.2993,
                    24.6637, 26.1584, 23.9408, 25.5788, 27.1004
                ],
                "longitude": [
                    75.7873, 71.1924, 87.4594, 76.2711, 80.0982,
                    75.7139, 80.2707, 85.0985, 91.7086, 75.7129,
                    78.6569, 79.7400, 78.4867, 85.3131, 75.3412,
                    77.5677, 76.3189, 79.0193, 73.9934,
                    93.9063, 94.5624, 91.9882, 91.8933, 93.6167
                ],
                "visitors_annual": [
                    150000, 120000, 85000, 200000, 90000,
                    110000, 180000, 75000, 95000, 70000,
                    65000, 100000, 55000, 80000, 90000,
                    110000, 60000, 45000, 300000,
                    50000, 30000, 25000, 35000, 20000
                ],
                "cultural_significance": [
                    "High", "High", "Medium", "High", "Medium",
                    "Medium", "High", "Medium", "Medium", "Medium",
                    "Medium", "High", "Medium", "High", "Medium",
                    "Medium", "Medium", "Low", "Medium",
                    "High", "Medium", "Low", "Low", "Medium"
                ]
            }
            
            df = pd.DataFrame(data)
            return df
            
        except requests.exceptions.RequestException as e:
            st.warning(f"Could not fetch data from data.gov.in API: {e}")
            # Return a structured DataFrame as a fallback
            # Using the same data structure as above
            return pd.DataFrame(data)
    
    except Exception as e:
        st.error(f"Error loading art forms data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_tourism_data():
    """
    Load tourism data related to cultural sites in India.
    
    Returns:
        pandas.DataFrame: DataFrame containing tourism data
    """
    try:
        # In a real scenario, we would fetch this from an API or database
        # Creating a structured dataset for the purpose of this application
        data = {
            "year": np.repeat(range(2015, 2023), 10),
            "state": np.tile([
                "Rajasthan", "Gujarat", "West Bengal", "Kerala", "Uttar Pradesh",
                "Maharashtra", "Tamil Nadu", "Odisha", "Assam", "Karnataka"
            ], 8),
            "domestic_tourists": [
                # 2015
                3500000, 2800000, 2500000, 3200000, 4500000, 
                4800000, 3900000, 1800000, 1200000, 2900000,
                # 2016
                3700000, 3000000, 2700000, 3400000, 4700000,
                5000000, 4100000, 1900000, 1300000, 3100000,
                # 2017
                3900000, 3200000, 2900000, 3600000, 4900000,
                5200000, 4300000, 2000000, 1400000, 3300000,
                # 2018
                4100000, 3400000, 3100000, 3800000, 5100000,
                5400000, 4500000, 2100000, 1500000, 3500000,
                # 2019
                4300000, 3600000, 3300000, 4000000, 5300000,
                5600000, 4700000, 2200000, 1600000, 3700000,
                # 2020
                1500000, 1200000, 1100000, 1300000, 1800000,
                1900000, 1600000, 800000, 600000, 1300000,
                # 2021
                2200000, 1800000, 1600000, 2000000, 2700000,
                2800000, 2400000, 1200000, 900000, 1900000,
                # 2022
                3800000, 3200000, 2900000, 3500000, 4600000,
                4900000, 4100000, 1900000, 1300000, 3200000
            ],
            "international_tourists": [
                # 2015
                800000, 450000, 350000, 600000, 900000,
                1100000, 750000, 200000, 100000, 400000,
                # 2016
                850000, 480000, 380000, 640000, 950000,
                1150000, 800000, 220000, 110000, 430000,
                # 2017
                900000, 510000, 410000, 680000, 1000000,
                1200000, 850000, 240000, 120000, 460000,
                # 2018
                950000, 540000, 440000, 720000, 1050000,
                1250000, 900000, 260000, 130000, 490000,
                # 2019
                1000000, 570000, 470000, 760000, 1100000,
                1300000, 950000, 280000, 140000, 520000,
                # 2020
                250000, 140000, 120000, 190000, 280000,
                330000, 240000, 70000, 35000, 130000,
                # 2021
                400000, 230000, 190000, 300000, 450000,
                520000, 380000, 110000, 60000, 210000,
                # 2022
                800000, 450000, 370000, 600000, 900000,
                1050000, 750000, 210000, 100000, 420000
            ],
            "cultural_site_visits": [
                # 2015
                1500000, 900000, 800000, 1200000, 2000000,
                1800000, 1400000, 500000, 300000, 800000,
                # 2016
                1600000, 950000, 850000, 1280000, 2100000,
                1900000, 1500000, 530000, 320000, 850000,
                # 2017
                1700000, 1000000, 900000, 1360000, 2200000,
                2000000, 1600000, 560000, 340000, 900000,
                # 2018
                1800000, 1050000, 950000, 1440000, 2300000,
                2100000, 1700000, 590000, 360000, 950000,
                # 2019
                1900000, 1100000, 1000000, 1520000, 2400000,
                2200000, 1800000, 620000, 380000, 1000000,
                # 2020
                600000, 350000, 320000, 480000, 800000,
                700000, 570000, 200000, 120000, 320000,
                # 2021
                900000, 530000, 480000, 720000, 1200000,
                1050000, 860000, 300000, 180000, 480000,
                # 2022
                1600000, 950000, 860000, 1300000, 2150000,
                1900000, 1550000, 540000, 320000, 870000
            ],
            "revenue_millions_inr": [
                # 2015
                350, 220, 180, 290, 420,
                480, 350, 120, 80, 200,
                # 2016
                380, 240, 200, 310, 450,
                510, 380, 130, 90, 220,
                # 2017
                410, 260, 220, 330, 480,
                540, 410, 140, 100, 240,
                # 2018
                440, 280, 240, 350, 510,
                570, 440, 150, 110, 260,
                # 2019
                470, 300, 260, 370, 540,
                600, 470, 160, 120, 280,
                # 2020
                150, 100, 80, 120, 180,
                190, 150, 50, 40, 90,
                # 2021
                230, 150, 130, 180, 270,
                290, 230, 80, 60, 140,
                # 2022
                410, 270, 230, 320, 480,
                540, 410, 140, 100, 240
            ]
        }
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        st.error(f"Error loading tourism data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_hidden_gems_data():
    """
    Load data about lesser-known cultural destinations in India.
    
    Returns:
        pandas.DataFrame: DataFrame containing hidden gems data
    """
    try:
        # In a real scenario, we would fetch this from an API or database
        data = {
            "name": [
                "Nubra Valley", "Ziro Valley", "Majuli Island", "Champaner-Pavagadh",
                "Shekhawati Region", "Chettinad", "Dhanushkodi", "Andro Village",
                "Longwa Village", "Mawlynnong", "Andretta", "Chitrakote Falls",
                "Unakoti", "Nako", "Gurez Valley", "Mechuka", "Patan",
                "Orchha", "Valparai", "Tawang Monastery"
            ],
            "state": [
                "Ladakh", "Arunachal Pradesh", "Assam", "Gujarat",
                "Rajasthan", "Tamil Nadu", "Tamil Nadu", "Manipur",
                "Nagaland", "Meghalaya", "Himachal Pradesh", "Chhattisgarh",
                "Tripura", "Himachal Pradesh", "Jammu and Kashmir", "Arunachal Pradesh", "Gujarat",
                "Madhya Pradesh", "Tamil Nadu", "Arunachal Pradesh"
            ],
            "art_form": [
                "Thangka Painting", "Apatani Textile", "Mask Making", "Archaeological Heritage",
                "Fresco Painting", "Wood Carving", "Temple Architecture", "Pottery",
                "Wood Carving", "Bamboo Craft", "Pottery and Paintings", "Tribal Arts",
                "Rock Reliefs", "Thangka Painting", "Pashmina Weaving", "Tribal Weaving", "Patola Weaving",
                "Miniature Paintings", "Native Crafts", "Buddhist Thangkas"
            ],
            "latitude": [
                34.6989, 27.5949, 27.0014, 22.4866,
                27.6094, 10.5702, 9.1550, 24.7638,
                26.5693, 25.1982, 32.0398, 19.2307,
                24.0865, 31.8834, 34.6333, 28.9891, 23.8493,
                25.3518, 10.3271, 27.5859
            ],
            "longitude": [
                77.5619, 93.8290, 94.2300, 73.5333,
                75.3025, 78.7146, 79.3963, 94.0210,
                95.0610, 91.5767, 76.2082, 81.7200,
                91.9286, 77.9333, 74.8500, 94.9190, 72.1194,
                78.6582, 76.9512, 91.8566
            ],
            "description": [
                "Remote valley known for unique cultural traditions and Buddhist influence",
                "Home to the Apatani tribe known for their sustainable agriculture and unique nose plugs",
                "World's largest river island with a unique vaishnava culture and mask-making tradition",
                "Archaeological park with a blend of Hindu and Islamic architecture",
                "Open-air art gallery with hundreds of ornate havelis decorated with vibrant frescoes",
                "Mansions of wealthy traders featuring unique architecture and wood carvings",
                "Ghost town with abandoned structures and rich cultural history",
                "Cultural village known for pottery and traditional liquor brewing",
                "Village split between India and Myanmar, home to tattooed Konyak tribe headhunters",
                "Known as Asia's cleanest village with unique living root bridges",
                "Artists' colony established by Sardar Gurcharan Singh with pottery traditions",
                "Horseshoe-shaped waterfall with tribal communities preserving ancient art forms",
                "Ancient rock-cut sculptures and stone images dating back to 7-9th centuries",
                "Tiny Himalayan village with Buddhist monastery and traditional architecture",
                "Remote valley with unique Dard-Shin culture and traditional craftsmanship",
                "Remote valley with traditional Memba tribe culture and monasteries",
                "Ancient city famous for its Patola silk double-ikat textile tradition",
                "Medieval town with grand cenotaphs and Bundela architecture",
                "Tea plantation region with unique cultural blend and craft traditions",
                "Largest monastery in India with rare Buddhist artifacts and manuscripts"
            ],
            "visitors_annual": [
                8000, 5000, 10000, 12000,
                15000, 20000, 25000, 3000,
                2000, 18000, 7000, 12000,
                9000, 4000, 3000, 2000, 25000,
                35000, 15000, 20000
            ],
            "accessibility": [
                "Moderate", "Difficult", "Moderate", "Easy",
                "Easy", "Easy", "Moderate", "Difficult",
                "Difficult", "Moderate", "Moderate", "Moderate",
                "Moderate", "Difficult", "Difficult", "Difficult", "Easy",
                "Easy", "Moderate", "Moderate"
            ],
            "best_time_to_visit": [
                "May-September", "March-October", "November-March", "October-March",
                "October-March", "November-February", "October-March", "October-March",
                "October-April", "September-May", "March-November", "September-February",
                "October-March", "May-October", "July-September", "March-October", "October-March",
                "October-March", "September-May", "March-October"
            ]
        }
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        st.error(f"Error loading hidden gems data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_responsible_tourism_data():
    """
    Load data about responsible tourism initiatives and guidelines.
    
    Returns:
        pandas.DataFrame: DataFrame containing responsible tourism data
    """
    try:
        # In a real scenario, we would fetch this from an API or database
        data = {
            "initiative_name": [
                "Village Homestay Program", "Eco-Cultural Tours", "Artisan Direct",
                "Heritage Conservation Volunteers", "Rural Art Immersion", "Zero Waste Cultural Festivals",
                "Indigenous Knowledge Preservation", "Community Museum Network", "Cultural Exchange Program",
                "Sustainable Craft Tourism", "Women Artisans Cooperative", "Traditional Food Tours",
                "Cultural Heritage Protection Fund", "Green Temple Initiative", "Living Traditions Documentation"
            ],
            "state": [
                "Himachal Pradesh", "Kerala", "Rajasthan",
                "Maharashtra", "West Bengal", "Goa",
                "Nagaland", "Tamil Nadu", "Karnataka",
                "Gujarat", "Odisha", "Punjab",
                "Multiple States", "Multiple States", "Multiple States"
            ],
            "focus_area": [
                "Rural Tourism", "Eco-Tourism", "Craft Tourism",
                "Heritage Conservation", "Art Education", "Waste Management",
                "Knowledge Preservation", "Museum Development", "Cultural Exchange",
                "Sustainable Crafts", "Women Empowerment", "Culinary Tourism",
                "Heritage Protection", "Religious Tourism", "Cultural Documentation"
            ],
            "description": [
                "Connects travelers with village families offering authentic homestays and cultural experiences",
                "Combines ecological conservation with cultural experiences in the backwaters and forests",
                "Platform connecting tourists directly to artisans, eliminating middlemen and increasing artisan income",
                "Engaging tourists in heritage conservation activities at historical sites",
                "Immersive workshops with traditional artists in rural Bengal",
                "Implementation of waste reduction strategies at cultural festivals and events",
                "Documentation and preservation of indigenous knowledge systems with community participation",
                "Network of small community-run museums showcasing local heritage",
                "Facilitating cultural exchange between tourists and local communities",
                "Promoting sustainable practices in craft production and tourism",
                "Supporting women artisans through cooperative business models and tourism",
                "Food tours highlighting traditional cuisines with focus on local ingredients",
                "Fund supporting community-led heritage conservation projects",
                "Initiative promoting sustainable practices at religious sites and temples",
                "Project documenting living cultural traditions across India"
            ],
            "impact_score": [
                4.5, 4.8, 4.3,
                3.9, 4.2, 4.0,
                4.7, 3.8, 4.1,
                4.4, 4.6, 4.2,
                3.9, 4.0, 4.3
            ],
            "year_started": [
                2015, 2010, 2018,
                2016, 2019, 2017,
                2014, 2018, 2012,
                2016, 2013, 2019,
                2017, 2018, 2015
            ],
            "beneficiaries": [
                150, 320, 200,
                90, 75, 110,
                85, 60, 250,
                180, 120, 80,
                300, 450, 200
            ],
            "website": [
                "himachalhomestays.org", "keralaecoculture.org", "artisandirect.in",
                "heritageconservation.org", "bengalartimmersion.org", "zerowastefestivals.in",
                "indigenousknowledge.org", "communitymuseums.in", "culturalexchangeindia.org",
                "sustainablecrafts.org", "odishawomenartisans.org", "punjabfoodtours.org",
                "heritageprotectionfund.in", "greentemples.org", "livingtraditions.in"
            ]
        }
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        st.error(f"Error loading responsible tourism data: {e}")
        return None

@st.cache_data
def load_india_geojson():
    """
    Load GeoJSON data for India's states.
    
    Returns:
        dict: GeoJSON data for India
    """
    try:
        # In a real scenario, we would fetch this from a file or API
        # Here we're creating a simplified version for demonstration
        with open('assets/india_states.geojson', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("India GeoJSON file not found. Using simplified data.")
        return create_simplified_india_geojson()
    except Exception as e:
        st.error(f"Error loading India GeoJSON: {e}")
        return None

def create_simplified_india_geojson():
    """
    Create a simplified GeoJSON for India's major states.
    This is a fallback if the real file isn't available.
    
    Returns:
        dict: Simplified GeoJSON data
    """
    # This is a very simplified representation and not geographically accurate
    # In a real app, you would use a proper GeoJSON file
    simplified_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"state": "Rajasthan"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[72.0, 27.0], [72.0, 28.0], [73.0, 28.0], [73.0, 27.0], [72.0, 27.0]]]
                }
            },
            {
                "type": "Feature",
                "properties": {"state": "Gujarat"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[70.0, 22.0], [70.0, 23.0], [71.0, 23.0], [71.0, 22.0], [70.0, 22.0]]]
                }
            },
            {
                "type": "Feature",
                "properties": {"state": "Maharashtra"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[73.0, 19.0], [73.0, 20.0], [74.0, 20.0], [74.0, 19.0], [73.0, 19.0]]]
                }
            }
        ]
    }
    return simplified_geojson
