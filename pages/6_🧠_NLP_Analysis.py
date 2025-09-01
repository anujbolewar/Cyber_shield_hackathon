import streamlit as st
import json
from datetime import datetime
import traceback

# Import our NLP engine
try:
    from utils.nlp_engine import (
        AdvancedNLPEngine, 
        SentimentResult, 
        ThreatAnalysis, 
        EntityResult,
        BotAnalysis,
        EvidenceSummary
    )
except ImportError as e:
    st.error(f"NLP Engine import error: {str(e)}")
    st.stop()

st.set_page_config(
    page_title="NLP Analysis Engine - Police AI Monitor",
    page_icon="🧠",
    layout="wide"
)

# Enhanced Police Theme CSS for NLP Engine
st.markdown("""
<style>
    /* Police theme variables */
    :root {
        --police-blue: #1e3a8a;
        --police-blue-dark: #1e40af;
        --police-blue-light: #3b82f6;
        --police-accent: #fbbf24;
        --police-red: #dc2626;
        --police-green: #16a34a;
    }
    
    /* NLP Engine Header */
    .nlp-header {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .nlp-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-red) 0%, var(--police-accent) 50%, var(--police-red) 100%);
        animation: scan-line 2s infinite linear;
    }
    
    @keyframes scan-line {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Analysis result cards */
    .analysis-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
    }
    
    .analysis-card.critical {
        border-left: 5px solid var(--police-red);
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    }
    
    .analysis-card.high {
        border-left: 5px solid #dc2626;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    }
    
    .analysis-card.medium {
        border-left: 5px solid var(--police-accent);
    }
    
    .analysis-card.low {
        border-left: 5px solid var(--police-green);
    }
    
    /* Risk score indicators */
    .risk-score {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        font-size: 1.2rem;
        font-weight: bold;
        color: white;
        margin: 1rem;
    }
    
    .risk-critical {
        background: linear-gradient(135deg, var(--police-red) 0%, #dc2626 100%);
        animation: pulse-critical 2s infinite;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, var(--police-accent) 0%, #d97706 100%);
    }
    
    .risk-low {
        background: linear-gradient(135deg, var(--police-green) 0%, #059669 100%);
    }
    
    @keyframes pulse-critical {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Entity display */
    .entity-tag {
        display: inline-block;
        background: var(--police-blue);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .entity-person { background: #059669; }
    .entity-org { background: #dc2626; }
    .entity-location { background: var(--police-accent); color: #1f2937; }
    .entity-other { background: var(--police-blue-light); }
    
    /* Bot analysis indicators */
    .bot-indicator {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid var(--police-red);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .bot-indicator.likely {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-color: var(--police-red);
    }
    
    .bot-indicator.unlikely {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-color: var(--police-green);
    }
    
    /* Evidence summary styling */
    .evidence-summary {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border: 2px solid var(--police-blue);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .evidence-header {
        background: var(--police-blue);
        color: white;
        padding: 1rem;
        margin: -2rem -2rem 1rem -2rem;
        border-radius: 10px 10px 0 0;
        text-align: center;
        font-weight: bold;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state for NLP analysis"""
    if 'nlp_engine' not in st.session_state:
        openai_key = st.session_state.api_keys.get('openai', {}).get('key') if 'api_keys' in st.session_state else None
        st.session_state.nlp_engine = AdvancedNLPEngine(openai_api_key=openai_key)
    
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def main():
    initialize_session_state()
    
    # Security classification banner
    st.markdown("""
    <div style="background: var(--police-red); color: white; text-align: center; padding: 0.5rem; font-weight: bold; font-size: 0.9rem; letter-spacing: 1px;">
        🔒 CLASSIFIED - NLP ANALYSIS ENGINE - AUTHORIZED PERSONNEL ONLY 🔒
    </div>
    """, unsafe_allow_html=True)
    
    # NLP Engine header
    st.markdown("""
    <div class="nlp-header">
        <h1>🧠 ADVANCED NLP ANALYSIS ENGINE</h1>
        <p>AI-powered content analysis for threat detection and intelligence gathering</p>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                🤖 Multi-language Support | 🎯 Threat Detection | 📊 Risk Assessment
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Content Analysis")
        
        # Content input
        analysis_type = st.selectbox(
            "Analysis Type",
            [
                "Comprehensive Analysis",
                "Sentiment Analysis Only", 
                "Threat Detection Only",
                "Entity Extraction Only",
                "Bot Behavior Analysis",
                "Anti-National Content Detection"
            ]
        )
        
        content_input = st.text_area(
            "Content to Analyze",
            height=150,
            placeholder="Enter text content for analysis (supports Hindi and English)...",
            help="Paste social media posts, messages, or any text content for analysis"
        )
        
        # Additional parameters
        with st.expander("⚙️ Advanced Parameters", expanded=False):
            col_meta1, col_meta2 = st.columns(2)
            
            with col_meta1:
                st.subheader("User Metadata")
                username = st.text_input("Username", placeholder="@username")
                account_age = st.number_input("Account Age (days)", min_value=1, value=365)
                followers = st.number_input("Followers", min_value=0, value=100)
                following = st.number_input("Following", min_value=0, value=100)
                posts_per_day = st.number_input("Posts per Day", min_value=0.1, value=5.0)
            
            with col_meta2:
                st.subheader("Additional Posts")
                additional_posts = st.text_area(
                    "Recent Posts (one per line)",
                    height=100,
                    placeholder="Enter recent posts from the same user for bot analysis..."
                )
                
                # OpenAI API toggle
                use_openai = st.checkbox(
                    "Use OpenAI Analysis", 
                    value=bool(st.session_state.nlp_engine.openai_api_key),
                    help="Enable advanced AI analysis using OpenAI API"
                )
    
    with col2:
        st.header("🔧 Analysis Controls")
        
        # Quick analysis buttons
        if st.button("🚀 Analyze Content", type="primary", use_container_width=True):
            if content_input.strip():
                analyze_content(content_input, analysis_type, {
                    'username': username,
                    'account_age_days': account_age,
                    'followers': followers,
                    'following': following,
                    'posts_per_day': posts_per_day
                }, additional_posts, use_openai)
            else:
                st.error("Please enter content to analyze")
        
        if st.button("📋 Generate Report", use_container_width=True):
            if content_input.strip():
                generate_police_report(content_input)
            else:
                st.error("Please enter content to analyze")
        
        if st.button("🔄 Clear Results", use_container_width=True):
            clear_results()
        
        # Analysis history
        st.subheader("📊 Analysis History")
        if st.session_state.analysis_history:
            for i, entry in enumerate(reversed(st.session_state.analysis_history[-5:])):
                with st.expander(f"Analysis {len(st.session_state.analysis_history) - i}", expanded=False):
                    st.write(f"**Time:** {entry['timestamp']}")
                    st.write(f"**Type:** {entry['type']}")
                    st.write(f"**Risk Score:** {entry.get('risk_score', 'N/A')}")
                    st.write(f"**Content:** {entry['content'][:100]}...")
        else:
            st.info("No analysis history yet")
    
    # Display results area
    if 'current_analysis' in st.session_state:
        display_analysis_results(st.session_state.current_analysis)

def analyze_content(content, analysis_type, metadata, additional_posts, use_openai):
    """Perform content analysis based on selected type"""
    try:
        with st.spinner("🔍 Analyzing content..."):
            nlp_engine = st.session_state.nlp_engine
            
            # Prepare user posts list
            user_posts = [content]
            if additional_posts.strip():
                user_posts.extend([post.strip() for post in additional_posts.split('\n') if post.strip()])
            
            # Perform analysis based on type
            if analysis_type == "Comprehensive Analysis":
                results = nlp_engine.comprehensive_analysis(content, metadata, user_posts)
            elif analysis_type == "Sentiment Analysis Only":
                results = {'sentiment': nlp_engine.analyze_content_sentiment(content)}
            elif analysis_type == "Threat Detection Only":
                results = {'threat_analysis': nlp_engine.detect_anti_national_content(content)}
            elif analysis_type == "Entity Extraction Only":
                results = {'entities': nlp_engine.extract_entities(content)}
            elif analysis_type == "Bot Behavior Analysis":
                results = {'bot_analysis': nlp_engine.identify_bot_behavior(metadata, user_posts)}
            elif analysis_type == "Anti-National Content Detection":
                results = {'anti_national': nlp_engine.detect_anti_national_content(content)}
            
            # Add OpenAI analysis if requested
            if use_openai and nlp_engine.openai_api_key:
                with st.spinner("🤖 Running OpenAI analysis..."):
                    openai_result = nlp_engine.analyze_with_openai(content)
                    results['openai_analysis'] = openai_result
            
            # Store results
            st.session_state.current_analysis = {
                'content': content,
                'type': analysis_type,
                'results': results,
                'metadata': metadata,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add to history
            history_entry = {
                'content': content[:200] + "..." if len(content) > 200 else content,
                'type': analysis_type,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'risk_score': results.get('risk_score', 'N/A')
            }
            st.session_state.analysis_history.append(history_entry)
            
            st.success(f"✅ {analysis_type} completed successfully!")
            
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.error(f"Error details: {traceback.format_exc()}")

def display_analysis_results(analysis):
    """Display comprehensive analysis results"""
    st.header("📊 Analysis Results")
    
    results = analysis['results']
    content = analysis['content']
    
    # Overall risk assessment
    if 'risk_score' in results or 'threat_analysis' in results:
        display_risk_assessment(results)
    
    # Create tabs for different result types
    result_tabs = []
    if 'sentiment' in results:
        result_tabs.append("🎭 Sentiment")
    if 'threat_analysis' in results or 'anti_national' in results:
        result_tabs.append("🚨 Threat Analysis")
    if 'entities' in results:
        result_tabs.append("🏷️ Entities")
    if 'bot_analysis' in results:
        result_tabs.append("🤖 Bot Analysis")
    if 'coordination' in results:
        result_tabs.append("🔗 Coordination")
    if 'openai_analysis' in results:
        result_tabs.append("🧠 AI Analysis")
    if 'evidence_summary' in results:
        result_tabs.append("📋 Evidence Report")
    
    if result_tabs:
        tabs = st.tabs(result_tabs)
        
        tab_index = 0
        
        # Sentiment Analysis Tab
        if 'sentiment' in results:
            with tabs[tab_index]:
                display_sentiment_analysis(results['sentiment'])
            tab_index += 1
        
        # Threat Analysis Tab
        if 'threat_analysis' in results or 'anti_national' in results:
            with tabs[tab_index]:
                threat_data = results.get('threat_analysis') or results.get('anti_national')
                display_threat_analysis(threat_data)
            tab_index += 1
        
        # Entities Tab
        if 'entities' in results:
            with tabs[tab_index]:
                display_entity_analysis(results['entities'])
            tab_index += 1
        
        # Bot Analysis Tab
        if 'bot_analysis' in results:
            with tabs[tab_index]:
                display_bot_analysis(results['bot_analysis'])
            tab_index += 1
        
        # Coordination Tab
        if 'coordination' in results:
            with tabs[tab_index]:
                display_coordination_analysis(results['coordination'])
            tab_index += 1
        
        # OpenAI Analysis Tab
        if 'openai_analysis' in results:
            with tabs[tab_index]:
                display_openai_analysis(results['openai_analysis'])
            tab_index += 1
        
        # Evidence Report Tab
        if 'evidence_summary' in results:
            with tabs[tab_index]:
                display_evidence_summary(results['evidence_summary'])

def display_risk_assessment(results):
    """Display overall risk assessment"""
    st.subheader("⚠️ Risk Assessment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Overall risk score
    risk_score = results.get('risk_score', 0)
    threat_analysis = results.get('threat_analysis', {})
    
    with col1:
        if risk_score >= 80:
            risk_class = 'critical'
            risk_level = 'CRITICAL'
        elif risk_score >= 60:
            risk_class = 'high'
            risk_level = 'HIGH'
        elif risk_score >= 40:
            risk_class = 'medium'
            risk_level = 'MEDIUM'
        else:
            risk_class = 'low'
            risk_level = 'LOW'
        
        st.markdown(f"""
        <div class="risk-score risk-{risk_class}">
            {risk_score:.0f}
        </div>
        <div style="text-align: center; font-weight: bold; color: var(--police-blue);">
            Risk Score
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        threat_type = threat_analysis.get('threat_type', 'No Threat Detected')
        st.metric("Threat Type", threat_type)
    
    with col3:
        severity = threat_analysis.get('severity', 'LOW')
        st.metric("Severity Level", severity)
    
    with col4:
        confidence = threat_analysis.get('confidence', 0.0)
        st.metric("Confidence", f"{confidence:.1%}")

def display_sentiment_analysis(sentiment_data):
    """Display sentiment analysis results"""
    st.subheader("🎭 Sentiment Analysis")
    
    if isinstance(sentiment_data, dict):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Overall Sentiment", sentiment_data.get('label', 'Unknown').title())
            st.metric("Confidence", f"{sentiment_data.get('confidence', 0):.1%}")
            st.metric("Language", sentiment_data.get('language', 'Unknown').title())
        
        with col2:
            # Sentiment breakdown
            positive = sentiment_data.get('positive', 0)
            negative = sentiment_data.get('negative', 0)
            neutral = sentiment_data.get('neutral', 0)
            
            st.write("**Sentiment Breakdown:**")
            st.progress(positive, text=f"Positive: {positive:.1%}")
            st.progress(negative, text=f"Negative: {negative:.1%}")
            st.progress(neutral, text=f"Neutral: {neutral:.1%}")
            
            compound = sentiment_data.get('compound', 0)
            st.metric("Compound Score", f"{compound:.3f}")

def display_threat_analysis(threat_data):
    """Display threat analysis results"""
    st.subheader("🚨 Threat Analysis")
    
    if isinstance(threat_data, dict):
        risk_score = threat_data.get('risk_score', 0)
        threat_type = threat_data.get('threat_type', 'Unknown')
        severity = threat_data.get('severity', 'LOW')
        
        # Determine card class based on severity
        if severity == 'CRITICAL':
            card_class = 'critical'
        elif severity == 'HIGH':
            card_class = 'high'
        elif severity == 'MEDIUM':
            card_class = 'medium'
        else:
            card_class = 'low'
        
        st.markdown(f"""
        <div class="analysis-card {card_class}">
            <h4>🎯 Threat Assessment</h4>
            <p><strong>Threat Type:</strong> {threat_type}</p>
            <p><strong>Risk Score:</strong> {risk_score}/100</p>
            <p><strong>Severity:</strong> {severity}</p>
            <p><strong>Confidence:</strong> {threat_data.get('confidence', 0):.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detected keywords
        keywords = threat_data.get('detected_keywords', [])
        if keywords:
            st.write("**🔍 Detected Threat Keywords:**")
            for keyword in keywords:
                st.markdown(f"<span class='entity-tag'>{keyword}</span>", unsafe_allow_html=True)
        
        # Evidence points
        evidence = threat_data.get('evidence_points', [])
        if evidence:
            st.write("**📋 Evidence Points:**")
            for point in evidence:
                st.write(f"• {point}")
        
        # Explanation
        explanation = threat_data.get('explanation', '')
        if explanation:
            st.write("**💡 Analysis Explanation:**")
            st.info(explanation)

def display_entity_analysis(entity_data):
    """Display entity extraction results"""
    st.subheader("🏷️ Named Entity Recognition")
    
    if isinstance(entity_data, dict):
        # Persons
        persons = entity_data.get('persons', [])
        if persons:
            st.write("**👥 Persons:**")
            for person in persons:
                st.markdown(f"<span class='entity-tag entity-person'>{person}</span>", unsafe_allow_html=True)
        
        # Organizations
        orgs = entity_data.get('organizations', [])
        if orgs:
            st.write("**🏢 Organizations:**")
            for org in orgs:
                st.markdown(f"<span class='entity-tag entity-org'>{org}</span>", unsafe_allow_html=True)
        
        # Locations
        locations = entity_data.get('locations', [])
        if locations:
            st.write("**📍 Locations:**")
            for location in locations:
                st.markdown(f"<span class='entity-tag entity-location'>{location}</span>", unsafe_allow_html=True)
        
        # Other entities
        other_entities = entity_data.get('other_entities', {})
        if other_entities:
            st.write("**🔍 Other Entities:**")
            for entity_type, entities in other_entities.items():
                if entities:
                    st.write(f"*{entity_type}:*")
                    for entity in entities:
                        st.markdown(f"<span class='entity-tag entity-other'>{entity}</span>", unsafe_allow_html=True)

def display_bot_analysis(bot_data):
    """Display bot behavior analysis"""
    st.subheader("🤖 Bot Behavior Analysis")
    
    if isinstance(bot_data, dict):
        is_bot = bot_data.get('is_bot_likely', False)
        bot_score = bot_data.get('bot_score', 0)
        confidence = bot_data.get('confidence', 0)
        
        # Bot likelihood indicator
        bot_class = 'likely' if is_bot else 'unlikely'
        bot_status = 'LIKELY BOT' if is_bot else 'LIKELY HUMAN'
        
        st.markdown(f"""
        <div class="bot-indicator {bot_class}">
            <h4>🎯 Bot Assessment: {bot_status}</h4>
            <p><strong>Bot Score:</strong> {bot_score:.1f}/100</p>
            <p><strong>Confidence:</strong> {confidence:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Behavioral indicators
        indicators = bot_data.get('indicators', [])
        if indicators:
            st.write("**⚠️ Bot Indicators:**")
            for indicator in indicators:
                st.write(f"• {indicator}")
        
        # Behavioral patterns
        patterns = bot_data.get('behavioral_patterns', {})
        if patterns:
            st.write("**📊 Behavioral Patterns:**")
            for pattern, value in patterns.items():
                st.metric(pattern.replace('_', ' ').title(), f"{value:.3f}")

def display_coordination_analysis(coord_data):
    """Display coordination analysis results"""
    st.subheader("🔗 Coordination Analysis")
    
    if isinstance(coord_data, dict):
        is_coordinated = coord_data.get('is_coordinated', False)
        similarity_score = coord_data.get('similarity_score', 0)
        confidence = coord_data.get('confidence', 0)
        
        coord_status = 'COORDINATED ACTIVITY DETECTED' if is_coordinated else 'NO COORDINATION DETECTED'
        coord_class = 'critical' if is_coordinated else 'low'
        
        st.markdown(f"""
        <div class="analysis-card {coord_class}">
            <h4>🎯 Coordination Status: {coord_status}</h4>
            <p><strong>Similarity Score:</strong> {similarity_score:.1%}</p>
            <p><strong>Confidence:</strong> {confidence:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Similar patterns
        patterns = coord_data.get('similar_patterns', [])
        if patterns:
            st.write("**🔍 Similar Patterns:**")
            for pattern in patterns:
                st.write(f"• {pattern}")
        
        # Coordination indicators
        indicators = coord_data.get('coordination_indicators', [])
        if indicators:
            st.write("**⚠️ Coordination Indicators:**")
            for indicator in indicators:
                st.write(f"• {indicator}")

def display_openai_analysis(openai_data):
    """Display OpenAI analysis results"""
    st.subheader("🧠 Advanced AI Analysis")
    
    if isinstance(openai_data, dict):
        if openai_data.get('success'):
            analysis = openai_data.get('analysis', '')
            st.markdown("**🤖 AI Analysis Report:**")
            st.write(analysis)
            
            usage = openai_data.get('usage', {})
            if usage:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Prompt Tokens", usage.get('prompt_tokens', 0))
                with col2:
                    st.metric("Completion Tokens", usage.get('completion_tokens', 0))
                with col3:
                    st.metric("Total Tokens", usage.get('total_tokens', 0))
        else:
            error_msg = openai_data.get('error', 'Unknown error')
            st.error(f"❌ OpenAI Analysis Failed: {error_msg}")

def display_evidence_summary(evidence_data):
    """Display evidence summary in police report format"""
    st.subheader("📋 Police Evidence Report")
    
    if isinstance(evidence_data, dict):
        st.markdown(f"""
        <div class="evidence-summary">
            <div class="evidence-header">
                🚓 POLICE CYBER MONITORING UNIT - EVIDENCE SUMMARY
            </div>
            
            <p><strong>Case ID:</strong> {evidence_data.get('case_id', 'N/A')}</p>
            <p><strong>Analysis Date:</strong> {evidence_data.get('timestamp', 'N/A')}</p>
            <p><strong>Threat Level:</strong> {evidence_data.get('threat_level', 'N/A')}</p>
            
            <h4>📋 EXECUTIVE SUMMARY</h4>
            <p>{evidence_data.get('summary', 'No summary available')}</p>
            
            <h4>🔍 DETAILED ANALYSIS</h4>
            <pre>{evidence_data.get('detailed_analysis', 'No detailed analysis available')}</pre>
            
            <h4>📊 EVIDENCE POINTS</h4>
        """, unsafe_allow_html=True)
        
        evidence_points = evidence_data.get('evidence_points', [])
        for i, point in enumerate(evidence_points, 1):
            st.markdown(f"**{i}.** {point}")
        
        st.markdown("""
            <h4>⚡ RECOMMENDED ACTIONS</h4>
        """, unsafe_allow_html=True)
        
        actions = evidence_data.get('recommended_actions', [])
        for i, action in enumerate(actions, 1):
            st.markdown(f"**{i}.** {action}")
        
        legal_implications = evidence_data.get('legal_implications', '')
        if legal_implications:
            st.markdown(f"""
                <h4>⚖️ LEGAL IMPLICATIONS</h4>
                <pre>{legal_implications}</pre>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def generate_police_report(content):
    """Generate a comprehensive police report"""
    try:
        with st.spinner("📋 Generating comprehensive police report..."):
            nlp_engine = st.session_state.nlp_engine
            
            # Run comprehensive analysis
            metadata = {'analysis_type': 'police_report'}
            results = nlp_engine.comprehensive_analysis(content, metadata)
            
            # Generate evidence summary
            evidence_summary = nlp_engine.generate_evidence_summary(content, results)
            
            # Display the report
            st.success("✅ Police report generated successfully!")
            display_evidence_summary(evidence_summary.__dict__)
            
            # Offer download option
            report_json = json.dumps(evidence_summary.__dict__, indent=2, default=str)
            st.download_button(
                label="📥 Download Report (JSON)",
                data=report_json,
                file_name=f"police_report_{evidence_summary.case_id}.json",
                mime="application/json"
            )
            
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")

def clear_results():
    """Clear analysis results"""
    if 'current_analysis' in st.session_state:
        del st.session_state.current_analysis
    st.success("Results cleared!")
    st.rerun()

if __name__ == "__main__":
    main()
