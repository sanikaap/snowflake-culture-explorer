import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_tourism_data, load_art_forms_data
from utils.visualization import create_trend_chart, create_bar_chart, create_bubble_chart

def show_tourism_trends_page():
    """
    Display the Tourism Trends page.
    """
    st.title("📊 Tourism Trends to Cultural Hotspots")
    
    st.write("""
    Tourism plays a vital role in preserving and promoting cultural heritage. This section explores
    the trends in tourism to India's cultural hotspots over the years, providing insights into 
    visitor patterns, economic impact, and the relationship between tourism and cultural preservation.
    
    Analyze the visualizations below to understand how tourism to cultural sites has evolved.
    """)
    
    # Load data
    tourism_data = load_tourism_data()
    art_forms_data = load_art_forms_data()
    
    if tourism_data is None:
        st.error("Unable to load tourism data. Please try again later.")
        return
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Visitor Trends", "Economic Impact", "Domestic vs International", "State Analysis"])
    
    with tab1:
        st.subheader("Visitor Trends Over Time")
        
        # Year range selector
        year_range = st.slider(
            "Select Year Range",
            min_value=min(tourism_data['year']),
            max_value=max(tourism_data['year']),
            value=(min(tourism_data['year']), max(tourism_data['year']))
        )
        
        # Filter data by year range
        filtered_data = tourism_data[(tourism_data['year'] >= year_range[0]) & (tourism_data['year'] <= year_range[1])]
        
        # Group data by year
        yearly_data = filtered_data.groupby('year').agg({
            'domestic_tourists': 'sum',
            'international_tourists': 'sum',
            'cultural_site_visits': 'sum'
        }).reset_index()
        
        # Create a line chart for visitor trends
        fig = create_trend_chart(
            yearly_data,
            'year',
            'cultural_site_visits',
            title="Total Cultural Site Visits Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional trend chart for domestic and international tourists
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=yearly_data['year'],
            y=yearly_data['domestic_tourists'],
            mode='lines+markers',
            name='Domestic Tourists'
        ))
        
        fig2.add_trace(go.Scatter(
            x=yearly_data['year'],
            y=yearly_data['international_tourists'],
            mode='lines+markers',
            name='International Tourists'
        ))
        
        fig2.update_layout(
            title="Domestic vs International Tourist Numbers Over Time",
            xaxis_title="Year",
            yaxis_title="Number of Tourists",
            legend_title="Tourist Type",
            hovermode="x unified",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Impact of COVID-19
        st.write("### Impact of COVID-19 on Cultural Tourism")
        
        covid_data = tourism_data[tourism_data['year'].isin([2019, 2020, 2021, 2022])]
        covid_yearly = covid_data.groupby('year').agg({
            'cultural_site_visits': 'sum'
        }).reset_index()
        
        covid_change = pd.DataFrame({
            'Year': covid_yearly['year'],
            'Cultural Site Visits': covid_yearly['cultural_site_visits'],
            'Year-over-Year Change (%)': [0] + [
                ((covid_yearly['cultural_site_visits'].iloc[i] - covid_yearly['cultural_site_visits'].iloc[i-1]) / 
                 covid_yearly['cultural_site_visits'].iloc[i-1] * 100) 
                for i in range(1, len(covid_yearly))
            ]
        })
        
        st.write("""
        The COVID-19 pandemic had a significant impact on cultural tourism in India. 
        The table below shows the year-over-year change in cultural site visits during the pandemic period.
        """)
        
        st.dataframe(covid_change.style.format({
            'Cultural Site Visits': '{:,.0f}',
            'Year-over-Year Change (%)': '{:.2f}%'
        }))
    
    with tab2:
        st.subheader("Economic Impact of Cultural Tourism")
        
        # Create a scatter plot of visitors vs revenue
        yearly_state_data = tourism_data.groupby(['year', 'state']).agg({
            'cultural_site_visits': 'sum',
            'revenue_millions_inr': 'sum'
        }).reset_index()
        
        # Year selector
        selected_year = st.selectbox(
            "Select Year for Analysis",
            options=sorted(tourism_data['year'].unique(), reverse=True)
        )
        
        year_data = yearly_state_data[yearly_state_data['year'] == selected_year]
        
        # Create bubble chart
        fig = create_bubble_chart(
            year_data,
            'cultural_site_visits',
            'revenue_millions_inr',
            'cultural_site_visits',
            'state',
            title=f"Cultural Site Visits vs. Revenue by State ({selected_year})"
        )
        
        fig.update_layout(
            xaxis_title="Cultural Site Visits",
            yaxis_title="Revenue (Millions INR)",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Total revenue over time
        yearly_revenue = tourism_data.groupby('year')['revenue_millions_inr'].sum().reset_index()
        
        fig2 = create_trend_chart(
            yearly_revenue,
            'year',
            'revenue_millions_inr',
            title="Total Revenue from Cultural Tourism Over Time (Millions INR)"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Revenue per visitor
        yearly_state_data['revenue_per_visitor'] = yearly_state_data['revenue_millions_inr'] * 1000000 / yearly_state_data['cultural_site_visits']
        
        latest_year = yearly_state_data['year'].max()
        latest_data = yearly_state_data[yearly_state_data['year'] == latest_year]
        
        fig3 = create_bar_chart(
            latest_data.sort_values('revenue_per_visitor', ascending=False),
            'state',
            'revenue_per_visitor',
            title=f"Revenue per Visitor by State ({latest_year})"
        )
        
        fig3.update_layout(
            xaxis_title="State",
            yaxis_title="Revenue per Visitor (INR)"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.subheader("Domestic vs International Tourism")
        
        # Ratio of domestic to international tourists over time
        yearly_ratio = tourism_data.groupby('year').agg({
            'domestic_tourists': 'sum',
            'international_tourists': 'sum'
        }).reset_index()
        
        yearly_ratio['domestic_percent'] = yearly_ratio['domestic_tourists'] / (yearly_ratio['domestic_tourists'] + yearly_ratio['international_tourists']) * 100
        yearly_ratio['international_percent'] = yearly_ratio['international_tourists'] / (yearly_ratio['domestic_tourists'] + yearly_ratio['international_tourists']) * 100
        
        # Create a stacked area chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=yearly_ratio['year'],
            y=yearly_ratio['domestic_percent'],
            mode='lines',
            name='Domestic',
            line=dict(width=0.5, color='rgb(73, 160, 181)'),
            stackgroup='one',
            groupnorm='percent'
        ))
        
        fig.add_trace(go.Scatter(
            x=yearly_ratio['year'],
            y=yearly_ratio['international_percent'],
            mode='lines',
            name='International',
            line=dict(width=0.5, color='rgb(235, 77, 75)'),
            stackgroup='one'
        ))
        
        fig.update_layout(
            title="Proportion of Domestic vs International Tourists Over Time",
            xaxis_title="Year",
            yaxis_title="Percentage",
            hovermode="x unified",
            plot_bgcolor="white",
            yaxis=dict(
                type='linear',
                range=[0, 100],
                ticksuffix='%'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # State preferences for domestic vs international tourists
        if st.checkbox("Show State Preferences for Domestic vs International Tourists"):
            # Year selector
            year_for_analysis = st.selectbox(
                "Select Year",
                options=sorted(tourism_data['year'].unique(), reverse=True),
                key="year_for_domestic_intl"
            )
            
            # Filter data for selected year
            year_state_data = tourism_data[tourism_data['year'] == year_for_analysis]
            
            # Calculate ratio of international to domestic tourists
            year_state_data['intl_to_domestic_ratio'] = year_state_data['international_tourists'] / year_state_data['domestic_tourists']
            
            # Sort by ratio
            sorted_data = year_state_data.sort_values('intl_to_domestic_ratio', ascending=False)
            
            # Create a bar chart
            fig2 = px.bar(
                sorted_data,
                x='state',
                y='intl_to_domestic_ratio',
                title=f"Ratio of International to Domestic Tourists by State ({year_for_analysis})",
                color='intl_to_domestic_ratio',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            
            fig2.update_layout(
                xaxis_title="State",
                yaxis_title="International to Domestic Ratio",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            st.write("""
            This chart shows the ratio of international to domestic tourists for each state.
            A higher ratio indicates that the state attracts relatively more international tourists compared to domestic ones.
            """)
    
    with tab4:
        st.subheader("State-wise Tourism Analysis")
        
        # State selector
        selected_states = st.multiselect(
            "Select States for Comparison",
            options=sorted(tourism_data['state'].unique()),
            default=tourism_data['state'].unique()[:3]
        )
        
        if not selected_states:
            st.warning("Please select at least one state for analysis.")
        else:
            # Filter data for selected states
            state_data = tourism_data[tourism_data['state'].isin(selected_states)]
            
            # Create a line chart for cultural site visits by state
            state_yearly = state_data.groupby(['year', 'state'])['cultural_site_visits'].sum().reset_index()
            
            fig = create_trend_chart(
                state_yearly,
                'year',
                'cultural_site_visits',
                'state',
                title="Cultural Site Visits by State Over Time"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth rate analysis
            st.write("### Tourism Growth Rate by State")
            
            # Calculate growth rate between first and last year
            first_year = state_data['year'].min()
            last_year = state_data['year'].max()
            
            first_year_data = state_data[state_data['year'] == first_year].set_index('state')['cultural_site_visits']
            last_year_data = state_data[state_data['year'] == last_year].set_index('state')['cultural_site_visits']
            
            growth_data = pd.DataFrame({
                'First Year Visits': first_year_data,
                'Last Year Visits': last_year_data
            }).reset_index()
            
            growth_data['Growth Rate (%)'] = (growth_data['Last Year Visits'] - growth_data['First Year Visits']) / growth_data['First Year Visits'] * 100
            
            # Sort by growth rate
            growth_data = growth_data.sort_values('Growth Rate (%)', ascending=False)
            
            # Display as a table
            st.dataframe(growth_data.style.format({
                'First Year Visits': '{:,.0f}',
                'Last Year Visits': '{:,.0f}',
                'Growth Rate (%)': '{:.2f}%'
            }))
            
            # Correlation with art forms
            if art_forms_data is not None:
                st.write("### Correlation with Traditional Art Forms")
                
                # Count art forms by state
                art_form_counts = art_forms_data.groupby('state').size().reset_index(name='art_form_count')
                
                # Get latest year tourism data
                latest_tourism = tourism_data[tourism_data['year'] == last_year][['state', 'cultural_site_visits']]
                
                # Merge the datasets
                merged_data = pd.merge(latest_tourism, art_form_counts, on='state', how='inner')
                
                # Create a scatter plot
                fig = px.scatter(
                    merged_data,
                    x='art_form_count',
                    y='cultural_site_visits',
                    hover_name='state',
                    trendline='ols',
                    title=f"Relationship Between Number of Art Forms and Cultural Site Visits ({last_year})"
                )
                
                fig.update_layout(
                    xaxis_title="Number of Traditional Art Forms",
                    yaxis_title="Cultural Site Visits",
                    plot_bgcolor="white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("""
                This chart explores the relationship between the number of traditional art forms in a state
                and the number of cultural site visits. A positive correlation suggests that states with more
                diverse art forms tend to attract more cultural tourists.
                """)
    
    # Download options
    st.subheader("Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = tourism_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Tourism Data as CSV",
            data=csv,
            file_name="india_cultural_tourism_data.csv",
            mime="text/csv"
        )
    
    with col2:
        st.write("""
        This data includes annual tourism statistics for cultural sites across India,
        including domestic and international visitor numbers, cultural site visits, and revenue.
        """)
