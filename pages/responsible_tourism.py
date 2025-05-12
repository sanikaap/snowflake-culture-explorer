import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from utils.data_loader import load_responsible_tourism_data, load_art_forms_data
from utils.visualization import create_bar_chart, create_altair_chart

def show_responsible_tourism_page():
    """
    Display the Responsible Tourism page.
    """
    st.title("🌿 Responsible Cultural Tourism")
    
    st.write("""
    As interest in cultural tourism grows, so does the importance of responsible and sustainable tourism practices.
    This section explores initiatives promoting responsible cultural tourism in India, ethical considerations
    for travelers, and guidelines for supporting local communities and preserving cultural heritage.
    
    Discover how to experience India's rich cultural tapestry while making a positive impact.
    """)
    
    # Load data
    responsible_data = load_responsible_tourism_data()
    art_forms_data = load_art_forms_data()
    
    if responsible_data is None:
        st.error("Unable to load responsible tourism data. Please try again later.")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Key Initiatives", "Traveler Guidelines", "Impact Measurement", "Case Studies"])
    
    with tab1:
        st.subheader("Key Responsible Tourism Initiatives")
        
        # Filter initiatives by focus area
        focus_areas = sorted(responsible_data['focus_area'].unique())
        selected_focus = st.multiselect(
            "Filter by Focus Area",
            options=focus_areas,
            default=[]
        )
        
        filtered_initiatives = responsible_data
        if selected_focus:
            filtered_initiatives = filtered_initiatives[filtered_initiatives['focus_area'].isin(selected_focus)]
        
        # Display initiatives
        if filtered_initiatives.empty:
            st.warning("No initiatives match the selected focus areas. Please adjust your selection.")
        else:
            st.write(f"Displaying {len(filtered_initiatives)} initiatives")
            
            # Sort by impact score
            sorted_initiatives = filtered_initiatives.sort_values('impact_score', ascending=False)
            
            for i, (_, initiative) in enumerate(sorted_initiatives.iterrows()):
                with st.expander(f"{initiative['initiative_name']} ({initiative['state']})", expanded=i==0):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Focus Area:** {initiative['focus_area']}")
                        st.write(f"**Description:** {initiative['description']}")
                        st.write(f"**Year Started:** {initiative['year_started']}")
                        st.write(f"**Website:** {initiative['website']}")
                    
                    with col2:
                        st.metric(
                            "Impact Score",
                            f"{initiative['impact_score']}/5",
                            delta=f"{initiative['beneficiaries']} beneficiaries"
                        )
        
        # Impact score distribution
        st.write("### Impact Score Distribution")
        
        # Create a histogram of impact scores
        fig = px.histogram(
            responsible_data,
            x="impact_score",
            nbins=10,
            title="Distribution of Initiative Impact Scores",
            color_discrete_sequence=["#3498db"]
        )
        
        fig.update_layout(
            xaxis_title="Impact Score (out of 5)",
            yaxis_title="Number of Initiatives",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Initiative timeline
        st.write("### Timeline of Responsible Tourism Initiatives")
        
        # Create a timeline of when initiatives started
        timeline_data = responsible_data.groupby('year_started').size().reset_index(name='count')
        timeline_data['cumulative'] = timeline_data['count'].cumsum()
        
        fig2 = px.line(
            timeline_data,
            x="year_started",
            y="cumulative",
            title="Cumulative Growth of Responsible Tourism Initiatives",
            markers=True
        )
        
        fig2.update_layout(
            xaxis_title="Year",
            yaxis_title="Cumulative Number of Initiatives",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("Guidelines for Responsible Cultural Tourism")
        
        st.write("""
        ### Responsible Cultural Tourism: A Traveler's Guide
        
        When experiencing India's rich cultural heritage, consider these guidelines to ensure your
        visit has a positive impact on local communities and helps preserve cultural traditions.
        """)
        
        # Create expandable sections for different guidelines
        with st.expander("Support Local Communities", expanded=True):
            st.markdown("""
            - **Buy directly from artisans** whenever possible, ensuring they receive fair compensation
            - **Stay in locally-owned accommodations** rather than international hotel chains
            - **Hire local guides** who have deep knowledge of cultural traditions and history
            - **Eat at local restaurants** serving traditional cuisine using local ingredients
            - **Participate in community-based tourism initiatives** that benefit local populations
            """)
        
        with st.expander("Respect Cultural Sensitivities"):
            st.markdown("""
            - **Research local customs** before your visit to understand appropriate behavior
            - **Dress modestly** when visiting religious sites and traditional communities
            - **Ask permission before photographing** people, ceremonies, or religious practices
            - **Remove shoes** when entering temples, homes, and certain cultural sites
            - **Avoid public displays of affection** which may be considered inappropriate
            - **Learn a few words in the local language** as a sign of respect
            """)
        
        with st.expander("Minimize Environmental Impact"):
            st.markdown("""
            - **Reduce plastic waste** by carrying a reusable water bottle and shopping bag
            - **Dispose of waste properly** and participate in clean-up initiatives
            - **Use public transportation or shared vehicles** to reduce carbon emissions
            - **Choose eco-friendly accommodations** that implement sustainable practices
            - **Conserve water and energy** during your stay, especially in water-scarce regions
            """)
        
        with st.expander("Protect Cultural Heritage"):
            st.markdown("""
            - **Never purchase antiquities or historical artifacts**, which contributes to looting
            - **Follow all site rules** at monuments, temples, and heritage locations
            - **Support conservation efforts** through donations or volunteer work
            - **Engage with authentic cultural experiences** rather than commercialized shows
            - **Respect "no photography" signs** at cultural sites and museums
            """)
        
        # Certification programs
        st.write("### Responsible Tourism Certification Programs")
        
        cert_data = {
            "Certification": [
                "Responsible Tourism Classification", 
                "India Heritage Tourism Certification",
                "Green Leaf Certification",
                "Cultural Heritage Preservation Award",
                "Sustainable Communities Certification"
            ],
            "Focus": [
                "Comprehensive sustainability assessment",
                "Heritage preservation and interpretation",
                "Environmental sustainability in tourism",
                "Protection of tangible and intangible heritage",
                "Community benefits and involvement"
            ],
            "Authority": [
                "Ministry of Tourism, Government of India",
                "Indian Heritage Cities Network",
                "Kerala Tourism Department",
                "INTACH (Indian National Trust for Art and Cultural Heritage)",
                "Responsible Tourism Society of India"
            ]
        }
        
        cert_df = pd.DataFrame(cert_data)
        st.table(cert_df)
        
        # Ethical dilemmas
        st.write("### Navigating Ethical Dilemmas in Cultural Tourism")
        
        ethical_data = {
            "Dilemma": [
                "Photographing religious ceremonies",
                "Visiting tribal communities",
                "Purchasing traditional crafts",
                "Participating in festivals",
                "Visiting religious sites as a non-believer"
            ],
            "Considerations": [
                "May disturb worshippers; commercializes sacred practices",
                "Risk of treating communities as 'human zoos'; disruption of lifestyle",
                "Authenticity concerns; fair compensation for artisans",
                "Increased crowds may alter traditional celebrations",
                "Respect for sacred spaces; understanding religious significance"
            ],
            "Responsible Approach": [
                "Ask permission; attend public ceremonies only; be unobtrusive",
                "Use community-approved tour operators; limit group sizes; respect privacy",
                "Buy directly from artisans; learn about techniques; respect fair pricing",
                "Research cultural context; participate respectfully; follow local customs",
                "Observe dress codes; follow behavioral guidelines; show genuine interest"
            ]
        }
        
        ethical_df = pd.DataFrame(ethical_data)
        st.dataframe(ethical_df)
    
    with tab3:
        st.subheader("Measuring the Impact of Responsible Tourism")
        
        st.write("""
        Measuring the impact of responsible tourism initiatives is essential for understanding their
        effectiveness and ensuring they deliver meaningful benefits to communities and cultural heritage.
        """)
        
        # Impact metrics visualization
        impact_data = responsible_data[['initiative_name', 'impact_score', 'beneficiaries', 'year_started']]
        
        # Create an interactive scatter plot
        fig = px.scatter(
            impact_data,
            x="year_started",
            y="impact_score",
            size="beneficiaries",
            hover_name="initiative_name",
            title="Impact Assessment of Responsible Tourism Initiatives",
            labels={
                "year_started": "Year Established",
                "impact_score": "Impact Score (out of 5)",
                "beneficiaries": "Number of Beneficiaries"
            },
            color_discrete_sequence=["#1f77b4"]
        )
        
        fig.update_layout(
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        The visualization above shows the relationship between when initiatives were established,
        their impact scores, and the number of beneficiaries they serve. Newer initiatives may show
        promising impact scores but often reach fewer beneficiaries initially.
        """)
        
        # Impact by focus area
        st.write("### Impact by Focus Area")
        
        focus_impact = responsible_data.groupby('focus_area').agg({
            'impact_score': 'mean',
            'beneficiaries': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a bar chart for average impact score by focus area
            fig1 = create_bar_chart(
                focus_impact.sort_values('impact_score', ascending=False),
                'focus_area',
                'impact_score',
                title="Average Impact Score by Focus Area"
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Create a bar chart for total beneficiaries by focus area
            fig2 = create_bar_chart(
                focus_impact.sort_values('beneficiaries', ascending=False),
                'focus_area',
                'beneficiaries',
                title="Total Beneficiaries by Focus Area"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Key performance indicators
        st.write("### Key Performance Indicators for Responsible Tourism")
        
        kpi_data = {
            "Category": [
                "Economic", "Economic", "Economic",
                "Social", "Social", "Social",
                "Cultural", "Cultural", "Cultural",
                "Environmental", "Environmental", "Environmental"
            ],
            "KPI": [
                "Local Employment Generation",
                "Artisan Income Increase",
                "Local Business Support",
                "Community Participation",
                "Women's Empowerment",
                "Skills Development",
                "Cultural Preservation",
                "Traditional Knowledge Transfer",
                "Authentic Experience Creation",
                "Waste Reduction",
                "Resource Conservation",
                "Sustainable Practices Adoption"
            ],
            "Measurement Method": [
                "Number of local jobs created",
                "Percentage increase in artisan income",
                "Number of local businesses in supply chain",
                "Percentage of community members involved",
                "Number of women-led enterprises",
                "Number of training programs conducted",
                "Documentation of cultural practices",
                "Number of apprenticeship programs",
                "Visitor satisfaction surveys",
                "Waste audit records",
                "Resource consumption monitoring",
                "Certification achievements"
            ]
        }
        
        kpi_df = pd.DataFrame(kpi_data)
        
        # Create a grouped table
        st.dataframe(kpi_df, use_container_width=True)
    
    with tab4:
        st.subheader("Case Studies in Responsible Cultural Tourism")
        
        # Create a selectbox for case study selection
        case_study = st.selectbox(
            "Select a Case Study",
            options=[
                "Village Homestay Program (Himachal Pradesh)",
                "Women Artisans Cooperative (Odisha)",
                "Heritage Conservation Volunteers (Maharashtra)",
                "Indigenous Knowledge Preservation (Nagaland)"
            ]
        )
        
        # Display the selected case study
        if case_study == "Village Homestay Program (Himachal Pradesh)":
            st.write("### Village Homestay Program (Himachal Pradesh)")
            
            st.write("""
            #### Background
            
            The Village Homestay Program in Himachal Pradesh connects travelers with local families in remote
            mountain villages, offering authentic cultural experiences while creating sustainable income
            opportunities for rural communities.
            
            #### Implementation
            
            - Started in 2015 with 10 families in 3 villages
            - Provided training in hospitality, sanitation, and cultural interpretation
            - Established quality standards and fair pricing guidelines
            - Created online booking platform connecting travelers directly to host families
            - Developed cultural experience packages showcasing local traditions, crafts, and cuisine
            
            #### Impact
            
            - Economic: 150 families now earn supplemental income, average household income increased by 35%
            - Cultural: Revival of traditional cooking methods, folk music, and craft practices
            - Social: Reduced youth migration to cities, increased women's participation in decision-making
            - Environmental: Implementation of waste management systems and solar power in participating villages
            
            #### Challenges & Solutions
            
            - Initial resistance from communities was addressed through transparent communication and early success stories
            - Balancing authentic experiences with visitor comfort required targeted infrastructure improvements
            - Seasonal tourism fluctuation was mitigated by developing winter cultural packages
            
            #### Key Lessons
            
            - Community ownership is essential for sustainable tourism initiatives
            - Gradual scaling prevents overwhelming cultural and environmental systems
            - Direct booking connections maximize economic benefits to communities
            """)
            
        elif case_study == "Women Artisans Cooperative (Odisha)":
            st.write("### Women Artisans Cooperative (Odisha)")
            
            st.write("""
            #### Background
            
            The Women Artisans Cooperative in Odisha was established to preserve traditional textile arts
            while empowering women economically through sustainable tourism and direct market access.
            
            #### Implementation
            
            - Founded in 2013 with 25 women artisans specializing in traditional ikat weaving
            - Created a central production and visitor center in a historic building
            - Developed artisan-led workshops for visitors to learn traditional techniques
            - Established direct sales channels eliminating exploitative middlemen
            - Implemented a profit-sharing model benefiting both individual artisans and community projects
            
            #### Impact
            
            - Economic: 120 women artisans now earn living wages, income increased 3-4 times pre-cooperative levels
            - Cultural: Documented 15 endangered weaving techniques, revived natural dyeing processes
            - Social: Funded a community health center and education programs for girls
            - Environmental: Transitioned to natural, locally-sourced dyes and sustainable materials
            
            #### Challenges & Solutions
            
            - Quality consistency was addressed through mentorship programs pairing experienced and new artisans
            - Market fluctuations were balanced by developing both tourism and export markets
            - Competition from machine-made replicas was countered through authentication processes and education
            
            #### Key Lessons
            
            - Women's economic empowerment creates ripple effects throughout communities
            - Cultural preservation requires both documentation and creating economic incentives
            - Transparent supply chains build visitor trust and willingness to pay fair prices
            """)
            
        elif case_study == "Heritage Conservation Volunteers (Maharashtra)":
            st.write("### Heritage Conservation Volunteers (Maharashtra)")
            
            st.write("""
            #### Background
            
            The Heritage Conservation Volunteers program in Maharashtra engages tourists in the preservation
            of historical sites while providing educational experiences and supporting local conservation efforts.
            
            #### Implementation
            
            - Launched in 2016 at three heritage sites facing conservation challenges
            - Developed structured volunteer programs ranging from one day to two weeks
            - Created training modules on traditional conservation techniques
            - Partnered with local conservation experts and community elders
            - Established a heritage adoption system where visitor fees directly fund specific restoration projects
            
            #### Impact
            
            - Conservation: Successfully restored five endangered heritage structures using traditional methods
            - Educational: Over 2,000 visitors participated in hands-on conservation activities
            - Community: 90 local residents trained in heritage conservation techniques
            - Economic: Created sustainable employment for local craftspeople specializing in traditional building methods
            
            #### Challenges & Solutions
            
            - Balancing conservation integrity with visitor participation required careful activity design
            - Administrative hurdles were overcome through partnerships with heritage authorities
            - Seasonal variations in volunteer numbers were addressed through year-round local conservation teams
            
            #### Key Lessons
            
            - Experiential learning creates deeper visitor connections to cultural heritage
            - Transparent project outcomes build donor and volunteer confidence
            - Combining traditional knowledge with visitor enthusiasm creates sustainable conservation models
            """)
            
        elif case_study == "Indigenous Knowledge Preservation (Nagaland)":
            st.write("### Indigenous Knowledge Preservation (Nagaland)")
            
            st.write("""
            #### Background
            
            The Indigenous Knowledge Preservation project in Nagaland works to document, protect, and
            revitalize traditional ecological and cultural knowledge through community-based tourism initiatives.
            
            #### Implementation
            
            - Established in 2014 across five Naga villages with distinct cultural traditions
            - Created a digital archive of traditional knowledge with community ownership of intellectual property
            - Developed cultural immersion experiences led by tribal elders and knowledge keepers
            - Implemented a knowledge transmission program pairing elders with youth
            - Established ethical guidelines for visitor interactions with sacred knowledge and practices
            
            #### Impact
            
            - Cultural: Documented over 300 traditional practices, songs, and stories previously unrecorded
            - Intergenerational: 85 young community members actively learning traditional practices
            - Economic: Created non-extractive income opportunities in remote communities
            - Environmental: Revitalized traditional sustainable forest management practices
            
            #### Challenges & Solutions
            
            - Cultural appropriation concerns were addressed through strict visitor guidelines and education
            - Balancing privacy and sharing was managed through community-determined boundaries
            - Technology adoption barriers were overcome through youth-elder collaboration teams
            
            #### Key Lessons
            
            - Indigenous communities must retain control over how their culture is presented
            - Visitor education before cultural encounters prevents harmful interactions
            - Digital preservation complements but cannot replace lived cultural transmission
            """)
    
    # Visitor guidelines for responsible cultural tourism
    st.subheader("Guidelines for Responsible Cultural Tourism")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <h3 style="color: #2e7d32;">Responsible Tourism Mission Kerala</h3>
            <p>An initiative by Kerala Tourism that implements responsible tourism practices</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write("""
        When visiting India's cultural sites and experiencing traditional art forms, remember these key principles:
        
        - **Respect cultural practices** and follow local customs and etiquette
        - **Support local artisans** by purchasing directly from them when possible
        - **Ask permission before photographing** people or cultural practices
        - **Learn about the cultural context** before visiting sites or attending performances
        - **Minimize environmental impact** through responsible waste management
        - **Contribute to conservation efforts** through responsible operators
        """)
    
    # Download options
    st.subheader("Download Data and Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = responsible_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Responsible Tourism Data as CSV",
            data=csv,
            file_name="india_responsible_tourism_initiatives.csv",
            mime="text/csv"
        )
    
    with col2:
        st.write("""
        This data includes information about responsible tourism initiatives across India,
        including their focus areas, impact scores, and beneficiary numbers.
        """)
