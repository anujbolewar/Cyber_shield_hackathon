#!/usr/bin/env python3
"""
Web Scraping Engine for Police Monitoring System
Advanced scraping capabilities with anti-detection and rate limiting
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse, quote
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from datetime import datetime, timedelta
import hashlib
from dataclasses import dataclass, field
import logging
from pathlib import Path
import sqlite3
import threading
from queue import Queue
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuration for web scraping operations"""
    max_pages: int = 5
    delay_range: Tuple[float, float] = (1.0, 3.0)
    timeout: int = 10
    retries: int = 3
    user_agents: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ])
    headers: Dict[str, str] = field(default_factory=lambda: {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })

@dataclass
class ContentExtractor:
    """Content extraction patterns for different website types"""
    
    # News Article Selectors
    NEWS_SELECTORS = {
        'title': [
            'h1', 'title', '.headline', '.post-title', '.article-title',
            '[class*="title"]', '[class*="headline"]', '.entry-title'
        ],
        'content': [
            'article', '.article-content', '.post-content', '.entry-content',
            '[class*="content"]', 'main p', '.story-body', '.article-body'
        ],
        'author': [
            '.author', '.byline', '[class*="author"]', '[rel="author"]',
            '.writer', '.journalist', '.reporter'
        ],
        'timestamp': [
            'time', '.date', '.timestamp', '[datetime]', '.published',
            '.post-date', '.article-date'
        ]
    }
    
    # Social Media Selectors
    SOCIAL_SELECTORS = {
        'title': [
            '[data-testid="tweetText"]',  # Twitter
            '[class*="post-title"]',      # Facebook/LinkedIn
            '.post-header h3',            # General social
            '.status-content'             # Various platforms
        ],
        'content': [
            '[data-testid="tweetText"]',
            '.post-content',
            '[class*="post-text"]',
            '.userContent',
            '.status-text'
        ],
        'author': [
            '[data-testid="User-Names"]',
            '.author-name',
            '[class*="username"]',
            '.post-author',
            '.user-name'
        ]
    }
    
    # Forum Selectors
    FORUM_SELECTORS = {
        'title': [
            '.thread-title', '.topic-title', 'h1', '.post-title',
            '.discussion-title', '.forum-title'
        ],
        'content': [
            '.post-content', '.message-content', '.thread-content',
            '.discussion-content', '.forum-post'
        ],
        'comments': [
            '.reply', '.post-reply', '.message', '.comment',
            '.discussion-reply', '.forum-reply'
        ]
    }
    
    # Comment Section Selectors
    COMMENT_SELECTORS = {
        'comments': [
            '.comment', '.comments', '[class*="comment"]',
            '.discussion', '.replies', '.user-comment'
        ],
        'comment_author': [
            '.comment-author', '.commenter', '.comment-user',
            '[class*="comment-author"]'
        ],
        'comment_content': [
            '.comment-content', '.comment-text', '.comment-body',
            '[class*="comment-content"]'
        ]
    }

