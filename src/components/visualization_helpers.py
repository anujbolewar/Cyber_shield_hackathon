"""
Visualization helper functions for social media monitoring
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_custom_chart(chart_type: str, data: dict, **kwargs):
    """Create custom charts based on type and data"""
    
    if chart_type == 'gauge':
        return create_gauge_chart(data, **kwargs)
    elif chart_type == 'waterfall':
        return create_waterfall_chart(data, **kwargs)
    elif chart_type == 'radar':
        return create_radar_chart(data, **kwargs)
    elif chart_type == 'sankey':
        return create_sankey_chart(data, **kwargs)
    elif chart_type == 'bubble':
        return create_bubble_chart(data, **kwargs)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

def create_gauge_chart(data: dict, title: str = "Gauge Chart", **kwargs):
    """Create a gauge chart for KPI visualization"""
    
    value = data.get('value', 50)
    min_value = data.get('min', 0)
    max_value = data.get('max', 100)
    threshold_good = data.get('threshold_good', max_value * 0.8)
    threshold_warning = data.get('threshold_warning', max_value * 0.6)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': data.get('reference', value * 0.9)},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_value, threshold_warning], 'color': "lightgray"},
                {'range': [threshold_warning, threshold_good], 'color': "yellow"},
                {'range': [threshold_good, max_value], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_good
            }
        }
    ))
    
    fig.update_layout(height=400, **kwargs)
    return fig

def create_waterfall_chart(data: dict, title: str = "Waterfall Chart", **kwargs):
    """Create a waterfall chart for showing cumulative effects"""
    
    categories = data.get('categories', ['Start', 'Change 1', 'Change 2', 'End'])
    values = data.get('values', [100, 20, -30, 90])
    
    # Calculate cumulative values for positioning
    cumulative = [0]
    for i, val in enumerate(values):
        if i == 0:  # Starting value
            cumulative.append(val)
        elif i == len(values) - 1:  # Ending value (total)
            cumulative.append(val)
        else:  # Intermediate changes
            cumulative.append(cumulative[-1] + val)
    
    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=["absolute"] + ["relative"] * (len(values) - 2) + ["total"],
        x=categories,
        textposition="outside",
        text=[f"{v:+}" if v != values[0] and v != values[-1] else f"{v}" for v in values],
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title=title,
        showlegend=False,
        height=400,
        **kwargs
    )
    
    return fig

def create_radar_chart(data: dict, title: str = "Radar Chart", **kwargs):
    """Create a radar chart for multi-dimensional data"""
    
    categories = data.get('categories', ['A', 'B', 'C', 'D', 'E'])
    series = data.get('series', {})
    
    fig = go.Figure()
    
    for name, values in series.items():
        # Ensure the radar chart is closed by adding the first value at the end
        radar_values = values + [values[0]]
        radar_categories = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill='toself',
            name=name
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([max(vals) for vals in series.values()]) if series else 1]
            )),
        showlegend=True,
        title=title,
        height=400,
        **kwargs
    )
    
    return fig

def create_sankey_chart(data: dict, title: str = "Sankey Diagram", **kwargs):
    """Create a Sankey diagram for flow visualization"""
    
    source = data.get('source', [0, 1, 0, 2, 3, 3])
    target = data.get('target', [2, 3, 3, 4, 4, 5])
    value = data.get('value', [8, 4, 2, 8, 4, 2])
    labels = data.get('labels', ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue"
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])
    
    fig.update_layout(
        title_text=title,
        font_size=10,
        height=400,
        **kwargs
    )
    
    return fig

def create_bubble_chart(data: dict, title: str = "Bubble Chart", **kwargs):
    """Create a bubble chart for three-dimensional data"""
    
    x = data.get('x', [1, 2, 3, 4, 5])
    y = data.get('y', [1, 4, 2, 3, 5])
    size = data.get('size', [10, 20, 30, 40, 50])
    color = data.get('color', x)
    text = data.get('text', [f"Point {i+1}" for i in range(len(x))])
    
    fig = px.scatter(
        x=x, y=y, size=size, color=color, hover_name=text,
        size_max=60, title=title
    )
    
    fig.update_layout(height=400, **kwargs)
    return fig

def create_multi_axis_chart(data: dict, title: str = "Multi-Axis Chart", **kwargs):
    """Create a chart with multiple y-axes"""
    
    x_data = data.get('x', list(range(10)))
    y1_data = data.get('y1', np.random.randint(10, 100, 10))
    y2_data = data.get('y2', np.random.uniform(0, 1, 10))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=x_data, y=y1_data, name="Primary Metric"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=x_data, y=y2_data, name="Secondary Metric"),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Primary Metric", secondary_y=False)
    fig.update_yaxes(title_text="Secondary Metric", secondary_y=True)
    
    fig.update_layout(
        title_text=title,
        height=400,
        **kwargs
    )
    
    return fig

def create_heatmap_calendar(data: dict, title: str = "Calendar Heatmap", **kwargs):
    """Create a calendar heatmap for activity visualization"""
    
    dates = data.get('dates', pd.date_range('2024-01-01', periods=365, freq='D'))
    values = data.get('values', np.random.randint(0, 100, 365))
    
    # Create a DataFrame
    df = pd.DataFrame({'date': dates, 'value': values})
    df['day_of_week'] = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week
    
    # Pivot for heatmap
    heatmap_data = df.pivot(index='day_of_week', columns='week_of_year', values='value')
    
    fig = px.imshow(
        heatmap_data,
        title=title,
        color_continuous_scale='Blues',
        aspect='auto'
    )
    
    fig.update_layout(height=400, **kwargs)
    return fig

def create_animated_chart(data: dict, title: str = "Animated Chart", **kwargs):
    """Create an animated chart for time series data"""
    
    # Sample data structure: {'dates': [...], 'categories': [...], 'values': [...]}
    df = pd.DataFrame(data)
    
    if 'date' in df.columns and 'category' in df.columns and 'value' in df.columns:
        fig = px.bar(
            df, x='category', y='value',
            animation_frame='date',
            title=title,
            range_y=[0, df['value'].max() * 1.1]
        )
    else:
        # Fallback to static chart
        fig = px.bar(title=title)
    
    fig.update_layout(height=400, **kwargs)
    return fig

def create_3d_scatter(data: dict, title: str = "3D Scatter Plot", **kwargs):
    """Create a 3D scatter plot"""
    
    x = data.get('x', np.random.randn(100))
    y = data.get('y', np.random.randn(100))
    z = data.get('z', np.random.randn(100))
    color = data.get('color', x)
    
    fig = px.scatter_3d(
        x=x, y=y, z=z, color=color,
        title=title
    )
    
    fig.update_layout(height=500, **kwargs)
    return fig

def create_sunburst_chart(data: dict, title: str = "Sunburst Chart", **kwargs):
    """Create a sunburst chart for hierarchical data"""
    
    ids = data.get('ids', ['Root', 'A', 'B', 'C', 'A1', 'A2', 'B1', 'B2'])
    labels = data.get('labels', ['Root', 'Category A', 'Category B', 'Category C', 'A1', 'A2', 'B1', 'B2'])
    parents = data.get('parents', ['', 'Root', 'Root', 'Root', 'A', 'A', 'B', 'B'])
    values = data.get('values', [0, 10, 15, 8, 5, 5, 7, 8])
    
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        **kwargs
    )
    
    return fig

def create_treemap_chart(data: dict, title: str = "Treemap Chart", **kwargs):
    """Create a treemap chart for hierarchical data"""
    
    labels = data.get('labels', ['A', 'B', 'C', 'D'])
    parents = data.get('parents', ['', '', '', ''])
    values = data.get('values', [10, 20, 30, 40])
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        **kwargs
    )
    
    return fig

def apply_custom_theme(fig, theme: str = "default"):
    """Apply custom themes to charts"""
    
    themes = {
        "dark": {
            "paper_bgcolor": "#2F2F2F",
            "plot_bgcolor": "#2F2F2F",
            "font": {"color": "white"},
            "colorway": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
        },
        "minimal": {
            "paper_bgcolor": "white",
            "plot_bgcolor": "white",
            "font": {"color": "#444"},
            "colorway": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
        },
        "corporate": {
            "paper_bgcolor": "#F8F9FA",
            "plot_bgcolor": "#F8F9FA",
            "font": {"color": "#495057", "family": "Arial"},
            "colorway": ["#0066CC", "#FF6B35", "#4ECDC4", "#45B7D1", "#96CEB4"]
        }
    }
    
    if theme in themes:
        fig.update_layout(**themes[theme])
    
    return fig

def add_annotations(fig, annotations: list):
    """Add annotations to a chart"""
    
    for annotation in annotations:
        fig.add_annotation(
            x=annotation.get('x', 0),
            y=annotation.get('y', 0),
            text=annotation.get('text', ''),
            showarrow=annotation.get('showarrow', True),
            arrowhead=annotation.get('arrowhead', 2),
            arrowsize=annotation.get('arrowsize', 1),
            arrowwidth=annotation.get('arrowwidth', 2),
            arrowcolor=annotation.get('arrowcolor', '#636363')
        )
    
    return fig

def create_comparison_chart(data: dict, chart_type: str = "bar", title: str = "Comparison Chart", **kwargs):
    """Create comparison charts for multiple series"""
    
    categories = data.get('categories', ['A', 'B', 'C', 'D'])
    series = data.get('series', {})
    
    if chart_type == "bar":
        fig = go.Figure()
        for name, values in series.items():
            fig.add_trace(go.Bar(name=name, x=categories, y=values))
        fig.update_layout(barmode='group')
    
    elif chart_type == "line":
        fig = go.Figure()
        for name, values in series.items():
            fig.add_trace(go.Scatter(name=name, x=categories, y=values, mode='lines+markers'))
    
    elif chart_type == "area":
        fig = go.Figure()
        for name, values in series.items():
            fig.add_trace(go.Scatter(name=name, x=categories, y=values, mode='lines', fill='tonexty'))
    
    else:
        fig = go.Figure()
    
    fig.update_layout(title=title, height=400, **kwargs)
    return fig

def export_chart(fig, filename: str, format: str = "png", **kwargs):
    """Export chart to various formats"""
    
    if format.lower() == "png":
        fig.write_image(f"{filename}.png", **kwargs)
    elif format.lower() == "pdf":
        fig.write_image(f"{filename}.pdf", **kwargs)
    elif format.lower() == "svg":
        fig.write_image(f"{filename}.svg", **kwargs)
    elif format.lower() == "html":
        fig.write_html(f"{filename}.html", **kwargs)
    else:
        raise ValueError(f"Unsupported format: {format}")

def create_dashboard_layout(charts: dict, title: str = "Dashboard", **kwargs):
    """Create a dashboard layout with multiple charts"""
    
    # This would create a subplot layout with multiple charts
    # For now, return a simple combined figure
    
    num_charts = len(charts)
    if num_charts == 0:
        return go.Figure()
    
    rows = (num_charts + 1) // 2  # 2 charts per row
    cols = 2
    
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=list(charts.keys())
    )
    
    # This is a simplified version - in practice, you'd need to handle different chart types
    for i, (chart_name, chart_data) in enumerate(charts.items()):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        # Add a simple trace (would need to be more sophisticated for different chart types)
        fig.add_trace(
            go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name=chart_name),
            row=row, col=col
        )
    
    fig.update_layout(
        title_text=title,
        height=300 * rows,
        **kwargs
    )
    
    return fig
