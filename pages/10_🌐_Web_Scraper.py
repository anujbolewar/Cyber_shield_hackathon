#!/usr/bin/env python3
"""
🌐 WEB SCRAPER - POLICE MONITORING SYSTEM
Advanced web scraping for law enforcement intelligence gathering
Features: News articles, social media, forums, comments analysis
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import sqlite3
from pathlib import Path
import hashlib
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
import validators
import sys
import os

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Page configuration
st.set_page_config(
    page_title="Web Scraper - Police AI Monitor",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for Web Scraper
st.markdown("""
<style>
    /* Police Web Scraper Theme */
    :root {
        --police-blue: #1e3a8a;
        --police-blue-dark: #1e40af;
        --police-blue-light: #3b82f6;
        --police-accent: #fbbf24;
        --police-red: #dc2626;
        --police-green: #16a34a;
        --scraper-purple: #7c3aed;
        --scraper-orange: #ea580c;
    }
    
    /* Web Scraper Header */
    .scraper-header {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--scraper-purple) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .scraper-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-red) 0%, var(--police-accent) 50%, var(--police-green) 100%);
        animation: data-flow 3s infinite linear;
    }
    
    @keyframes data-flow {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Input Cards */
    .scraper-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        color: #000000;
    }
    
    .scraper-card h3, .scraper-card h4, .scraper-card p, .scraper-card span, .scraper-card label {
        color: #000000;
    }
    
    .scraper-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.15);
    }
    
    /* Scrape Type Cards */
    .scrape-type-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid var(--police-blue-light);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #000000;
    }
    
    .scrape-type-card h3, .scrape-type-card h4, .scrape-type-card p, .scrape-type-card span {
        color: #000000;
    }
    
    .scrape-type-card:hover {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-color: var(--police-blue);
        transform: scale(1.02);
    }
    
    .scrape-type-card.selected {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--scraper-purple) 100%);
        color: white;
        border-color: var(--scraper-purple);
    }
    
    /* Progress indicators */
    .scraping-progress {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        border: 1px solid var(--scraper-orange);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #000000;
    }
    
    .scraping-progress h3, .scraping-progress h4, .scraping-progress p, .scraping-progress span {
        color: #000000;
    }
    
    /* Results styling */
    .scrape-result {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid var(--police-green);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #000000;
    }
    
    .scrape-result h3, .scrape-result h4, .scrape-result p, .scrape-result span {
        color: #000000;
    }
    
    /* Data field checkboxes */
    .data-field-option {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 6px;
        color: #000000;
    }
    
    .data-field-option label, .data-field-option span {
        color: #000000;
    }
    
    /* Ensure all inputs and text have black color */
    .stTextInput > div > div > input {
        color: #000000 !important;
    }
    
    .stTextArea > div > div > textarea {
        color: #000000 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #000000 !important;
    }
        border: 1px solid #e2e8f0;
    }
    
    /* URL validation styling */
    .url-valid {
        border-left: 4px solid var(--police-green) !important;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
    }
    
    .url-invalid {
        border-left: 4px solid var(--police-red) !important;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
    }
    
    /* Enhanced buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--scraper-purple) 0%, var(--police-blue) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6d28d9 0%, var(--police-blue-dark) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class ScrapedData:
    """Data structure for scraped content"""
    url: str
    title: str = ""
    content: str = ""
    author: str = ""
    timestamp: str = ""
    links: List[str] = None
    comments: List[str] = None
    metadata: Dict[str, Any] = None
    scraped_at: str = ""
    
    def __post_init__(self):
        if self.links is None:
            self.links = []
        if self.comments is None:
            self.comments = []
        if self.metadata is None:
            self.metadata = {}
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat()

class WebScraper:
    """Advanced web scraping system for police monitoring"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database for storing scraped data"""
        db_path = Path("data/web_scraper.db")
        db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            author TEXT,
            timestamp TEXT,
            links TEXT,
            comments TEXT,
            metadata TEXT,
            scrape_type TEXT,
            scraped_at TEXT,
            content_hash TEXT UNIQUE
        )
        """)
        
        conn.commit()
        conn.close()
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            return validators.url(url)
        except Exception:
            return False
    
    def get_page_content(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """Fetch and parse page content"""
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Handle different content types
            content_type = response.headers.get('content-type', '').lower()
            
            if 'html' in content_type or 'xml' in content_type:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                st.warning(f"Non-HTML content detected: {content_type}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Request error for {url}: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error parsing {url}: {str(e)}")
            return None
    
    def extract_news_article(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> ScrapedData:
        """Extract news article data"""
        data = ScrapedData(url=url)
        
        if "Title" in data_fields:
            # Try multiple selectors for title
            title_selectors = ['h1', 'title', '.headline', '.post-title', '[class*="title"]']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem and title_elem.get_text().strip():
                    data.title = title_elem.get_text().strip()
                    break
        
        if "Content" in data_fields:
            # Try multiple selectors for content
            content_selectors = [
                'article', '.article-content', '.post-content', 
                '.entry-content', '[class*="content"]', 'main p'
            ]
            for selector in content_selectors:
                content_elems = soup.select(selector)
                if content_elems:
                    data.content = '\n'.join([elem.get_text().strip() for elem in content_elems])
                    break
        
        if "Author" in data_fields:
            # Try multiple selectors for author
            author_selectors = ['.author', '.byline', '[class*="author"]', '[rel="author"]']
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem and author_elem.get_text().strip():
                    data.author = author_elem.get_text().strip()
                    break
        
        if "Timestamp" in data_fields:
            # Try multiple selectors for timestamp
            time_selectors = ['time', '.date', '.timestamp', '[datetime]']
            for selector in time_selectors:
                time_elem = soup.select_one(selector)
                if time_elem:
                    data.timestamp = time_elem.get('datetime') or time_elem.get_text().strip()
                    break
        
        if "Links" in data_fields:
            # Extract all links
            links = soup.find_all('a', href=True)
            data.links = [urljoin(url, link['href']) for link in links[:10]]  # Limit to 10 links
        
        if "Comments" in data_fields:
            # Try to find comments section
            comment_selectors = ['.comment', '.comments', '[class*="comment"]']
            for selector in comment_selectors:
                comment_elems = soup.select(selector)
                if comment_elems:
                    data.comments = [elem.get_text().strip() for elem in comment_elems[:5]]  # Limit to 5 comments
                    break
        
        return data
    
    def extract_social_media_post(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> ScrapedData:
        """Extract social media post data"""
        data = ScrapedData(url=url)
        
        # Social media specific selectors
        if "Title" in data_fields:
            title_selectors = [
                '[data-testid="tweetText"]',  # Twitter
                '[class*="post-title"]',      # Facebook/LinkedIn
                '.post-header h3',            # General social
            ]
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem and title_elem.get_text().strip():
                    data.title = title_elem.get_text().strip()
                    break
        
        if "Content" in data_fields:
            content_selectors = [
                '[data-testid="tweetText"]',
                '.post-content',
                '[class*="post-text"]',
                '.userContent'
            ]
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem and content_elem.get_text().strip():
                    data.content = content_elem.get_text().strip()
                    break
        
        if "Author" in data_fields:
            author_selectors = [
                '[data-testid="User-Names"]',
                '.author-name',
                '[class*="username"]',
                '.post-author'
            ]
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem and author_elem.get_text().strip():
                    data.author = author_elem.get_text().strip()
                    break
        
        return data
    
    def extract_forum_discussion(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> ScrapedData:
        """Extract forum discussion data"""
        data = ScrapedData(url=url)
        
        if "Title" in data_fields:
            title_selectors = ['.thread-title', '.topic-title', 'h1', '.post-title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem and title_elem.get_text().strip():
                    data.title = title_elem.get_text().strip()
                    break
        
        if "Content" in data_fields:
            # Get main post content
            content_selectors = ['.post-content', '.message-content', '.thread-content']
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem and content_elem.get_text().strip():
                    data.content = content_elem.get_text().strip()
                    break
        
        if "Comments" in data_fields:
            # Extract forum replies
            reply_selectors = ['.reply', '.post-reply', '.message']
            replies = soup.select(reply_selectors[0])
            if replies:
                data.comments = [reply.get_text().strip() for reply in replies[:10]]
        
        return data
    
    def extract_custom_selectors(self, soup: BeautifulSoup, url: str, custom_selectors: str) -> ScrapedData:
        """Extract data using custom CSS selectors"""
        data = ScrapedData(url=url)
        
        try:
            # Parse custom selectors (one per line)
            selectors = custom_selectors.strip().split('\n')
            for selector_line in selectors:
                if ':' in selector_line:
                    field_name, selector = selector_line.split(':', 1)
                    field_name = field_name.strip()
                    selector = selector.strip()
                    
                    elements = soup.select(selector)
                    if elements:
                        extracted_text = '\n'.join([elem.get_text().strip() for elem in elements])
                        setattr(data, field_name.lower(), extracted_text)
        except Exception as e:
            st.error(f"Error with custom selectors: {str(e)}")
        
        return data
    
    def scrape_website(self, url: str, scrape_type: str, max_pages: int, 
                      data_fields: List[str], custom_selectors: str = "") -> List[ScrapedData]:
        """Main scraping function"""
        results = []
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            for page_num in range(min(max_pages, 50)):  # Safety limit
                current_url = f"{url}?page={page_num + 1}" if page_num > 0 else url
                
                status_text.text(f"Scraping page {page_num + 1} of {max_pages}...")
                progress_bar.progress((page_num + 1) / max_pages)
                
                soup = self.get_page_content(current_url)
                if not soup:
                    st.warning(f"Could not fetch page {page_num + 1}")
                    continue
                
                # Extract data based on scrape type
                try:
                    if custom_selectors:
                        scraped_data = self.extract_custom_selectors(soup, current_url, custom_selectors)
                    elif scrape_type == "News Articles":
                        scraped_data = self.extract_news_article(soup, current_url, data_fields)
                    elif scrape_type == "Social Media Posts":
                        scraped_data = self.extract_social_media_post(soup, current_url, data_fields)
                    elif scrape_type == "Forum Discussions":
                        scraped_data = self.extract_forum_discussion(soup, current_url, data_fields)
                    else:
                        scraped_data = self.extract_news_article(soup, current_url, data_fields)  # Default
                    
                    if scraped_data.title or scraped_data.content:  # Only add if we got some data
                        results.append(scraped_data)
                        self.save_to_database(scraped_data, scrape_type)
                        st.success(f"✅ Extracted data from page {page_num + 1}")
                    else:
                        st.info(f"ℹ️ No relevant data found on page {page_num + 1}")
                
                except Exception as e:
                    st.warning(f"⚠️ Error extracting data from page {page_num + 1}: {str(e)}")
                    continue
                
                # Small delay to be respectful
                time.sleep(1)
                
                # Break if no pagination found (for multi-page scraping)
                if page_num > 0 and not soup.find('a', href=re.compile(r'page|next')):
                    st.info("No more pages found")
                    break
        
        except Exception as e:
            st.error(f"Scraping error: {str(e)}")
        finally:
            progress_bar.empty()
            status_text.empty()
        
        return results
    
    def save_to_database(self, data: ScrapedData, scrape_type: str):
        """Save scraped data to database"""
        try:
            # Create content hash for deduplication
            content_hash = hashlib.md5(f"{data.title}{data.content}".encode()).hexdigest()
            
            db_path = Path("data/web_scraper.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT OR IGNORE INTO scraped_content 
            (url, title, content, author, timestamp, links, comments, metadata, scrape_type, scraped_at, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.url,
                data.title,
                data.content,
                data.author,
                data.timestamp,
                json.dumps(data.links),
                json.dumps(data.comments),
                json.dumps(data.metadata),
                scrape_type,
                data.scraped_at,
                content_hash
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Database error: {str(e)}")

def initialize_session_state():
    """Initialize session state for web scraper"""
    if 'scraper' not in st.session_state:
        st.session_state.scraper = WebScraper()
    if 'scrape_results' not in st.session_state:
        st.session_state.scrape_results = []
    if 'scraping_active' not in st.session_state:
        st.session_state.scraping_active = False

def validate_url_input(url: str) -> tuple[bool, str]:
    """Validate URL input with detailed feedback"""
    if not url:
        return False, "Please enter a URL"
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        if not validators.url(url):
            return False, "Invalid URL format"
    except Exception:
        return False, "Invalid URL format"
    
    # Check for common problematic domains
    try:
        parsed = urlparse(url)
        blocked_domains = ['localhost', '127.0.0.1', '0.0.0.0']
        if parsed.hostname in blocked_domains:
            return False, "Cannot scrape local domains"
    except Exception:
        return False, "Invalid URL format"
    
    return True, url

def display_scrape_results(results: List[ScrapedData]):
    """Display scraped results in a formatted way"""
    if not results:
        st.info("No data scraped yet. Start a scraping job to see results here.")
        return
    
    st.markdown("### 📊 Scraping Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Items", len(results))
    with col2:
        st.metric("Unique URLs", len(set(r.url for r in results)))
    with col3:
        st.metric("With Content", len([r for r in results if r.content]))
    with col4:
        st.metric("With Authors", len([r for r in results if r.author]))
    
    # Results display
    for i, result in enumerate(results):
        with st.expander(f"📄 Item {i+1}: {result.title[:50]}..." if result.title else f"📄 Item {i+1}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if result.title:
                    st.markdown(f"**Title:** {result.title}")
                if result.author:
                    st.markdown(f"**Author:** {result.author}")
                if result.timestamp:
                    st.markdown(f"**Timestamp:** {result.timestamp}")
                if result.content:
                    st.markdown(f"**Content Preview:** {result.content[:200]}...")
            
            with col2:
                st.markdown(f"**URL:** [Link]({result.url})")
                if result.links:
                    st.markdown(f"**Links Found:** {len(result.links)}")
                if result.comments:
                    st.markdown(f"**Comments:** {len(result.comments)}")
                st.markdown(f"**Scraped:** {result.scraped_at[:16]}")

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="scraper-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center;">
            🌐 Web Scraper - Police Intelligence System
        </h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Advanced web scraping for law enforcement monitoring and intelligence gathering
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="scraper-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Scraping Configuration")
        
        # URL Input with validation
        st.markdown("#### 🔗 Target Website")
        url_input = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            help="Enter the URL you want to scrape. Must include http:// or https://",
            key="scraper_url"
        )
        
        # Real-time URL validation
        if url_input:
            is_valid, processed_url = validate_url_input(url_input)
            if is_valid:
                st.success(f"✅ Valid URL: {processed_url}")
                st.session_state.processed_url = processed_url
            else:
                st.error(f"❌ {processed_url}")
        
        # Scraping Type Selection
        st.markdown("#### 📋 Scraping Type")
        scrape_type = st.selectbox(
            "Select content type to scrape",
            ["News Articles", "Social Media Posts", "Forum Discussions", "Comments Section"],
            help="Choose the type of content you want to extract"
        )
        
        # Type-specific information
        type_info = {
            "News Articles": "🗞️ Extracts headlines, articles, authors, and publication dates",
            "Social Media Posts": "📱 Extracts posts, usernames, timestamps, and engagement data",
            "Forum Discussions": "💬 Extracts thread titles, posts, replies, and user information",
            "Comments Section": "💭 Focuses on extracting comment threads and user discussions"
        }
        st.info(type_info[scrape_type])
        
        # Max Pages
        st.markdown("#### 📄 Scraping Scope")
        max_pages = st.number_input(
            "Maximum pages to scrape",
            min_value=1,
            max_value=50,
            value=5,
            help="Number of pages to scrape (limited to 50 for performance)"
        )
        
        # Data Fields Selection
        st.markdown("#### 📊 Data Fields to Extract")
        data_fields = st.multiselect(
            "Select data fields to extract",
            ["Title", "Content", "Author", "Timestamp", "Links", "Comments"],
            default=["Title", "Content", "Author"],
            help="Choose which data fields you want to extract from each page"
        )
        
        # Custom CSS Selectors (Advanced)
        st.markdown("#### ⚙️ Advanced Options")
        with st.expander("🔧 Custom CSS Selectors (Advanced Users)"):
            custom_selectors = st.text_area(
                "Custom CSS Selectors",
                placeholder="title: h1.headline\ncontent: .article-body p\nauthor: .byline",
                help="Enter custom CSS selectors, one per line in format 'field: selector'",
                height=100
            )
            
            st.markdown("""
            **Format:** `field_name: css_selector`
            
            **Examples:**
            - `title: h1.headline`
            - `content: .article-body p`
            - `author: .author-name`
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="scraper-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Scraping Control")
        
        # Start Scraping Button
        if not st.session_state.scraping_active:
            if st.button("🕷️ Start Scraping", type="primary", use_container_width=True):
                if not url_input:
                    st.error("Please enter a URL first")
                elif not data_fields and not custom_selectors:
                    st.error("Please select at least one data field or provide custom selectors")
                else:
                    is_valid, processed_url = validate_url_input(url_input)
                    if is_valid:
                        st.session_state.scraping_active = True
                        
                        with st.spinner("🔄 Scraping in progress..."):
                            results = st.session_state.scraper.scrape_website(
                                processed_url, scrape_type, max_pages, data_fields, custom_selectors
                            )
                            st.session_state.scrape_results = results
                        
                        st.session_state.scraping_active = False
                        
                        if results:
                            st.success(f"✅ Successfully scraped {len(results)} items!")
                            st.balloons()
                        else:
                            st.warning("⚠️ No data could be extracted from the target URL")
                    else:
                        st.error(f"❌ {processed_url}")
        else:
            st.warning("🔄 Scraping in progress...")
            if st.button("🛑 Stop Scraping", type="secondary"):
                st.session_state.scraping_active = False
                st.rerun()
        
        # Quick Actions
        st.markdown("#### ⚡ Quick Actions")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 View Results", use_container_width=True):
                if st.session_state.scrape_results:
                    st.info(f"Found {len(st.session_state.scrape_results)} scraped items")
                else:
                    st.info("No results available yet")
        
        with col_b:
            if st.button("🗑️ Clear Results", use_container_width=True):
                st.session_state.scrape_results = []
                st.success("Results cleared!")
                st.rerun()
        
        # Export Options
        if st.session_state.scrape_results:
            st.markdown("#### 📤 Export Data")
            
            # Convert to DataFrame for export
            export_data = []
            for result in st.session_state.scrape_results:
                export_data.append({
                    'URL': result.url,
                    'Title': result.title,
                    'Content': result.content[:500] + '...' if len(result.content) > 500 else result.content,
                    'Author': result.author,
                    'Timestamp': result.timestamp,
                    'Links_Count': len(result.links),
                    'Comments_Count': len(result.comments),
                    'Scraped_At': result.scraped_at
                })
            
            df = pd.DataFrame(export_data)
            
            # Download as CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="💾 Download as CSV",
                data=csv_data,
                file_name=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Download as JSON
            json_data = json.dumps([result.__dict__ for result in st.session_state.scrape_results], indent=2)
            st.download_button(
                label="💾 Download as JSON",
                data=json_data,
                file_name=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Results Section
    st.markdown("---")
    display_scrape_results(st.session_state.scrape_results)
    
    # Recent Scraping History
    st.markdown("### 📚 Recent Scraping History")
    
    try:
        db_path = Path("data/web_scraper.db")
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            
            # Get recent scraping sessions
            recent_data = pd.read_sql_query("""
            SELECT scrape_type, COUNT(*) as count, MAX(scraped_at) as last_scraped
            FROM scraped_content 
            WHERE scraped_at > datetime('now', '-7 days')
            GROUP BY scrape_type
            ORDER BY last_scraped DESC
            """, conn)
            
            if not recent_data.empty:
                st.dataframe(recent_data, use_container_width=True)
            else:
                st.info("No recent scraping history found")
            
            conn.close()
    except Exception as e:
        st.info("No scraping history available yet")

if __name__ == "__main__":
    main()