class WebScrapingEngine:
    """Advanced web scraping engine with anti-detection capabilities"""
    
    def __init__(self, config: ScrapingConfig = None):
        self.config = config or ScrapingConfig()
        self.session = requests.Session()
        self.extractor = ContentExtractor()
        self.setup_session()
        self.setup_database()
        
    def setup_session(self):
        """Configure session with rotating headers and user agents"""
        self.session.headers.update(self.config.headers)
        self.rotate_user_agent()
        
    def rotate_user_agent(self):
        """Rotate user agent to avoid detection"""
        user_agent = random.choice(self.config.user_agents)
        self.session.headers['User-Agent'] = user_agent
        
    def setup_database(self):
        """Setup SQLite database for caching and storing results"""
        db_path = Path("data/web_scraper_cache.db")
        db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scrape_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            content TEXT,
            scraped_at TEXT,
            expires_at TEXT,
            success BOOLEAN
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraping_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            scrape_type TEXT,
            success_rate REAL,
            avg_response_time REAL,
            last_updated TEXT
        )
        """)
        
        conn.commit()
        conn.close()
        
    def get_cached_content(self, url: str) -> Optional[str]:
        """Get cached content if available and not expired"""
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()
            db_path = Path("data/web_scraper_cache.db")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT content FROM scrape_cache 
            WHERE url_hash = ? AND expires_at > datetime('now') AND success = 1
            """, (url_hash,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")
            return None
            
    def cache_content(self, url: str, content: str, success: bool = True):
        """Cache scraped content"""
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()
            scraped_at = datetime.now().isoformat()
            expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
            
            db_path = Path("data/web_scraper_cache.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT OR REPLACE INTO scrape_cache 
            (url_hash, url, content, scraped_at, expires_at, success)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (url_hash, url, content, scraped_at, expires_at, success))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Cache storage error: {e}")
            
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with anti-detection measures"""
        # Check cache first
        cached_content = self.get_cached_content(url)
        if cached_content:
            return BeautifulSoup(cached_content, 'html.parser')
            
        # Rotate user agent
        self.rotate_user_agent()
        
        # Add random delay
        delay = random.uniform(*self.config.delay_range)
        time.sleep(delay)
        
        for attempt in range(self.config.retries):
            try:
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                # Cache the content
                self.cache_content(url, response.text, True)
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.config.retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.cache_content(url, "", False)
                    
        return None
        
    def extract_by_selectors(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text using a list of CSS selectors"""
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    text = ' '.join([elem.get_text().strip() for elem in elements])
                    if text:
                        return text
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
        return ""
        
    def extract_links(self, soup: BeautifulSoup, base_url: str, limit: int = 20) -> List[str]:
        """Extract links from the page"""
        links = []
        for link in soup.find_all('a', href=True)[:limit]:
            href = link['href']
            if href.startswith(('http://', 'https://')):
                links.append(href)
            elif href.startswith('/'):
                links.append(urljoin(base_url, href))
        return links
        
    def extract_images(self, soup: BeautifulSoup, base_url: str, limit: int = 10) -> List[str]:
        """Extract image URLs from the page"""
        images = []
        for img in soup.find_all('img', src=True)[:limit]:
            src = img['src']
            if src.startswith(('http://', 'https://')):
                images.append(src)
            elif src.startswith('/'):
                images.append(urljoin(base_url, src))
        return images
        
    def extract_news_article(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> Dict[str, Any]:
        """Extract news article data"""
        result = {'url': url, 'type': 'news_article'}
        
        if "Title" in data_fields:
            result['title'] = self.extract_by_selectors(soup, self.extractor.NEWS_SELECTORS['title'])
            
        if "Content" in data_fields:
            result['content'] = self.extract_by_selectors(soup, self.extractor.NEWS_SELECTORS['content'])
            
        if "Author" in data_fields:
            result['author'] = self.extract_by_selectors(soup, self.extractor.NEWS_SELECTORS['author'])
            
        if "Timestamp" in data_fields:
            result['timestamp'] = self.extract_by_selectors(soup, self.extractor.NEWS_SELECTORS['timestamp'])
            
        if "Links" in data_fields:
            result['links'] = self.extract_links(soup, url)
            
        # Additional metadata
        result['meta_description'] = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            result['meta_description'] = meta_desc.get('content', '')
            
        result['images'] = self.extract_images(soup, url)
        
        return result
        
    def extract_social_media(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> Dict[str, Any]:
        """Extract social media post data"""
        result = {'url': url, 'type': 'social_media'}
        
        if "Title" in data_fields:
            result['title'] = self.extract_by_selectors(soup, self.extractor.SOCIAL_SELECTORS['title'])
            
        if "Content" in data_fields:
            result['content'] = self.extract_by_selectors(soup, self.extractor.SOCIAL_SELECTORS['content'])
            
        if "Author" in data_fields:
            result['author'] = self.extract_by_selectors(soup, self.extractor.SOCIAL_SELECTORS['author'])
            
        if "Links" in data_fields:
            result['links'] = self.extract_links(soup, url)
            
        # Social media specific data
        result['hashtags'] = self.extract_hashtags(soup)
        result['mentions'] = self.extract_mentions(soup)
        
        return result
        
    def extract_forum_discussion(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> Dict[str, Any]:
        """Extract forum discussion data"""
        result = {'url': url, 'type': 'forum_discussion'}
        
        if "Title" in data_fields:
            result['title'] = self.extract_by_selectors(soup, self.extractor.FORUM_SELECTORS['title'])
            
        if "Content" in data_fields:
            result['content'] = self.extract_by_selectors(soup, self.extractor.FORUM_SELECTORS['content'])
            
        if "Comments" in data_fields:
            comments = []
            comment_elements = soup.select('.reply, .post-reply, .message')
            for elem in comment_elements[:10]:  # Limit to 10 comments
                comment_text = elem.get_text().strip()
                if comment_text:
                    comments.append(comment_text)
            result['comments'] = comments
            
        if "Links" in data_fields:
            result['links'] = self.extract_links(soup, url)
            
        return result
        
    def extract_comments_section(self, soup: BeautifulSoup, url: str, data_fields: List[str]) -> Dict[str, Any]:
        """Extract comments section data"""
        result = {'url': url, 'type': 'comments_section'}
        
        if "Comments" in data_fields:
            comments = []
            comment_selectors = self.extractor.COMMENT_SELECTORS['comments']
            
            for selector in comment_selectors:
                comment_elements = soup.select(selector)
                if comment_elements:
                    for elem in comment_elements[:20]:  # Limit to 20 comments
                        comment_text = elem.get_text().strip()
                        if comment_text and len(comment_text) > 10:  # Filter out very short comments
                            comments.append(comment_text)
                    break
                    
            result['comments'] = comments
            
        if "Links" in data_fields:
            result['links'] = self.extract_links(soup, url)
            
        return result
        
    def extract_hashtags(self, soup: BeautifulSoup) -> List[str]:
        """Extract hashtags from social media content"""
        hashtags = []
        text = soup.get_text()
        hashtag_pattern = r'#\w+'
        hashtags = re.findall(hashtag_pattern, text)
        return list(set(hashtags))  # Remove duplicates
        
    def extract_mentions(self, soup: BeautifulSoup) -> List[str]:
        """Extract mentions from social media content"""
        mentions = []
        text = soup.get_text()
        mention_pattern = r'@\w+'
        mentions = re.findall(mention_pattern, text)
        return list(set(mentions))  # Remove duplicates
        
    def extract_custom_selectors(self, soup: BeautifulSoup, url: str, custom_selectors: str) -> Dict[str, Any]:
        """Extract data using custom CSS selectors"""
        result = {'url': url, 'type': 'custom'}
        
        try:
            lines = custom_selectors.strip().split('\n')
            for line in lines:
                if ':' in line:
                    field_name, selector = line.split(':', 1)
                    field_name = field_name.strip().lower()
                    selector = selector.strip()
                    
                    extracted_text = self.extract_by_selectors(soup, [selector])
                    if extracted_text:
                        result[field_name] = extracted_text
                        
        except Exception as e:
            logger.error(f"Custom selector error: {e}")
            
        return result
        
    def scrape_single_page(self, url: str, scrape_type: str, data_fields: List[str], 
                          custom_selectors: str = "") -> Optional[Dict[str, Any]]:
        """Scrape a single page"""
        soup = self.fetch_page(url)
        if not soup:
            return None
            
        # Extract data based on scrape type
        if custom_selectors:
            return self.extract_custom_selectors(soup, url, custom_selectors)
        elif scrape_type == "News Articles":
            return self.extract_news_article(soup, url, data_fields)
        elif scrape_type == "Social Media Posts":
            return self.extract_social_media(soup, url, data_fields)
        elif scrape_type == "Forum Discussions":
            return self.extract_forum_discussion(soup, url, data_fields)
        elif scrape_type == "Comments Section":
            return self.extract_comments_section(soup, url, data_fields)
        else:
            return self.extract_news_article(soup, url, data_fields)  # Default
            
    def find_next_page_urls(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Find URLs for pagination"""
        next_urls = []
        
        # Common pagination patterns
        pagination_selectors = [
            'a[rel="next"]',
            '.next',
            '.pagination a',
            '[class*="next"]',
            '[class*="page"]'
        ]
        
        for selector in pagination_selectors:
            elements = soup.select(selector)
            for elem in elements:
                href = elem.get('href')
                if href:
                    if href.startswith(('http://', 'https://')):
                        next_urls.append(href)
                    elif href.startswith('/'):
                        next_urls.append(urljoin(base_url, href))
                        
        return list(set(next_urls))  # Remove duplicates
        
    def scrape_multiple_pages(self, base_url: str, scrape_type: str, max_pages: int,
                             data_fields: List[str], custom_selectors: str = "") -> List[Dict[str, Any]]:
        """Scrape multiple pages with pagination"""
        results = []
        visited_urls = set()
        urls_to_visit = [base_url]
        
        for page_num in range(min(max_pages, 50)):  # Safety limit
            if not urls_to_visit or page_num >= len(urls_to_visit):
                break
                
            current_url = urls_to_visit[page_num] if page_num < len(urls_to_visit) else base_url
            
            if current_url in visited_urls:
                continue
                
            visited_urls.add(current_url)
            
            # Scrape current page
            page_data = self.scrape_single_page(current_url, scrape_type, data_fields, custom_selectors)
            if page_data and (page_data.get('title') or page_data.get('content')):
                results.append(page_data)
                
            # Find next page URLs for first page only
            if page_num == 0:
                soup = self.fetch_page(current_url)
                if soup:
                    next_urls = self.find_next_page_urls(soup, current_url)
                    for next_url in next_urls:
                        if next_url not in visited_urls:
                            urls_to_visit.append(next_url)
                            
        return results
        
    def get_scraping_stats(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        try:
            db_path = Path("data/web_scraper_cache.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get cache stats
            cursor.execute("SELECT COUNT(*) FROM scrape_cache WHERE success = 1")
            successful_scrapes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scrape_cache WHERE success = 0")
            failed_scrapes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scrape_cache")
            total_scrapes = cursor.fetchone()[0]
            
            success_rate = (successful_scrapes / total_scrapes * 100) if total_scrapes > 0 else 0
            
            conn.close()
            
            return {
                'total_scrapes': total_scrapes,
                'successful_scrapes': successful_scrapes,
                'failed_scrapes': failed_scrapes,
                'success_rate': round(success_rate, 2)
            }
        except Exception as e:
            logger.error(f"Stats retrieval error: {e}")
            return {
                'total_scrapes': 0,
                'successful_scrapes': 0,
                'failed_scrapes': 0,
                'success_rate': 0
            }
