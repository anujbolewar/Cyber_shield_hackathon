#!/usr/bin/env python3
"""
🏛️ POLICE-GRADE VISUALIZATIONS SYSTEM
Professional interactive charts for law enforcement cyber monitoring
Created for Indian Police Departments & Cyber Crime Units
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
import random
from typing import Dict, List, Tuple, Optional, Any

class PoliceVisualizationEngine:
    """
    🚨 Professional police-grade visualization engine for cyber monitoring
    Features: Interactive charts, export capabilities, mobile-responsive design
    """
    
    def __init__(self):
        """Initialize police visualization engine with professional styling"""
        
        # Police color scheme
        self.colors = {
            'police_blue': '#1B365D',
            'police_dark_blue': '#0D1B2A',
            'alert_red': '#DC143C',
            'warning_orange': '#FF6B35',
            'safe_green': '#28A745',
            'neutral_gray': '#6C757D',
            'accent_gold': '#FFD700',
            'background_dark': '#2C3E50',
            'text_light': '#FFFFFF',
            'grid_gray': '#34495E'
        }
        
        # Professional layout template
        self.layout_template = {
            'paper_bgcolor': self.colors['background_dark'],
            'plot_bgcolor': self.colors['police_dark_blue'],
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': self.colors['text_light']
            },
            'title': {
                'font': {'size': 18, 'color': self.colors['text_light']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
            'legend': {
                'bgcolor': 'rgba(0,0,0,0.5)',
                'bordercolor': self.colors['police_blue'],
                'borderwidth': 1,
                'font': {'color': self.colors['text_light']}
            }
        }
        
        # Mobile responsive configuration
        self.mobile_config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['downloadPng', 'downloadSvg', 'downloadPdf'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'police_intelligence_chart',
                'height': 800,
                'width': 1200,
                'scale': 2
            },
            'responsive': True
        }
        
        print("🏛️ Police Visualization Engine initialized")
        print("🚨 Professional law enforcement charts ready")
    
    def create_threat_level_gauge(self, current_threat: float, 
                                title: str = "🚨 Real-Time Threat Level") -> go.Figure:
        """
        Create professional threat level gauge for police operations
        
        Args:
            current_threat: Current threat level (0-100)
            title: Chart title
            
        Returns:
            Plotly gauge figure
        """
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_threat,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {
                'text': title,
                'font': {'size': 24, 'color': self.colors['text_light']}
            },
            delta = {
                'reference': 50,
                'increasing': {'color': self.colors['alert_red']},
                'decreasing': {'color': self.colors['safe_green']}
            },
            gauge = {
                'axis': {
                    'range': [None, 100],
                    'tickwidth': 1,
                    'tickcolor': self.colors['text_light']
                },
                'bar': {'color': self.colors['police_blue']},
                'bgcolor': self.colors['background_dark'],
                'borderwidth': 2,
                'bordercolor': self.colors['police_blue'],
                'steps': [
                    {'range': [0, 30], 'color': self.colors['safe_green']},
                    {'range': [30, 70], 'color': self.colors['warning_orange']},
                    {'range': [70, 100], 'color': self.colors['alert_red']}
                ],
                'threshold': {
                    'line': {'color': self.colors['accent_gold'], 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        # Apply police styling
        fig.update_layout(
            **self.layout_template,
            height=400
        )
        
        fig.add_annotation(
            text="🚨 CRITICAL ALERT THRESHOLD: 90+",
            x=0.5, y=0.1,
            showarrow=False,
            font=dict(size=14, color=self.colors['alert_red'])
        )
        
        return fig
    
    def create_geographic_heatmap(self, threat_data: List[Dict], 
                                title: str = "🗺️ Geographic Threat Distribution - India") -> go.Figure:
        """
        Create geographic heatmap of threats across Indian states/cities
        
        Args:
            threat_data: List of threat data with lat, lon, intensity
            title: Chart title
            
        Returns:
            Plotly heatmap figure
        """
        
        # Sample Indian cities data if not provided
        if not threat_data:
            threat_data = self._generate_sample_geo_data()
        
        df = pd.DataFrame(threat_data)
        
        fig = px.density_mapbox(
            df, 
            lat='latitude', 
            lon='longitude', 
            z='threat_intensity',
            radius=15,
            center=dict(lat=20.5937, lon=78.9629),  # Center of India
            zoom=4,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=[
                [0, self.colors['safe_green']],
                [0.5, self.colors['warning_orange']],
                [1, self.colors['alert_red']]
            ],
            title=title,
            hover_data=['city', 'state', 'incident_count', 'threat_type']
        )
        
        # Add city markers
        fig.add_trace(go.Scattermapbox(
            lat=df['latitude'],
            lon=df['longitude'],
            mode='markers',
            marker=dict(
                size=df['threat_intensity'] * 0.5,
                color=df['threat_intensity'],
                colorscale='Reds',
                opacity=0.8,
                sizemode='diameter'
            ),
            text=df['city'],
            hovertemplate=
            "<b>🏙️ %{text}</b><br>" +
            "📍 State: %{customdata[0]}<br>" +
            "🚨 Threat Level: %{customdata[1]}<br>" +
            "📊 Incidents: %{customdata[2]}<br>" +
            "⚠️ Primary Threat: %{customdata[3]}<br>" +
            "<extra></extra>",
            customdata=df[['state', 'threat_intensity', 'incident_count', 'threat_type']],
            name="Cities"
        ))
        
        fig.update_layout(
            **self.layout_template,
            height=600
        )
        
        fig.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(lat=20.5937, lon=78.9629),
                zoom=4
            )
        )
        
        return fig
    
    def create_network_graph(self, network_data: Dict, 
                           title: str = "🕸️ Account Network Connections") -> go.Figure:
        """
        Create network graph showing account connections and relationships
        
        Args:
            network_data: Network data with nodes and edges
            title: Chart title
            
        Returns:
            Plotly network graph figure
        """
        
        # Generate sample network data if not provided
        if not network_data:
            network_data = self._generate_sample_network()
        
        nodes = network_data['nodes']
        edges = network_data['edges']
        
        # Calculate node positions using force-directed layout
        pos = self._calculate_network_positions(nodes, edges)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in edges:
            x0, y0 = pos[edge['source']]
            x1, y1 = pos[edge['target']]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color=self.colors['neutral_gray']),
            hoverinfo='none',
            mode='lines',
            name='Connections'
        )
        
        # Create node traces
        node_x = [pos[node['id']][0] for node in nodes]
        node_y = [pos[node['id']][1] for node in nodes]
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node['label'] for node in nodes],
            textposition="middle center",
            marker=dict(
                showscale=True,
                colorscale='RdYlBu_r',
                reversescale=True,
                color=[node['risk_score'] for node in nodes],
                size=[node['connections'] * 3 + 10 for node in nodes],
                colorbar=dict(
                    thickness=15,
                    len=0.7,
                    x=1.02,
                    title="Risk Score",
                    titlefont=dict(color=self.colors['text_light']),
                    tickcolor=self.colors['text_light']
                ),
                line=dict(width=2, color=self.colors['police_blue'])
            ),
            name='Accounts',
            hovertemplate=
            "<b>👤 %{customdata[0]}</b><br>" +
            "🚨 Risk Score: %{customdata[1]}/100<br>" +
            "🔗 Connections: %{customdata[2]}<br>" +
            "📱 Platform: %{customdata[3]}<br>" +
            "⚠️ Account Type: %{customdata[4]}<br>" +
            "<extra></extra>",
            customdata=[[node['label'], node['risk_score'], node['connections'], 
                        node['platform'], node['account_type']] for node in nodes]
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        
        fig.update_layout(
            **self.layout_template,
            showlegend=True,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )
        
        fig.add_annotation(
            text="🔍 Node size indicates connection count • Color indicates risk level",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002,
            xanchor='left', yanchor='bottom',
            font=dict(color=self.colors['text_light'], size=12)
        )
        
        return fig
    
    def create_timeline_analysis(self, campaign_data: List[Dict], 
                               title: str = "📈 Campaign Timeline Analysis") -> go.Figure:
        """
        Create timeline analysis showing campaign evolution over time
        
        Args:
            campaign_data: Time-series campaign data
            title: Chart title
            
        Returns:
            Plotly timeline figure
        """
        
        # Generate sample timeline data if not provided
        if not campaign_data:
            campaign_data = self._generate_sample_timeline()
        
        df = pd.DataFrame(campaign_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                "🚨 Threat Activity Over Time",
                "📊 Content Volume Analysis", 
                "🤖 Bot Activity Detection"
            ),
            vertical_spacing=0.1,
            shared_xaxes=True
        )
        
        # Threat activity timeline
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['threat_score'],
                mode='lines+markers',
                name='Threat Score',
                line=dict(color=self.colors['alert_red'], width=3),
                marker=dict(size=8),
                fill='tonexty',
                fillcolor='rgba(220, 20, 60, 0.3)',
                hovertemplate="📅 %{x}<br>🚨 Threat: %{y}/100<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Content volume
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['content_volume'],
                name='Content Volume',
                marker_color=self.colors['police_blue'],
                opacity=0.8,
                hovertemplate="📅 %{x}<br>📊 Posts: %{y}<extra></extra>"
            ),
            row=2, col=1
        )
        
        # Bot activity
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['bot_percentage'],
                mode='lines+markers',
                name='Bot Activity %',
                line=dict(color=self.colors['warning_orange'], width=2),
                marker=dict(size=6),
                hovertemplate="📅 %{x}<br>🤖 Bot Activity: %{y}%<extra></extra>"
            ),
            row=3, col=1
        )
        
        # Add critical event annotations
        critical_events = [event for event in campaign_data if event.get('is_critical', False)]
        for event in critical_events:
            fig.add_annotation(
                x=event['timestamp'],
                y=event['threat_score'],
                text="🚨 CRITICAL",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=self.colors['alert_red'],
                bgcolor=self.colors['alert_red'],
                bordercolor=self.colors['text_light'],
                borderwidth=2,
                font=dict(color=self.colors['text_light']),
                row=1, col=1
            )
        
        fig.update_layout(
            **self.layout_template,
            height=800,
            showlegend=True
        )
        
        # Update x-axis labels
        fig.update_xaxes(
            title_text="📅 Timeline",
            gridcolor=self.colors['grid_gray'],
            row=3, col=1
        )
        
        # Update y-axis labels
        fig.update_yaxes(title_text="🚨 Threat Score", gridcolor=self.colors['grid_gray'], row=1, col=1)
        fig.update_yaxes(title_text="📊 Posts Count", gridcolor=self.colors['grid_gray'], row=2, col=1)
        fig.update_yaxes(title_text="🤖 Bot %", gridcolor=self.colors['grid_gray'], row=3, col=1)
        
        return fig
    
    def create_platform_distribution(self, platform_data: Dict, 
                                   title: str = "📱 Platform Distribution Analysis") -> go.Figure:
        """
        Create pie charts showing platform distribution of threats
        
        Args:
            platform_data: Platform usage and threat data
            title: Chart title
            
        Returns:
            Plotly pie chart figure
        """
        
        # Generate sample platform data if not provided
        if not platform_data:
            platform_data = self._generate_sample_platform_data()
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type':'domain'}, {'type':'domain'}]],
            subplot_titles=("📊 Content Volume by Platform", "🚨 Threat Distribution by Platform")
        )
        
        platforms = list(platform_data.keys())
        volumes = [platform_data[p]['volume'] for p in platforms]
        threats = [platform_data[p]['threats'] for p in platforms]
        
        # Content volume pie
        fig.add_trace(
            go.Pie(
                labels=platforms,
                values=volumes,
                name="Content Volume",
                marker_colors=[self.colors['police_blue'], self.colors['safe_green'], 
                             self.colors['warning_orange'], self.colors['neutral_gray']],
                textinfo='label+percent',
                textfont=dict(color=self.colors['text_light']),
                hovertemplate="📱 %{label}<br>📊 Volume: %{value}<br>📈 Percentage: %{percent}<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Threat distribution pie
        fig.add_trace(
            go.Pie(
                labels=platforms,
                values=threats,
                name="Threats",
                marker_colors=[self.colors['alert_red'], self.colors['warning_orange'], 
                             self.colors['police_blue'], self.colors['neutral_gray']],
                textinfo='label+percent',
                textfont=dict(color=self.colors['text_light']),
                hovertemplate="📱 %{label}<br>🚨 Threats: %{value}<br>📈 Percentage: %{percent}<extra></extra>"
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            **self.layout_template,
            height=500
        )
        
        fig.add_annotation(
            text="📊 Total Content", x=0.18, y=0.5, font_size=16, showarrow=False,
            font_color=self.colors['text_light']
        )
        fig.add_annotation(
            text="🚨 High-Risk Threats", x=0.82, y=0.5, font_size=16, showarrow=False,
            font_color=self.colors['text_light']
        )
        
        return fig
    
    def create_engagement_velocity(self, engagement_data: List[Dict], 
                                 title: str = "🚀 Engagement Velocity Analysis") -> go.Figure:
        """
        Create line charts showing engagement velocity over time
        
        Args:
            engagement_data: Time-series engagement data
            title: Chart title
            
        Returns:
            Plotly line chart figure
        """
        
        # Generate sample engagement data if not provided
        if not engagement_data:
            engagement_data = self._generate_sample_engagement()
        
        df = pd.DataFrame(engagement_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig = go.Figure()
        
        # Likes velocity
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['likes_velocity'],
            mode='lines+markers',
            name='👍 Likes/Hour',
            line=dict(color=self.colors['safe_green'], width=3),
            marker=dict(size=6),
            hovertemplate="📅 %{x}<br>👍 Likes: %{y}/hour<extra></extra>"
        ))
        
        # Shares velocity
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['shares_velocity'],
            mode='lines+markers',
            name='🔄 Shares/Hour',
            line=dict(color=self.colors['police_blue'], width=3),
            marker=dict(size=6),
            hovertemplate="📅 %{x}<br>🔄 Shares: %{y}/hour<extra></extra>"
        ))
        
        # Comments velocity
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['comments_velocity'],
            mode='lines+markers',
            name='💬 Comments/Hour',
            line=dict(color=self.colors['warning_orange'], width=3),
            marker=dict(size=6),
            hovertemplate="📅 %{x}<br>💬 Comments: %{y}/hour<extra></extra>"
        ))
        
        # Viral threshold line
        viral_threshold = df['likes_velocity'].mean() * 3
        fig.add_hline(
            y=viral_threshold,
            line_dash="dash",
            line_color=self.colors['alert_red'],
            annotation_text="🚨 VIRAL THRESHOLD",
            annotation_position="top right",
            annotation_font_color=self.colors['alert_red']
        )
        
        fig.update_layout(
            **self.layout_template,
            xaxis_title="📅 Timeline",
            yaxis_title="📊 Engagement Rate (per hour)",
            height=500,
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def create_risk_score_histogram(self, risk_data: List[float], 
                                  title: str = "📊 Risk Score Distribution") -> go.Figure:
        """
        Create histogram showing risk score distribution
        
        Args:
            risk_data: List of risk scores
            title: Chart title
            
        Returns:
            Plotly histogram figure
        """
        
        # Generate sample risk data if not provided
        if not risk_data:
            risk_data = self._generate_sample_risk_scores()
        
        fig = go.Figure()
        
        # Main histogram
        fig.add_trace(go.Histogram(
            x=risk_data,
            nbinsx=20,
            name='Risk Distribution',
            marker_color=self.colors['police_blue'],
            opacity=0.8,
            hovertemplate="📊 Risk Range: %{x}<br>📈 Count: %{y}<extra></extra>"
        ))
        
        # Add risk zone indicators
        fig.add_vrect(
            x0=0, x1=30,
            fillcolor=self.colors['safe_green'],
            opacity=0.2,
            layer="below",
            line_width=0,
            annotation_text="🟢 LOW RISK",
            annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=30, x1=70,
            fillcolor=self.colors['warning_orange'],
            opacity=0.2,
            layer="below",
            line_width=0,
            annotation_text="🟡 MEDIUM RISK",
            annotation_position="top"
        )
        
        fig.add_vrect(
            x0=70, x1=100,
            fillcolor=self.colors['alert_red'],
            opacity=0.2,
            layer="below",
            line_width=0,
            annotation_text="🔴 HIGH RISK",
            annotation_position="top right"
        )
        
        # Statistical lines
        mean_score = np.mean(risk_data)
        fig.add_vline(
            x=mean_score,
            line_dash="dash",
            line_color=self.colors['text_light'],
            annotation_text=f"📊 Mean: {mean_score:.1f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            **self.layout_template,
            xaxis_title="🚨 Risk Score (0-100)",
            yaxis_title="📊 Frequency Count",
            height=500,
            bargap=0.1,
            showlegend=False
        )
        
        return fig
    
    def create_keyword_treemap(self, keyword_data: Dict, 
                             title: str = "🔍 Keyword Frequency Analysis") -> go.Figure:
        """
        Create treemap showing keyword frequency and importance
        
        Args:
            keyword_data: Dictionary of keywords and their metrics
            title: Chart title
            
        Returns:
            Plotly treemap figure
        """
        
        # Generate sample keyword data if not provided
        if not keyword_data:
            keyword_data = self._generate_sample_keywords()
        
        # Prepare data for treemap
        labels = []
        values = []
        parents = []
        colors = []
        hover_data = []
        
        # Add category parents first
        categories = set(keyword_data[k]['category'] for k in keyword_data.keys())
        for category in categories:
            labels.append(category)
            parents.append("")
            category_total = sum(keyword_data[k]['frequency'] for k in keyword_data.keys() 
                               if keyword_data[k]['category'] == category)
            values.append(category_total)
            colors.append(self.colors['police_blue'])
            hover_data.append((0, category))
        
        # Add individual keywords
        for keyword, data in keyword_data.items():
            labels.append(keyword)
            parents.append(data['category'])
            values.append(data['frequency'])
            hover_data.append((data['risk_level'], data['category']))
            
            # Color based on risk level
            if data['risk_level'] >= 80:
                colors.append(self.colors['alert_red'])
            elif data['risk_level'] >= 50:
                colors.append(self.colors['warning_orange'])
            else:
                colors.append(self.colors['safe_green'])
        
        # Create treemap
        fig = go.Figure(go.Treemap(
            labels=labels,
            values=values,
            parents=parents,
            textinfo="label+value",
            textfont_size=11,
            textfont_color='white',
            marker_colors=colors,
            marker_line_color='white',
            marker_line_width=2,
            branchvalues="total",
            maxdepth=2,
            hovertemplate=
            "<b>🔍 %{label}</b><br>" +
            "📊 Frequency: %{value}<br>" +
            "📈 Percentage: %{percentParent}<br>" +
            "🚨 Risk Level: %{customdata[0]}/100<br>" +
            "📂 Category: %{customdata[1]}<br>" +
            "<extra></extra>",
            customdata=hover_data
        ))
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': 'white'}
            },
            paper_bgcolor=self.colors['background_dark'],
            plot_bgcolor=self.colors['police_dark_blue'],
            font=dict(color='white', size=12),
            height=500,
            showlegend=False,
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        return fig
    
    def create_bot_detection_scatter(self, bot_data: List[Dict], 
                                   title: str = "🤖 Bot Detection Analysis") -> go.Figure:
        """
        Create scatter plot for bot detection patterns
        
        Args:
            bot_data: Bot analysis data
            title: Chart title
            
        Returns:
            Plotly scatter plot figure
        """
        
        # Generate sample bot data if not provided
        if not bot_data:
            bot_data = self._generate_sample_bot_data()
        
        df = pd.DataFrame(bot_data)
        
        # Create color mapping for bot probability
        colors = []
        for prob in df['bot_probability']:
            if prob >= 0.8:
                colors.append(self.colors['alert_red'])
            elif prob >= 0.5:
                colors.append(self.colors['warning_orange'])
            else:
                colors.append(self.colors['safe_green'])
        
        fig = go.Figure()
        
        # Main scatter plot
        fig.add_trace(go.Scatter(
            x=df['account_age_days'],
            y=df['posting_frequency'],
            mode='markers',
            marker=dict(
                size=df['account_age_days'] / 10 + 5,  # Scale size appropriately
                color=df['bot_probability'],
                colorscale='RdYlGn_r',
                showscale=True,
                sizemode='diameter',
                sizemin=5,
                line=dict(width=1, color=self.colors['police_blue']),
                colorbar=dict(
                    title="🤖 Bot Probability",
                    titlefont=dict(color=self.colors['text_light']),
                    tickcolor=self.colors['text_light']
                )
            ),
            text=df['username'],
            hovertemplate=
            "<b>👤 @%{text}</b><br>" +
            "📅 Account Age: %{x} days<br>" +
            "📊 Posts/Day: %{y}<br>" +
            "👥 Followers: %{customdata[0]}<br>" +
            "🤖 Bot Probability: %{customdata[1]:.1%}<br>" +
            "🚨 Risk Score: %{customdata[2]}/100<br>" +
            "<extra></extra>",
            customdata=df[['follower_count', 'bot_probability', 'risk_score']],
            name='Accounts'
        ))
        
        # Add bot threshold regions
        fig.add_hline(
            y=df['posting_frequency'].quantile(0.9),
            line_dash="dash",
            line_color=self.colors['alert_red'],
            annotation_text="🚨 Suspicious Activity Threshold",
            annotation_position="top right"
        )
        
        fig.add_vline(
            x=30,
            line_dash="dash",
            line_color=self.colors['warning_orange'],
            annotation_text="⚠️ New Account Alert",
            annotation_position="top"
        )
        
        fig.update_layout(
            **self.layout_template,
            xaxis_title="📅 Account Age (Days)",
            yaxis_title="📊 Daily Posting Frequency",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_comprehensive_dashboard(self, data: Dict) -> Dict[str, go.Figure]:
        """
        Create comprehensive dashboard with all police visualization charts
        
        Args:
            data: Complete dataset for all visualizations
            
        Returns:
            Dictionary of all chart figures
        """
        
        print("🏛️ Creating comprehensive police intelligence dashboard...")
        
        dashboard = {}
        
        # Generate all charts
        dashboard['threat_gauge'] = self.create_threat_level_gauge(
            data.get('current_threat', 75)
        )
        
        dashboard['geo_heatmap'] = self.create_geographic_heatmap(
            data.get('geographic_threats', [])
        )
        
        dashboard['network_graph'] = self.create_network_graph(
            data.get('network_data', {})
        )
        
        dashboard['timeline'] = self.create_timeline_analysis(
            data.get('timeline_data', [])
        )
        
        dashboard['platform_dist'] = self.create_platform_distribution(
            data.get('platform_data', {})
        )
        
        dashboard['engagement'] = self.create_engagement_velocity(
            data.get('engagement_data', [])
        )
        
        dashboard['risk_histogram'] = self.create_risk_score_histogram(
            data.get('risk_scores', [])
        )
        
        dashboard['keyword_treemap'] = self.create_keyword_treemap(
            data.get('keyword_data', {})
        )
        
        dashboard['bot_scatter'] = self.create_bot_detection_scatter(
            data.get('bot_data', [])
        )
        
        print("✅ Police intelligence dashboard created successfully")
        print(f"📊 Generated {len(dashboard)} professional charts")
        
        return dashboard
    
    def export_charts(self, figures: Dict[str, go.Figure], 
                     export_format: str = 'png') -> Dict[str, str]:
        """
        Export all charts in specified format for police reports
        
        Args:
            figures: Dictionary of chart figures
            export_format: Export format (png, svg, pdf, html)
            
        Returns:
            Dictionary of exported file paths
        """
        
        exported_files = {}
        
        for chart_name, fig in figures.items():
            filename = f"police_intelligence_{chart_name}.{export_format}"
            
            if export_format == 'html':
                fig.write_html(filename, config=self.mobile_config)
            elif export_format == 'png':
                fig.write_image(filename, width=1200, height=800, scale=2)
            elif export_format == 'svg':
                fig.write_image(filename, format='svg', width=1200, height=800)
            elif export_format == 'pdf':
                fig.write_image(filename, format='pdf', width=1200, height=800)
            
            exported_files[chart_name] = filename
        
        print(f"📁 Exported {len(exported_files)} charts in {export_format.upper()} format")
        return exported_files
    
    def get_mobile_responsive_config(self) -> Dict:
        """Get mobile-responsive configuration for charts"""
        return self.mobile_config
    
    def get_police_color_scheme(self) -> Dict[str, str]:
        """Get police color scheme for custom styling"""
        return self.colors.copy()
    
    # Helper methods for generating sample data
    def _generate_sample_geo_data(self) -> List[Dict]:
        """Generate sample geographic threat data for Indian cities"""
        
        indian_cities = [
            {"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777},
            {"city": "Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090},
            {"city": "Bangalore", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946},
            {"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
            {"city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639},
            {"city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867},
            {"city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567},
            {"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714},
            {"city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873},
            {"city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462}
        ]
        
        threat_types = ["Terrorism", "Cyber Crime", "Anti-National", "Disinformation", "Drug Trafficking"]
        
        geo_data = []
        for city in indian_cities:
            geo_data.append({
                "city": city["city"],
                "state": city["state"],
                "latitude": city["lat"],
                "longitude": city["lon"],
                "threat_intensity": random.uniform(20, 95),
                "incident_count": random.randint(5, 50),
                "threat_type": random.choice(threat_types)
            })
        
        return geo_data
    
    def _generate_sample_network(self) -> Dict:
        """Generate sample network data for account connections"""
        
        accounts = ["TerrorLeader", "SuspectBot1", "PropagandaAcc", "FakeNews_Hub", 
                   "CyberCriminal", "AntiNational1", "BotNetwork2", "Disinformation"]
        
        nodes = []
        for i, account in enumerate(accounts):
            nodes.append({
                "id": i,
                "label": account,
                "risk_score": random.randint(30, 95),
                "connections": random.randint(5, 25),
                "platform": random.choice(["Twitter", "Facebook", "Instagram", "Telegram"]),
                "account_type": random.choice(["Bot", "Human", "Suspicious", "Coordinated"])
            })
        
        edges = []
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if random.random() < 0.4:  # 40% chance of connection
                    edges.append({"source": i, "target": j})
        
        return {"nodes": nodes, "edges": edges}
    
    def _calculate_network_positions(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Calculate positions for network graph using simple force-directed layout"""
        
        positions = {}
        n = len(nodes)
        
        # Simple circular layout
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / n
            x = np.cos(angle) + random.uniform(-0.3, 0.3)
            y = np.sin(angle) + random.uniform(-0.3, 0.3)
            positions[node['id']] = (x, y)
        
        return positions
    
    def _generate_sample_timeline(self) -> List[Dict]:
        """Generate sample timeline data for campaign analysis"""
        
        timeline_data = []
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            date = start_date + timedelta(days=i)
            timeline_data.append({
                "timestamp": date.isoformat(),
                "threat_score": random.randint(20, 90),
                "content_volume": random.randint(100, 1000),
                "bot_percentage": random.uniform(10, 60),
                "is_critical": random.random() < 0.1  # 10% chance of critical event
            })
        
        return timeline_data
    
    def _generate_sample_platform_data(self) -> Dict:
        """Generate sample platform distribution data"""
        
        return {
            "Twitter": {"volume": 15000, "threats": 450},
            "Facebook": {"volume": 25000, "threats": 320},
            "Instagram": {"volume": 18000, "threats": 280},
            "Telegram": {"volume": 8000, "threats": 520}
        }
    
    def _generate_sample_engagement(self) -> List[Dict]:
        """Generate sample engagement velocity data"""
        
        engagement_data = []
        start_time = datetime.now() - timedelta(hours=24)
        
        for i in range(24):
            time = start_time + timedelta(hours=i)
            engagement_data.append({
                "timestamp": time.isoformat(),
                "likes_velocity": random.randint(50, 500),
                "shares_velocity": random.randint(10, 100),
                "comments_velocity": random.randint(20, 200)
            })
        
        return engagement_data
    
    def _generate_sample_risk_scores(self) -> List[float]:
        """Generate sample risk score distribution"""
        
        # Generate realistic risk score distribution
        scores = []
        
        # Normal distribution with bias towards lower scores
        normal_scores = np.random.normal(35, 20, 500)
        scores.extend([max(0, min(100, score)) for score in normal_scores])
        
        # Add some high-risk outliers
        high_risk = np.random.uniform(80, 100, 50)
        scores.extend(high_risk)
        
        return scores
    
    def _generate_sample_keywords(self) -> Dict:
        """Generate sample keyword frequency data"""
        
        keywords = {
            "terrorism": {"frequency": 1250, "risk_level": 95, "category": "Security Threats"},
            "bomb": {"frequency": 890, "risk_level": 98, "category": "Security Threats"},
            "jihad": {"frequency": 567, "risk_level": 92, "category": "Security Threats"},
            "attack": {"frequency": 1450, "risk_level": 85, "category": "Security Threats"},
            "cyber_fraud": {"frequency": 2340, "risk_level": 78, "category": "Cyber Crime"},
            "phishing": {"frequency": 1890, "risk_level": 75, "category": "Cyber Crime"},
            "bitcoin_scam": {"frequency": 1120, "risk_level": 70, "category": "Cyber Crime"},
            "fake_news": {"frequency": 3450, "risk_level": 65, "category": "Disinformation"},
            "propaganda": {"frequency": 2780, "risk_level": 72, "category": "Disinformation"},
            "anti_national": {"frequency": 890, "risk_level": 88, "category": "Anti-National"},
            "separatist": {"frequency": 456, "risk_level": 90, "category": "Anti-National"},
            "drug_trafficking": {"frequency": 1230, "risk_level": 82, "category": "Organized Crime"}
        }
        
        return keywords
    
    def _generate_sample_bot_data(self) -> List[Dict]:
        """Generate sample bot detection data"""
        
        bot_data = []
        
        for i in range(200):
            bot_data.append({
                "username": f"user_{i:03d}",
                "account_age_days": random.randint(1, 365),
                "posting_frequency": random.uniform(0.5, 50),
                "follower_count": random.randint(10, 10000),
                "bot_probability": random.uniform(0.1, 0.95),
                "risk_score": random.randint(20, 95)
            })
        
        return bot_data


