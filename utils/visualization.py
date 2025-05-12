import pandas as pd
import numpy as np
import folium
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import altair as alt
from folium.plugins import MarkerCluster

def create_india_map(data, zoom_start=5):
    """
    Create a folium map of India with markers for art forms.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing art form data with latitude and longitude
        zoom_start (int): Initial zoom level for the map
    
    Returns:
        folium.Map: A folium map object
    """
    # Create a map centered on India
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=zoom_start, tiles="OpenStreetMap")
    
    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(india_map)
    
    # Add markers for each art form
    for idx, row in data.iterrows():
        popup_text = f"""
        <strong>{row['art_form']}</strong><br>
        State: {row['state']}<br>
        Type: {row['type']}<br>
        Description: {row['description']}<br>
        Annual Visitors: {row['visitors_annual']:,}
        """
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['art_form'],
            icon=folium.Icon(icon="palette", prefix="fa", color="red")
        ).add_to(marker_cluster)
    
    return india_map

def create_choropleth_map(data, geojson, column, title, colorscale="YlOrRd"):
    """
    Create a choropleth map of India showing values by state.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing data with a state column
        geojson (dict): GeoJSON data for India's states
        column (str): The column to visualize
        title (str): Title for the map
        colorscale (str): Color scale for the map
    
    Returns:
        folium.Map: A folium map object with choropleth
    """
    # Create a map centered on India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4, tiles="CartoDB positron")
    
    # Add the choropleth layer
    folium.Choropleth(
        geo_data=geojson,
        name='choropleth',
        data=data,
        columns=['state', column],
        key_on='feature.properties.state',
        fill_color=colorscale,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=title
    ).add_to(m)
    
    # Add tooltips
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color': '#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color': '#000000', 
                                    'fillOpacity': 0.5, 
                                    'weight': 0.1}
    
    # Add GeoJson layer with tooltips
    folium.GeoJson(
        geojson,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['state'],
            aliases=['State:'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    ).add_to(m)
    
    return m

def create_trend_chart(data, x_column, y_column, color_column=None, title=None):
    """
    Create a line chart showing trends over time.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing the data
        x_column (str): Column name for x-axis
        y_column (str): Column name for y-axis
        color_column (str): Column name for color differentiation
        title (str): Title for the chart
    
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    if color_column:
        fig = px.line(
            data, 
            x=x_column, 
            y=y_column, 
            color=color_column,
            title=title,
            markers=True
        )
    else:
        fig = px.line(
            data, 
            x=x_column, 
            y=y_column,
            title=title,
            markers=True
        )
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        legend_title=color_column if color_column else "",
        plot_bgcolor="white",
        hovermode="x unified"
    )
    
    return fig

def create_bar_chart(data, x_column, y_column, color_column=None, title=None):
    """
    Create a bar chart for comparing values.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing the data
        x_column (str): Column name for x-axis
        y_column (str): Column name for y-axis
        color_column (str): Column name for color differentiation
        title (str): Title for the chart
    
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    if color_column:
        fig = px.bar(
            data, 
            x=x_column, 
            y=y_column, 
            color=color_column,
            title=title
        )
    else:
        fig = px.bar(
            data, 
            x=x_column, 
            y=y_column,
            title=title
        )
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        legend_title=color_column if color_column else "",
        plot_bgcolor="white"
    )
    
    return fig

def create_scatter_map(data, lat_column, lon_column, hover_name, size_column=None, color_column=None, title=None):
    """
    Create a scatter map using Plotly.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing the data
        lat_column (str): Column name for latitude
        lon_column (str): Column name for longitude
        hover_name (str): Column name for hover text
        size_column (str): Column name for marker size
        color_column (str): Column name for marker color
        title (str): Title for the map
    
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    fig = px.scatter_mapbox(
        data,
        lat=lat_column,
        lon=lon_column,
        hover_name=hover_name,
        size=size_column,
        color=color_column,
        zoom=4,
        mapbox_style="carto-positron",
        title=title
    )
    
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        height=600
    )
    
    return fig

def create_bubble_chart(data, x_column, y_column, size_column, hover_name, color_column=None, title=None):
    """
    Create a bubble chart.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing the data
        x_column (str): Column name for x-axis
        y_column (str): Column name for y-axis
        size_column (str): Column name for bubble size
        hover_name (str): Column name for hover text
        color_column (str): Column name for bubble color
        title (str): Title for the chart
    
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    fig = px.scatter(
        data,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        hover_name=hover_name,
        title=title,
        size_max=60
    )
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        legend_title=color_column if color_column else "",
        plot_bgcolor="white"
    )
    
    return fig

def create_altair_chart(data, x_column, y_column, color_column=None, tooltip=None):
    """
    Create an interactive Altair chart.
    
    Parameters:
        data (pandas.DataFrame): DataFrame containing the data
        x_column (str): Column name for x-axis
        y_column (str): Column name for y-axis
        color_column (str): Column name for color differentiation
        tooltip (list): List of columns to display in tooltip
    
    Returns:
        altair.Chart: An Altair chart object
    """
    if tooltip is None:
        tooltip = [x_column, y_column]
        if color_column:
            tooltip.append(color_column)
    
    if color_column:
        chart = alt.Chart(data).mark_circle(
            opacity=0.8,
            stroke='black',
            strokeWidth=1
        ).encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column),
            color=alt.Color(color_column, title=color_column),
            tooltip=tooltip
        ).interactive()
    else:
        chart = alt.Chart(data).mark_circle(
            opacity=0.8,
            stroke='black',
            strokeWidth=1
        ).encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column),
            tooltip=tooltip
        ).interactive()
    
    return chart
