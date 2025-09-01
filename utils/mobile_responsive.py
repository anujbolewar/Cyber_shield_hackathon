"""
Mobile Responsive Utilities for Police AI Monitor
Provides responsive design helpers and mobile-optimized components
"""

import streamlit as st

def inject_mobile_css():
    """Inject mobile-responsive CSS"""
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    @media (max-width: 1200px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        /* Stack columns on tablets */
        .element-container .row-widget .stHorizontalBlock {
            flex-direction: column;
        }
        
        .element-container .row-widget .stHorizontalBlock > div {
            width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Adjust font sizes */
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.3rem !important; }
        
        /* Adjust metric cards */
        .metric-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Sidebar adjustments */
        .css-1d391kg {
            width: 100% !important;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        /* Further font size adjustments */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        
        /* Button adjustments */
        .stButton > button {
            width: 100%;
            padding: 0.5rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Select box adjustments */
        .stSelectbox > div > div {
            font-size: 0.9rem;
        }
        
        /* Metric adjustments */
        .css-1xarl3l {
            font-size: 1.2rem !important;
        }
        
        .css-1wivap2 {
            font-size: 0.8rem !important;
        }
    }
    
    /* Touch-friendly button sizing */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 44px;
            padding: 0.75rem 1rem;
        }
        
        .stSelectbox > div > div {
            min-height: 44px;
        }
        
        .stTextInput > div > div > input {
            min-height: 44px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_device_type():
    """Detect device type based on viewport width"""
    # This is a simplified detection - in a real app you'd use JavaScript
    # For now, we'll use Streamlit's column system to detect layout
    return "mobile"  # Placeholder

def mobile_metric_card(label, value, delta=None, help_text=None):
    """Create a mobile-optimized metric card"""
    delta_html = ""
    if delta:
        delta_color = "green" if str(delta).startswith('+') else "red" if str(delta).startswith('-') else "gray"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.8rem; margin-top: 0.25rem;">{delta}</div>'
    
    help_html = ""
    if help_text:
        help_html = f'<div style="font-size: 0.7rem; color: #666; margin-top: 0.25rem;">{help_text}</div>'
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, white 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1e3a8a;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">{label}</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #1e3a8a; margin: 0.25rem 0;">{value}</div>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)

def mobile_alert_card(title, message, severity="info"):
    """Create a mobile-optimized alert card"""
    colors = {
        "critical": {"bg": "#fee2e2", "border": "#dc2626", "icon": "🚨"},
        "high": {"bg": "#fef3c7", "border": "#f59e0b", "icon": "⚠️"},
        "medium": {"bg": "#dbeafe", "border": "#3b82f6", "icon": "ℹ️"},
        "info": {"bg": "#f0f9ff", "border": "#0ea5e9", "icon": "📋"},
        "success": {"bg": "#dcfce7", "border": "#16a34a", "icon": "✅"}
    }
    
    color_scheme = colors.get(severity, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: {color_scheme['bg']};
        border: 2px solid {color_scheme['border']};
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">{color_scheme['icon']}</span>
            <strong style="color: {color_scheme['border']}; font-size: 1rem;">{title}</strong>
        </div>
        <div style="color: #374151; line-height: 1.5;">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def mobile_status_indicator(status, label):
    """Create a mobile-optimized status indicator"""
    status_colors = {
        "operational": {"color": "#16a34a", "icon": "🟢"},
        "warning": {"color": "#f59e0b", "icon": "🟡"},
        "critical": {"color": "#dc2626", "icon": "🔴"},
        "unknown": {"color": "#64748b", "icon": "⚪"}
    }
    
    status_info = status_colors.get(status.lower(), status_colors["unknown"])
    
    st.markdown(f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.9);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        color: {status_info['color']};
        margin: 0.25rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <span>{status_info['icon']}</span>
        <span>{label}: {status.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

def mobile_progress_bar(value, max_value=100, label="", color="#1e3a8a"):
    """Create a mobile-optimized progress bar"""
    percentage = (value / max_value) * 100
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-size: 0.9rem; color: #64748b;">{label}</span>
            <span style="font-size: 0.9rem; font-weight: bold; color: {color};">{value}/{max_value}</span>
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color} 0%, {color}aa 100%);
                border-radius: 4px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mobile_navigation_menu(items):
    """Create a mobile-optimized navigation menu"""
    st.markdown("""
    <div style="
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
    ">
    """, unsafe_allow_html=True)
    
    for item in items:
        st.markdown(f"""
        <div style="
            flex: 1;
            min-width: 120px;
            padding: 0.75rem;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            text-align: center;
            color: white;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        ">
            {item}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def check_mobile_browser():
    """Check if user is on mobile browser (simplified)"""
    # In a real implementation, you'd use JavaScript to detect this
    # For now, we'll assume mobile if screen width is detected as small
    return False  # Placeholder

def mobile_optimized_layout(content_func, sidebar_func=None):
    """Create a mobile-optimized layout"""
    inject_mobile_css()
    
    # On mobile, stack content vertically
    if check_mobile_browser():
        if sidebar_func:
            with st.expander("🔧 Controls", expanded=False):
                sidebar_func()
        content_func()
    else:
        # Desktop layout
        if sidebar_func:
            with st.sidebar:
                sidebar_func()
        content_func()