def main():
    """Main function to demonstrate police visualization capabilities"""
    
    print("🏛️ POLICE VISUALIZATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Initialize visualization engine
    viz_engine = PoliceVisualizationEngine()
    
    # Create sample comprehensive data
    sample_data = {
        'current_threat': 78,
        'geographic_threats': [],  # Will use generated data
        'network_data': {},  # Will use generated data
        'timeline_data': [],  # Will use generated data
        'platform_data': {},  # Will use generated data
        'engagement_data': [],  # Will use generated data
        'risk_scores': [],  # Will use generated data
        'keyword_data': {},  # Will use generated data
        'bot_data': []  # Will use generated data
    }
    
    # Create comprehensive dashboard
    dashboard = viz_engine.create_comprehensive_dashboard(sample_data)
    
    print(f"\n✅ Successfully created {len(dashboard)} professional police charts")
    print("\n📊 Available visualizations:")
    for chart_name in dashboard.keys():
        print(f"   • {chart_name}")
    
    # Show color scheme
    colors = viz_engine.get_police_color_scheme()
    print(f"\n🎨 Police Color Scheme:")
    for color_name, color_code in colors.items():
        print(f"   • {color_name}: {color_code}")
    
    print("\n🚀 All charts ready for deployment in police monitoring systems!")
    print("📱 Mobile-responsive design with interactive features enabled")
    print("📁 Export capabilities: PNG, SVG, PDF, HTML formats available")
    
    return dashboard


if __name__ == "__main__":
    dashboard = main()
