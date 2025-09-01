"""
Advanced NLP Processing Engine for Police Cyber Monitoring
Enterprise-grade system supporting Hindi/English sentiment analysis, threat detection, 
bot detection, coordination analysis, and comprehensive evidence generation
"""

import re
import json
import hashlib
import logging
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import numpy as np
from pathlib import Path
import pickle
import threading
from functools import lru_cache
import time

# Suppress warnings
warnings.filterwarnings('ignore')

# Core NLP libraries
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    from nltk.stem import SnowballStemmer
    from nltk.corpus import wordnet
    
    # Download required NLTK data
    nltk_downloads = [
        'vader_lexicon', 'punkt', 'averaged_perceptron_tagger', 
        'maxent_ne_chunker', 'words', 'stopwords', 'wordnet',
        'punkt_tab', 'omw-1.4'
    ]
    for download in nltk_downloads:
        try:
            nltk.download(download, quiet=True)
        except:
            pass
            
except ImportError:
    print("NLTK not available. Install with: pip install nltk")

try:
    from textblob import TextBlob
    from textblob.sentiments import NaiveBayesAnalyzer
except ImportError:
    print("TextBlob not available. Install with: pip install textblob")

try:
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP_WORDS
    
    # Try to load English and Hindi models
    try:
        nlp_en = spacy.load("en_core_web_sm")
    except OSError:
        print("English spaCy model not found. Install with: python -m spacy download en_core_web_sm")
        nlp_en = None
    
    try:
        nlp_hi = spacy.load("hi_core_news_sm")
    except OSError:
        print("Hindi spaCy model not found. Install with: python -m spacy download hi_core_news_sm")
        nlp_hi = None
        
except ImportError:
    print("spaCy not available. Install with: pip install spacy")
    nlp_en = None
    nlp_hi = None

try:
    from transformers import (
        pipeline, AutoTokenizer, AutoModelForSequenceClassification,
        AutoModel, BertTokenizer, BertForSequenceClassification
    )
    
    # Initialize multiple sentiment analysis pipelines
    sentiment_pipeline = None
    multilingual_pipeline = None
    hate_speech_pipeline = None
    
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", 
                                    model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
        multilingual_pipeline = pipeline("sentiment-analysis",
                                        model="nlptown/bert-base-multilingual-uncased-sentiment")
        hate_speech_pipeline = pipeline("text-classification",
                                       model="unitary/toxic-bert")
    except Exception as e:
        print(f"Some transformer models failed to load: {e}")
        
except ImportError:
    print("Transformers not available. Install with: pip install transformers torch")
    sentiment_pipeline = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    sklearn_available = True
except ImportError:
    print("Scikit-learn not available. Install with: pip install scikit-learn")
    sklearn_available = False

import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Enhanced sentiment analysis result with multilingual support"""
    positive: float
    negative: float
    neutral: float
    compound: float
    label: str
    confidence: float
    language: str
    emotion_scores: Dict[str, float]
    subjectivity: float
    intensity: str
    cultural_context: Dict[str, Any]

@dataclass
class ThreatAnalysis:
    """Advanced threat analysis result with detailed categorization"""
    risk_score: float
    threat_type: str
    confidence: float
    detected_keywords: List[str]
    severity: str
    explanation: str
    evidence_points: List[str]
    threat_category: str
    sub_categories: List[str]
    geographical_indicators: List[str]
    temporal_indicators: List[str]
    network_indicators: List[str]
    probability_scores: Dict[str, float]
    mitigation_suggestions: List[str]

@dataclass
class EntityResult:
    """Enhanced named entity recognition result"""
    persons: List[Dict[str, Any]]  # Name, confidence, context
    organizations: List[Dict[str, Any]]
    locations: List[Dict[str, Any]]
    dates: List[Dict[str, Any]]
    money: List[Dict[str, Any]]
    phone_numbers: List[str]
    email_addresses: List[str]
    urls: List[str]
    social_handles: List[str]
    cryptocurrencies: List[str]
    vehicles: List[str]
    weapons: List[str]
    drugs: List[str]
    other_entities: Dict[str, List[Dict[str, Any]]]
    entity_relationships: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]

@dataclass
class BotAnalysis:
    """Advanced bot behavior analysis result"""
    is_bot_likely: bool
    bot_score: float
    confidence: float
    indicators: List[str]
    behavioral_patterns: Dict[str, float]
    automation_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    bot_type: str  # SPAM, PROPAGANDA, MISINFORMATION, COORDINATED
    sophistication_score: float
    human_probability: float
    detection_methods: List[str]
    temporal_patterns: Dict[str, Any]
    linguistic_patterns: Dict[str, Any]
    network_patterns: Dict[str, Any]

@dataclass
class CoordinationResult:
    """Enhanced content coordination detection result"""
    similarity_score: float
    is_coordinated: bool
    confidence: float
    similar_patterns: List[str]
    coordination_indicators: List[str]
    coordination_type: str  # TIMING, CONTENT, BEHAVIORAL, NETWORK
    network_size_estimate: int
    coordination_sophistication: str
    campaign_indicators: Dict[str, Any]
    temporal_coordination: Dict[str, Any]
    content_coordination: Dict[str, Any]
    behavioral_coordination: Dict[str, Any]

@dataclass
class IntelligenceInsight:
    """Advanced intelligence insight from content analysis"""
    insight_type: str
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    evidence: List[str]
    confidence: float
    actionable: bool
    time_sensitivity: str
    related_entities: List[str]
    intelligence_value: float
    verification_needed: bool

@dataclass
class EvidenceSummary:
    """Comprehensive police report format evidence summary"""
    case_id: str
    timestamp: datetime
    threat_level: str
    summary: str
    detailed_analysis: str
    evidence_points: List[str]
    recommended_actions: List[str]
    technical_details: Dict[str, Any]
    legal_implications: str
    intelligence_insights: List[IntelligenceInsight]
    chain_of_custody: List[Dict[str, Any]]
    forensic_markers: Dict[str, Any]
    correlation_data: Dict[str, Any]
    expert_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]

class AdvancedNLPEngine:
    """Enterprise-grade NLP processing engine for police cyber monitoring"""
    
    def __init__(self, openai_api_key: Optional[str] = None, config: Dict[str, Any] = None):
        """Initialize the advanced NLP engine"""
        self.openai_api_key = openai_api_key
        self.config = config or {}
        
        # Initialize core components
        self.sentiment_analyzer = SentimentIntensityAnalyzer() if 'nltk' in globals() else None
        self.stemmer_en = SnowballStemmer('english') if 'nltk' in globals() else None
        self.stemmer_hi = SnowballStemmer('arabic') if 'nltk' in globals() else None  # Closest to Hindi
        
        # Enhanced threat intelligence
        self.threat_keywords = self._load_enhanced_threat_keywords()
        self.anti_national_patterns = self._load_enhanced_anti_national_patterns()
        self.bot_indicators = self._load_enhanced_bot_indicators()
        self.coordination_patterns = self._load_coordination_patterns()
        
        # Advanced features
        self.emotion_lexicon = self._load_emotion_lexicon()
        self.cultural_context_db = self._load_cultural_context()
        self.entity_patterns = self._load_entity_patterns()
        
        # Machine learning models
        self.ml_models = self._initialize_ml_models()
        
        # Caching and performance
        self.content_cache = {}
        self.entity_cache = {}
        self.model_cache = {}
        
        # Threading for concurrent processing
        self.thread_lock = threading.Lock()
        
        # Performance metrics
        self.processing_stats = {
            'total_processed': 0,
            'avg_processing_time': 0,
            'cache_hits': 0,
            'model_usage': defaultdict(int)
        }
        
        logger.info("Advanced NLP Engine initialized with enhanced capabilities")
    
    def _load_enhanced_threat_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """Load comprehensive threat keywords with weights and context"""
        return {
            'terrorism': {
                'high_priority': [
                    'bomb', 'blast', 'attack', 'jihad', 'isis', 'al-qaeda', 'terrorist', 'suicide bomb',
                    'fidayeen', 'martyrdom', 'holy war', 'kafir', 'infidel',
                    'बम', 'धमाका', 'हमला', 'आतंकवाद', 'आतंकी', 'जिहाद', 'शहीद', 'काफिर'
                ],
                'medium_priority': [
                    'explosive', 'weapon', 'target', 'operation', 'mission', 'brotherhood',
                    'विस्फोटक', 'हथियार', 'निशाना', 'ऑपरेशन', 'मिशन'
                ],
                'context_dependent': [
                    'fight', 'struggle', 'resistance', 'freedom', 'liberation',
                    'लड़ाई', 'संघर्ष', 'प्रतिरोध', 'आजादी', 'मुक्ति'
                ]
            },
            'violence': {
                'high_priority': [
                    'kill', 'murder', 'assassinate', 'eliminate', 'destroy', 'annihilate',
                    'riot', 'lynch', 'massacre', 'slaughter', 'genocide',
                    'हत्या', 'मार डालो', 'नष्ट करो', 'दंगा', 'हिंसा', 'कत्लेआम'
                ],
                'medium_priority': [
                    'fight', 'beat', 'hurt', 'harm', 'damage', 'violence',
                    'लड़ाई', 'मारना', 'नुकसान', 'हिंसा'
                ],
                'weapons': [
                    'gun', 'pistol', 'rifle', 'ak47', 'grenade', 'knife', 'sword',
                    'बंदूक', 'पिस्तौल', 'राइफल', 'चाकू', 'तलवार'
                ]
            },
            'hate_speech': {
                'religious': [
                    'hindu', 'muslim', 'christian', 'sikh', 'buddhist', 'jain',
                    'हिंदू', 'मुस्लिम', 'ईसाई', 'सिख', 'बौद्ध', 'जैन'
                ],
                'caste': [
                    'brahmin', 'kshatriya', 'vaishya', 'shudra', 'dalit', 'scheduled caste',
                    'ब्राह्मण', 'क्षत्रिय', 'वैश्य', 'शूद्र', 'दलित'
                ],
                'slurs': [
                    'terrorist', 'traitor', 'anti-national', 'pakistan lover',
                    'आतंकवादी', 'गद्दार', 'राष्ट्रद्रोही', 'पाकिस्तान प्रेमी'
                ]
            },
            'anti_national': {
                'direct': [
                    'pakistan zindabad', 'destroy india', 'break india', 'anti-national',
                    'traitor to country', 'azaadi', 'khalistan', 'kashmir independence',
                    'पाकिस्तान जिंदाबाद', 'भारत को नष्ट करो', 'देश के गद्दार', 'खालिस्तान'
                ],
                'coded': [
                    'two nation theory', 'partition', 'separate homeland', 'independence movement',
                    'दो राष्ट्र सिद्धांत', 'विभाजन', 'अलग मातृभूमि'
                ]
            },
            'cybercrime': {
                'hacking': [
                    'hack', 'ddos', 'malware', 'phishing', 'ransomware', 'botnet',
                    'cyber attack', 'data breach', 'password crack',
                    'हैक', 'साइबर अटैक', 'डेटा चोरी'
                ],
                'fraud': [
                    'scam', 'fraud', 'fake', 'identity theft', 'credit card fraud',
                    'online fraud', 'banking fraud', 'upi fraud',
                    'धोखाधड़ी', 'नकली', 'पहचान चोरी', 'ऑनलाइन फ्रॉड'
                ]
            },
            'drugs': {
                'substances': [
                    'heroin', 'cocaine', 'marijuana', 'ganja', 'charas', 'opium',
                    'mdma', 'lsd', 'methamphetamine', 'brown sugar',
                    'हेरोइन', 'कोकीन', 'गांजा', 'चरस', 'अफीम', 'ब्राउन शुगर'
                ],
                'trafficking': [
                    'smuggling', 'dealing', 'peddling', 'drug trade', 'cartel',
                    'तस्करी', 'नशे का व्यापार', 'ड्रग डीलिंग'
                ]
            },
            'radicalization': {
                'ideology': [
                    'radical islam', 'extremist', 'fundamentalist', 'caliphate',
                    'sharia law', 'islamic state', 'mujahideen',
                    'कट्टरपंथी', 'अतिवादी', 'कैलिफेट', 'शरिया कानून'
                ],
                'recruitment': [
                    'join us', 'true believer', 'paradise', 'jannat', 'shaheed',
                    'हमारे साथ जुड़ें', 'सच्चा विश्वासी', 'जन्नत', 'शहीद'
                ]
            }
        }
    
    def _load_enhanced_anti_national_patterns(self) -> List[Dict[str, Any]]:
        """Load sophisticated anti-national content patterns"""
        return [
            {
                'pattern': r'pakistan\s+(zindabad|murdabad)',
                'weight': 0.9,
                'context': 'direct_support_enemy',
                'severity': 'CRITICAL'
            },
            {
                'pattern': r'destroy\s+india|break\s+india',
                'weight': 0.95,
                'context': 'direct_threat_nation',
                'severity': 'CRITICAL'
            },
            {
                'pattern': r'anti[_\s-]?national|traitor\s+to\s+country',
                'weight': 0.8,
                'context': 'ideological_opposition',
                'severity': 'HIGH'
            },
            {
                'pattern': r'azaadi|khalistan|kashmir\s+independence',
                'weight': 0.85,
                'context': 'separatist_movement',
                'severity': 'HIGH'
            },
            {
                'pattern': r'भारत\s+को\s+नष्ट|देश\s+के\s+गद्दार',
                'weight': 0.9,
                'context': 'hindi_anti_national',
                'severity': 'CRITICAL'
            },
            {
                'pattern': r'two\s+nation\s+theory|partition\s+of\s+india',
                'weight': 0.7,
                'context': 'historical_reference',
                'severity': 'MEDIUM'
            }
        ]
    
    def _load_enhanced_bot_indicators(self) -> Dict[str, Dict[str, float]]:
        """Load comprehensive bot detection indicators"""
        return {
            'linguistic_patterns': {
                'repetitive_phrases': 0.3,
                'grammatical_inconsistency': 0.25,
                'unnatural_language_flow': 0.2,
                'template_based_content': 0.35,
                'multilingual_inconsistency': 0.2,
                'emotional_incongruence': 0.15
            },
            'behavioral_patterns': {
                'high_frequency_posting': 0.3,
                'consistent_timing': 0.25,
                'lack_of_engagement': 0.2,
                'automated_responses': 0.3,
                'coordinated_hashtags': 0.25,
                'identical_sharing_patterns': 0.35
            },
            'network_patterns': {
                'suspicious_follower_ratio': 0.2,
                'fake_profile_connections': 0.3,
                'coordinated_following': 0.25,
                'burst_activity': 0.2,
                'cross_platform_consistency': 0.15
            },
            'content_patterns': {
                'duplicate_content': 0.4,
                'template_variations': 0.3,
                'copy_paste_behavior': 0.35,
                'content_farming': 0.25,
                'low_quality_content': 0.15
            }
        }
    
    def _load_coordination_patterns(self) -> Dict[str, Any]:
        """Load patterns for detecting coordinated behavior"""
        return {
            'temporal_patterns': {
                'simultaneous_posting': {'threshold': 60, 'weight': 0.4},  # seconds
                'regular_intervals': {'threshold': 0.1, 'weight': 0.3},  # coefficient of variation
                'synchronized_activity': {'threshold': 0.8, 'weight': 0.35}
            },
            'content_patterns': {
                'identical_text': {'threshold': 0.95, 'weight': 0.5},
                'template_variations': {'threshold': 0.8, 'weight': 0.4},
                'shared_urls': {'threshold': 0.7, 'weight': 0.3},
                'common_hashtags': {'threshold': 0.6, 'weight': 0.25}
            },
            'behavioral_patterns': {
                'similar_engagement': {'threshold': 0.7, 'weight': 0.3},
                'coordinated_likes': {'threshold': 0.8, 'weight': 0.35},
                'synchronized_shares': {'threshold': 0.75, 'weight': 0.3}
            }
        }
    
    def _load_emotion_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Load emotion detection lexicon for multiple languages"""
        return {
            'english': {
                'anger': ['angry', 'furious', 'rage', 'hate', 'mad', 'irritated'],
                'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'panic'],
                'joy': ['happy', 'excited', 'delighted', 'cheerful', 'joyful', 'elated'],
                'sadness': ['sad', 'depressed', 'miserable', 'unhappy', 'sorrowful'],
                'disgust': ['disgusted', 'revolted', 'sick', 'nauseated', 'repulsed'],
                'surprise': ['surprised', 'amazed', 'shocked', 'astonished', 'stunned']
            },
            'hindi': {
                'anger': ['गुस्सा', 'क्रोध', 'चिढ़', 'नफरत', 'गुस्से', 'नाराज'],
                'fear': ['डर', 'भय', 'डरना', 'घबराहट', 'चिंता', 'परेशानी'],
                'joy': ['खुशी', 'प्रसन्न', 'आनंद', 'हर्ष', 'उत्साह', 'मजा'],
                'sadness': ['दुख', 'उदास', 'गम', 'शोक', 'निराशा', 'अवसाद'],
                'disgust': ['घृणा', 'नफरत', 'जुगुप्सा', 'अरुचि'],
                'surprise': ['आश्चर्य', 'हैरानी', 'चकित', 'अचंभा', 'आश्चर्यचकित']
            }
        }
    
    def _load_cultural_context(self) -> Dict[str, Any]:
        """Load cultural context for better understanding"""
        return {
            'indian_context': {
                'festivals': ['दिवाली', 'होली', 'ईद', 'क्रिसमस', 'दुर्गा पूजा'],
                'political_terms': ['नेता', 'पार्टी', 'चुनाव', 'सरकार', 'विपक्ष'],
                'religious_terms': ['भगवान', 'अल्लाह', 'गुरु', 'मंदिर', 'मस्जिद'],
                'social_issues': ['जाति', 'धर्म', 'भ्रष्टाचार', 'गरीबी', 'शिक्षा']
            },
            'regional_languages': {
                'bengali': ['আমি', 'তুমি', 'ভালো', 'মন্দ'],
                'tamil': ['நான்', 'நீ', 'நல்ல', 'கெட்ட'],
                'telugu': ['నేను', 'నువ్వు', 'మంచి', 'చెడు'],
                'gujarati': ['હું', 'તું', 'સારું', 'ખરાબ']
            }
        }
    
    def _load_entity_patterns(self) -> Dict[str, str]:
        """Load regex patterns for entity extraction"""
        return {
            'indian_phone': r'(\+91|91|0)?[6-9]\d{9}',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'aadhar': r'\b\d{4}\s?\d{4}\s?\d{4}\b',
            'pan': r'\b[A-Z]{5}\d{4}[A-Z]\b',
            'vehicle_number': r'\b[A-Z]{2}\s?\d{2}\s?[A-Z]{1,2}\s?\d{4}\b',
            'bank_account': r'\b\d{9,18}\b',
            'ifsc': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
            'pincode': r'\b\d{6}\b',
            'bitcoin': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
            'ethereum': r'\b0x[a-fA-F0-9]{40}\b',
            'social_handle': r'@[A-Za-z0-9_]+',
            'hashtag': r'#[A-Za-z0-9_]+',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        }
    
    def _initialize_ml_models(self) -> Dict[str, Any]:
        """Initialize machine learning models for advanced analysis"""
        models = {}
        
        if sklearn_available:
            try:
                # TF-IDF vectorizer for similarity analysis
                models['tfidf'] = TfidfVectorizer(
                    max_features=10000,
                    stop_words='english',
                    ngram_range=(1, 3),
                    lowercase=True
                )
                
                # DBSCAN for clustering
                models['dbscan'] = DBSCAN(eps=0.5, min_samples=3)
                
                # LDA for topic modeling
                models['lda'] = LatentDirichletAllocation(
                    n_components=10,
                    random_state=42
                )
                
                logger.info("ML models initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing ML models: {e}")
        
        return models
    
    @lru_cache(maxsize=1000)
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Enhanced language detection with confidence and mixed language support"""
        # Character-based detection
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        
        total_chars = hindi_chars + english_chars + arabic_chars
        
        if total_chars == 0:
            return {'primary': 'unknown', 'confidence': 0.0, 'mixed': False, 'languages': []}
        
        # Calculate percentages
        hindi_pct = hindi_chars / total_chars
        english_pct = english_chars / total_chars
        arabic_pct = arabic_chars / total_chars
        
        # Determine primary language
        percentages = {'hindi': hindi_pct, 'english': english_pct, 'arabic': arabic_pct}
        primary = max(percentages, key=percentages.get)
        confidence = percentages[primary]
        
        # Check for mixed language content
        significant_languages = [lang for lang, pct in percentages.items() if pct > 0.2]
        is_mixed = len(significant_languages) > 1
        
        # Detect regional languages using basic patterns
        regional_indicators = []
        for lang, patterns in self.cultural_context_db.get('regional_languages', {}).items():
            for pattern in patterns:
                if pattern in text:
                    regional_indicators.append(lang)
        
        return {
            'primary': primary,
            'confidence': confidence,
            'mixed': is_mixed,
            'languages': significant_languages,
            'regional_indicators': regional_indicators,
            'language_distribution': percentages
        }
    
    def analyze_content_sentiment(self, text: str) -> SentimentResult:
        """
        Advanced sentiment analysis with multilingual support and emotion detection
        
        Args:
            text: Input text for sentiment analysis
            
        Returns:
            Enhanced SentimentResult with detailed analysis
        """
        start_time = time.time()
        
        try:
            # Language detection
            lang_info = self.detect_language(text)
            primary_language = lang_info['primary']
            
            # Initialize sentiment scores
            positive, negative, neutral, compound = 0.0, 0.0, 0.0, 0.0
            confidence = 0.0
            label = 'neutral'
            emotion_scores = {}
            subjectivity = 0.0
            intensity = 'LOW'
            cultural_context = {}
            
            # Multi-model sentiment analysis for better accuracy
            sentiment_results = []
            
            # VADER sentiment analysis (best for social media text)
            if self.sentiment_analyzer and primary_language in ['english', 'mixed']:
                try:
                    vader_scores = self.sentiment_analyzer.polarity_scores(text)
                    sentiment_results.append({
                        'model': 'vader',
                        'positive': vader_scores['pos'],
                        'negative': vader_scores['neg'],
                        'neutral': vader_scores['neu'],
                        'compound': vader_scores['compound'],
                        'weight': 0.3
                    })
                except Exception as e:
                    logger.debug(f"VADER analysis failed: {e}")
            
            # TextBlob sentiment analysis
            if 'TextBlob' in globals():
                try:
                    blob = TextBlob(text)
                    tb_polarity = blob.sentiment.polarity
                    tb_subjectivity = blob.sentiment.subjectivity
                    
                    sentiment_results.append({
                        'model': 'textblob',
                        'positive': (tb_polarity + 1) / 2 if tb_polarity > 0 else 0,
                        'negative': (1 - tb_polarity) / 2 if tb_polarity < 0 else 0,
                        'neutral': 1 - abs(tb_polarity),
                        'compound': tb_polarity,
                        'weight': 0.25,
                        'subjectivity': tb_subjectivity
                    })
                    subjectivity = tb_subjectivity
                except Exception as e:
                    logger.debug(f"TextBlob analysis failed: {e}")
            
            # Transformer-based sentiment analysis
            if sentiment_pipeline:
                try:
                    result = sentiment_pipeline(text[:512])[0]  # Limit text length
                    transformer_label = result['label'].lower()
                    transformer_score = result['score']
                    
                    if 'positive' in transformer_label or 'pos' in transformer_label:
                        sentiment_results.append({
                            'model': 'transformer',
                            'positive': transformer_score,
                            'negative': 1 - transformer_score,
                            'neutral': 0.0,
                            'compound': transformer_score,
                            'weight': 0.35
                        })
                    elif 'negative' in transformer_label or 'neg' in transformer_label:
                        sentiment_results.append({
                            'model': 'transformer',
                            'positive': 1 - transformer_score,
                            'negative': transformer_score,
                            'neutral': 0.0,
                            'compound': -transformer_score,
                            'weight': 0.35
                        })
                except Exception as e:
                    logger.debug(f"Transformer sentiment analysis failed: {e}")
            
            # Multilingual transformer analysis
            if multilingual_pipeline and primary_language != 'unknown':
                try:
                    result = multilingual_pipeline(text[:512])[0]
                    ml_score = float(result['label'].split(' ')[0]) / 5.0  # Convert 1-5 scale to 0-1
                    ml_compound = (ml_score - 0.5) * 2  # Convert to -1 to 1 scale
                    
                    sentiment_results.append({
                        'model': 'multilingual',
                        'positive': ml_score if ml_compound > 0 else 0,
                        'negative': 1 - ml_score if ml_compound < 0 else 0,
                        'neutral': 1 - abs(ml_compound),
                        'compound': ml_compound,
                        'weight': 0.3
                    })
                except Exception as e:
                    logger.debug(f"Multilingual sentiment analysis failed: {e}")
            
            # Ensemble the results
            if sentiment_results:
                total_weight = sum(r['weight'] for r in sentiment_results)
                positive = sum(r['positive'] * r['weight'] for r in sentiment_results) / total_weight
                negative = sum(r['negative'] * r['weight'] for r in sentiment_results) / total_weight
                neutral = sum(r['neutral'] * r['weight'] for r in sentiment_results) / total_weight
                compound = sum(r['compound'] * r['weight'] for r in sentiment_results) / total_weight
                
                # Determine label and confidence
                if compound >= 0.05:
                    label = 'positive'
                    confidence = positive
                elif compound <= -0.05:
                    label = 'negative'
                    confidence = negative
                else:
                    label = 'neutral'
                    confidence = neutral
                
                # Determine intensity
                if abs(compound) >= 0.7:
                    intensity = 'HIGH'
                elif abs(compound) >= 0.4:
                    intensity = 'MEDIUM'
                else:
                    intensity = 'LOW'
            
            # Emotion analysis
            emotion_scores = self._analyze_emotions(text, primary_language)
            
            # Cultural context analysis
            cultural_context = self._analyze_cultural_context(text, primary_language)
            
            # Update processing stats
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, 'sentiment_analysis')
            
            return SentimentResult(
                positive=positive,
                negative=negative,
                neutral=neutral,
                compound=compound,
                label=label,
                confidence=confidence,
                language=primary_language,
                emotion_scores=emotion_scores,
                subjectivity=subjectivity,
                intensity=intensity,
                cultural_context=cultural_context
            )
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return SentimentResult(
                positive=0.0, negative=0.0, neutral=1.0, compound=0.0,
                label='neutral', confidence=0.0, language='unknown',
                emotion_scores={}, subjectivity=0.0, intensity='LOW',
                cultural_context={}
            )
    
    def detect_anti_national_content(self, text: str, metadata: Dict[str, Any] = None) -> ThreatAnalysis:
        """
        Advanced anti-national content detection with sophisticated pattern matching
        
        Args:
            text: Input text to analyze
            metadata: Additional context information
            
        Returns:
            Enhanced ThreatAnalysis with comprehensive threat assessment
        """
        start_time = time.time()
        
        try:
            metadata = metadata or {}
            text_lower = text.lower()
            detected_keywords = []
            evidence_points = []
            risk_score = 0.0
            sub_categories = []
            geographical_indicators = []
            temporal_indicators = []
            network_indicators = []
            probability_scores = {}
            
            # Enhanced keyword analysis with context and weights
            for category, subcategories in self.threat_keywords.items():
                if category in ['anti_national', 'terrorism', 'hate_speech']:
                    category_score = 0
                    category_keywords = []
                    
                    if isinstance(subcategories, dict):
                        for priority, keywords in subcategories.items():
                            weight = {'high_priority': 25, 'medium_priority': 15, 'context_dependent': 10}.get(priority, 10)
                            
                            for keyword in keywords:
                                if keyword.lower() in text_lower:
                                    category_keywords.append(keyword)
                                    
                                    # Context-dependent analysis
                                    if priority == 'context_dependent':
                                        context_score = self._analyze_keyword_context(text, keyword)
                                        weight *= context_score
                                    
                                    category_score += weight
                                    evidence_points.append(
                                        f"{category.title()} keyword detected: '{keyword}' (priority: {priority})"
                                    )
                    
                    if category_keywords:
                        detected_keywords.extend(category_keywords)
                        risk_score += min(category_score, 60)  # Cap per category
                        sub_categories.append(category)
                        probability_scores[category] = min(category_score / 60, 1.0)
            
            # Advanced pattern matching with context analysis
            for pattern_info in self.anti_national_patterns:
                pattern = pattern_info['pattern']
                weight = pattern_info['weight']
                context = pattern_info['context']
                severity = pattern_info['severity']
                
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    pattern_score = len(matches) * weight * 30
                    risk_score += pattern_score
                    
                    evidence_points.append(
                        f"Anti-national pattern detected: {context} (severity: {severity})"
                    )
                    
                    # Extract geographical indicators
                    if 'geographical' in context or any(place in text_lower for place in ['kashmir', 'khalistan', 'northeast']):
                        geographical_indicators.extend(matches)
            
            # Sentiment-based risk amplification
            sentiment = self.analyze_content_sentiment(text)
            if sentiment.negative > 0.7:
                risk_score += 15
                evidence_points.append(f"Highly negative sentiment detected (score: {sentiment.negative:.2f})")
            
            # Emotion analysis for additional context
            dominant_emotions = [emotion for emotion, score in sentiment.emotion_scores.items() if score > 0.6]
            if 'anger' in dominant_emotions or 'disgust' in dominant_emotions:
                risk_score += 10
                evidence_points.append(f"Hostile emotions detected: {', '.join(dominant_emotions)}")
            
            # Cultural context analysis
            cultural_flags = self._detect_cultural_context_flags(text, sentiment.cultural_context)
            if cultural_flags:
                risk_score += len(cultural_flags) * 5
                evidence_points.extend([f"Cultural context flag: {flag}" for flag in cultural_flags])
            
            # Metadata-based risk factors
            if metadata:
                metadata_risk = self._analyze_metadata_risk(metadata, 'anti_national')
                risk_score += metadata_risk['score']
                evidence_points.extend(metadata_risk['evidence'])
                network_indicators.extend(metadata_risk.get('network_indicators', []))
            
            # Temporal analysis
            temporal_risk = self._analyze_temporal_patterns(text, metadata.get('timestamp'))
            if temporal_risk['suspicious']:
                risk_score += temporal_risk['score']
                temporal_indicators.extend(temporal_risk['indicators'])
                evidence_points.extend(temporal_risk['evidence'])
            
            # Advanced hate speech detection
            if hate_speech_pipeline:
                try:
                    hate_result = hate_speech_pipeline(text[:512])[0]
                    if hate_result['label'] == 'TOXIC' and hate_result['score'] > 0.7:
                        risk_score += 20
                        evidence_points.append(f"Toxic content detected (confidence: {hate_result['score']:.2f})")
                except Exception as e:
                    logger.debug(f"Hate speech detection failed: {e}")
            
            # Determine threat classification
            if risk_score >= 80:
                severity = 'CRITICAL'
                threat_type = 'Confirmed Anti-National Content'
                threat_category = 'NATIONAL_SECURITY_THREAT'
            elif risk_score >= 60:
                severity = 'HIGH'
                threat_type = 'Likely Anti-National Content'
                threat_category = 'SECURITY_CONCERN'
            elif risk_score >= 40:
                severity = 'MEDIUM'
                threat_type = 'Potential Anti-National Content'
                threat_category = 'SUSPICIOUS_ACTIVITY'
            elif risk_score >= 20:
                severity = 'LOW'
                threat_type = 'Questionable Content'
                threat_category = 'MONITORING_REQUIRED'
            else:
                severity = 'MINIMAL'
                threat_type = 'No Significant Anti-National Content'
                threat_category = 'ROUTINE_CONTENT'
            
            # Calculate confidence based on multiple factors
            confidence_factors = [
                len(evidence_points) * 0.1,
                len(detected_keywords) * 0.05,
                sentiment.confidence * 0.3,
                (len(sub_categories) / 3) * 0.2  # Normalize by max expected categories
            ]
            confidence = min(0.95, sum(confidence_factors))
            
            # Generate explanation
            explanation = self._generate_advanced_threat_explanation(
                'anti_national', detected_keywords, evidence_points, risk_score, confidence
            )
            
            # Generate mitigation suggestions
            mitigation_suggestions = self._generate_mitigation_suggestions(
                threat_category, risk_score, sub_categories
            )
            
            # Update processing stats
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, 'anti_national_detection')
            
            return ThreatAnalysis(
                risk_score=min(100, risk_score),
                threat_type=threat_type,
                confidence=confidence,
                detected_keywords=detected_keywords,
                severity=severity,
                explanation=explanation,
                evidence_points=evidence_points,
                threat_category=threat_category,
                sub_categories=sub_categories,
                geographical_indicators=geographical_indicators,
                temporal_indicators=temporal_indicators,
                network_indicators=network_indicators,
                probability_scores=probability_scores,
                mitigation_suggestions=mitigation_suggestions
            )
            
        except Exception as e:
            logger.error(f"Anti-national content detection error: {str(e)}")
            return ThreatAnalysis(
                risk_score=0.0, threat_type='Analysis Failed', confidence=0.0,
                detected_keywords=[], severity='UNKNOWN', explanation=str(e),
                evidence_points=[], threat_category='ERROR', sub_categories=[],
                geographical_indicators=[], temporal_indicators=[], network_indicators=[],
                probability_scores={}, mitigation_suggestions=[]
            )
    
    def calculate_risk_score(self, text: str, metadata: Dict[str, Any] = None, 
                           context_data: Dict[str, Any] = None) -> float:
        """
        Advanced risk score calculation with multi-factor analysis
        
        Args:
            text: Content to analyze
            metadata: User/content metadata
            context_data: Additional contextual information
            
        Returns:
            Comprehensive risk score from 0-100
        """
        start_time = time.time()
        
        try:
            metadata = metadata or {}
            context_data = context_data or {}
            total_risk = 0.0
            risk_components = {}
            
            # 1. Content-based risk analysis (40% weight)
            content_risk = self._calculate_content_risk(text)
            total_risk += content_risk * 0.4
            risk_components['content'] = content_risk
            
            # 2. Sentiment and emotion risk (15% weight)
            sentiment = self.analyze_content_sentiment(text)
            sentiment_risk = self._calculate_sentiment_risk(sentiment)
            total_risk += sentiment_risk * 0.15
            risk_components['sentiment'] = sentiment_risk
            
            # 3. Entity and network risk (15% weight)
            entities = self.extract_entities(text)
            entity_risk = self._calculate_entity_risk(entities, metadata)
            total_risk += entity_risk * 0.15
            risk_components['entities'] = entity_risk
            
            # 4. User behavior risk (20% weight)
            if metadata:
                behavior_risk = self._calculate_behavior_risk(metadata, context_data)
                total_risk += behavior_risk * 0.2
                risk_components['behavior'] = behavior_risk
            
            # 5. Temporal and contextual risk (10% weight)
            temporal_risk = self._calculate_temporal_risk(text, metadata, context_data)
            total_risk += temporal_risk * 0.1
            risk_components['temporal'] = temporal_risk
            
            # Advanced ML-based risk scoring if models available
            if self.ml_models and sklearn_available:
                try:
                    ml_risk = self._calculate_ml_risk_score(text, metadata)
                    # Use ML score as adjustment factor
                    total_risk = total_risk * (0.8 + 0.4 * ml_risk)
                    risk_components['ml_adjustment'] = ml_risk
                except Exception as e:
                    logger.debug(f"ML risk calculation failed: {e}")
            
            # Apply risk amplifiers and dampeners
            risk_multiplier = self._calculate_risk_multiplier(text, metadata, context_data)
            total_risk *= risk_multiplier
            risk_components['multiplier'] = risk_multiplier
            
            # Normalize and cap the final score
            final_score = min(100.0, max(0.0, total_risk))
            
            # Cache the result for performance
            cache_key = hashlib.md5(f"{text[:100]}{str(metadata)}".encode()).hexdigest()
            self.content_cache[cache_key] = {
                'risk_score': final_score,
                'components': risk_components,
                'timestamp': datetime.now()
            }
            
            # Update processing stats
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, 'risk_calculation')
            
            return final_score
            
        except Exception as e:
            logger.error(f"Risk score calculation error: {str(e)}")
            return 0.0
    
    def _calculate_content_risk(self, text: str) -> float:
        """Calculate risk based on content analysis"""
        risk = 0.0
        text_lower = text.lower()
        
        # Threat category analysis
        for category, subcategories in self.threat_keywords.items():
            category_risk = 0
            
            if isinstance(subcategories, dict):
                for priority, keywords in subcategories.items():
                    weight = {'high_priority': 25, 'medium_priority': 15, 'context_dependent': 10}.get(priority, 10)
                    
                    for keyword in keywords:
                        if keyword.lower() in text_lower:
                            context_multiplier = self._analyze_keyword_context(text, keyword)
                            category_risk += weight * context_multiplier
            else:
                # Backward compatibility
                for keyword in subcategories:
                    if keyword.lower() in text_lower:
                        category_risk += 15
            
            # Apply category-specific weights
            category_weights = {
                'terrorism': 1.5, 'anti_national': 1.4, 'violence': 1.3,
                'hate_speech': 1.2, 'cybercrime': 1.0, 'drugs': 1.1,
                'radicalization': 1.4
            }
            weight = category_weights.get(category, 1.0)
            risk += min(category_risk * weight, 40)  # Cap per category
        
        return min(risk, 100)
    
    def _calculate_sentiment_risk(self, sentiment: SentimentResult) -> float:
        """Calculate risk based on sentiment analysis"""
        risk = 0.0
        
        # Negative sentiment risk
        if sentiment.negative > 0.8:
            risk += 30
        elif sentiment.negative > 0.6:
            risk += 20
        elif sentiment.negative > 0.4:
            risk += 10
        
        # Emotion-based risk
        high_risk_emotions = ['anger', 'disgust', 'fear']
        for emotion in high_risk_emotions:
            score = sentiment.emotion_scores.get(emotion, 0)
            if score > 0.7:
                risk += 15
            elif score > 0.5:
                risk += 10
        
        # Intensity amplification
        if sentiment.intensity == 'HIGH':
            risk *= 1.3
        elif sentiment.intensity == 'MEDIUM':
            risk *= 1.1
        
        # Low confidence penalty
        if sentiment.confidence < 0.3:
            risk *= 0.7
        
        return min(risk, 100)
    
    def _calculate_entity_risk(self, entities: EntityResult, metadata: Dict[str, Any]) -> float:
        """Calculate risk based on extracted entities"""
        risk = 0.0
        
        # High-risk entities
        if entities.weapons:
            risk += len(entities.weapons) * 15
        
        if entities.drugs:
            risk += len(entities.drugs) * 12
        
        if entities.cryptocurrencies:
            risk += len(entities.cryptocurrencies) * 8
        
        # Suspicious locations
        high_risk_locations = ['pakistan', 'afghanistan', 'syria', 'iraq']
        for location_data in entities.locations:
            location = location_data.get('text', '').lower() if isinstance(location_data, dict) else location_data.lower()
            if any(risky in location for risky in high_risk_locations):
                risk += 10
        
        # Multiple communication channels (phones, emails)
        if len(entities.phone_numbers) > 2:
            risk += 8
        
        if len(entities.email_addresses) > 3:
            risk += 6
        
        # Suspicious organizations
        terrorist_orgs = ['isis', 'al-qaeda', 'taliban', 'let', 'jaish']
        for org_data in entities.organizations:
            org = org_data.get('text', '').lower() if isinstance(org_data, dict) else org_data.lower()
            if any(terror_org in org for terror_org in terrorist_orgs):
                risk += 25
        
        return min(risk, 100)
    
    def _calculate_behavior_risk(self, metadata: Dict[str, Any], context_data: Dict[str, Any]) -> float:
        """Calculate risk based on user behavior patterns"""
        risk = 0.0
        
        # Account characteristics
        account_age_days = metadata.get('account_age_days', 365)
        if account_age_days < 7:
            risk += 25
        elif account_age_days < 30:
            risk += 15
        elif account_age_days < 90:
            risk += 8
        
        # Activity patterns
        posts_per_day = metadata.get('posts_per_day', 1)
        if posts_per_day > 100:
            risk += 30
        elif posts_per_day > 50:
            risk += 20
        elif posts_per_day > 20:
            risk += 12
        
        # Network characteristics
        followers = metadata.get('followers', 100)
        following = metadata.get('following', 100)
        if following > 0:
            ratio = followers / following
            if ratio < 0.05:  # Very suspicious ratio
                risk += 20
            elif ratio < 0.2:
                risk += 12
            elif ratio < 0.5:
                risk += 5
        
        # Engagement patterns
        avg_engagement = metadata.get('avg_engagement_rate', 0.05)
        if avg_engagement < 0.01:  # Very low engagement
            risk += 10
        elif avg_engagement > 0.5:  # Unusually high engagement
            risk += 8
        
        # Geographic risk factors
        location = metadata.get('location', '').lower()
        high_risk_regions = ['pakistan', 'afghanistan', 'syria', 'disputed region']
        if any(region in location for region in high_risk_regions):
            risk += 15
        
        # VPN/Proxy usage
        if metadata.get('using_proxy', False) or metadata.get('using_vpn', False):
            risk += 10
        
        return min(risk, 100)
    
    def _calculate_temporal_risk(self, text: str, metadata: Dict[str, Any], 
                               context_data: Dict[str, Any]) -> float:
        """Calculate risk based on temporal patterns"""
        risk = 0.0
        
        # Posting time analysis
        current_hour = datetime.now().hour
        if 2 <= current_hour <= 5:  # Suspicious hours
            risk += 8
        elif 22 <= current_hour <= 24 or 0 <= current_hour <= 2:
            risk += 5
        
        # Event correlation
        if context_data.get('major_event_proximity', False):
            risk += 12
        
        if context_data.get('holiday_period', False):
            risk += 8
        
        # Frequency spikes
        if context_data.get('posting_frequency_spike', False):
            risk += 10
        
        # Coordinated timing
        if context_data.get('coordinated_timing_detected', False):
            risk += 15
        
        return min(risk, 100)
    
    def _calculate_ml_risk_score(self, text: str, metadata: Dict[str, Any]) -> float:
        """Calculate risk using machine learning models"""
        try:
            if 'tfidf' not in self.ml_models:
                return 0.5  # Neutral score
            
            # Vectorize the text
            vectorizer = self.ml_models['tfidf']
            
            # For demonstration - in production, this would use pre-trained models
            # Here we simulate ML-based risk assessment
            
            # Text complexity analysis
            words = text.split()
            unique_words = len(set(words))
            repetition_ratio = 1 - (unique_words / len(words)) if words else 0
            
            # Simple heuristic-based ML simulation
            complexity_score = len(words) / 100  # Normalize word count
            repetition_penalty = repetition_ratio * 0.5
            
            ml_risk = min(1.0, complexity_score + repetition_penalty)
            
            return ml_risk
            
        except Exception as e:
            logger.debug(f"ML risk calculation error: {e}")
            return 0.5  # Neutral score
    
    def _calculate_risk_multiplier(self, text: str, metadata: Dict[str, Any], 
                                 context_data: Dict[str, Any]) -> float:
        """Calculate risk multiplier based on various factors"""
        multiplier = 1.0
        
        # Length-based adjustment
        text_length = len(text)
        if text_length > 2000:  # Very long posts
            multiplier *= 1.1
        elif text_length < 50:  # Very short posts
            multiplier *= 0.9
        
        # Language mixing (often indicates automated content)
        lang_info = self.detect_language(text)
        if lang_info['mixed']:
            multiplier *= 1.05
        
        # Verified account dampener
        if metadata.get('verified', False):
            multiplier *= 0.8
        
        # High follower count dampener (but not for very new accounts)
        followers = metadata.get('followers', 0)
        account_age = metadata.get('account_age_days', 0)
        if followers > 10000 and account_age > 365:
            multiplier *= 0.9
        
        # Context amplifiers
        if context_data.get('viral_content', False):
            multiplier *= 1.2
        
        if context_data.get('trending_hashtags', False):
            multiplier *= 1.1
        
        return max(0.5, min(2.0, multiplier))  # Cap the multiplier
    
    def identify_bot_behavior(self, user_data: Dict[str, Any], 
                            recent_posts: List[str] = None,
                            network_data: Dict[str, Any] = None) -> BotAnalysis:
        """
        Advanced bot behavior identification with multi-factor analysis
        
        Args:
            user_data: Comprehensive user profile information
            recent_posts: List of recent posts from the user
            network_data: Network analysis data
            
        Returns:
            Enhanced BotAnalysis with detailed assessment
        """
        start_time = time.time()
        
        try:
            recent_posts = recent_posts or []
            network_data = network_data or {}
            
            bot_score = 0.0
            indicators = []
            behavioral_patterns = {}
            detection_methods = []
            temporal_patterns = {}
            linguistic_patterns = {}
            network_patterns = {}
            
            # 1. Linguistic Pattern Analysis (30% weight)
            if recent_posts:
                linguistic_analysis = self._analyze_linguistic_patterns(recent_posts)
                linguistic_score = linguistic_analysis['bot_score']
                bot_score += linguistic_score * 0.3
                
                linguistic_patterns = linguistic_analysis['patterns']
                indicators.extend(linguistic_analysis['indicators'])
                detection_methods.append('linguistic_analysis')
                
                if linguistic_score > 60:
                    indicators.append(f"Strong linguistic bot indicators (score: {linguistic_score:.1f})")
            
            # 2. Behavioral Pattern Analysis (25% weight)
            behavioral_analysis = self._analyze_behavioral_patterns(user_data, recent_posts)
            behavioral_score = behavioral_analysis['bot_score']
            bot_score += behavioral_score * 0.25
            
            behavioral_patterns.update(behavioral_analysis['patterns'])
            indicators.extend(behavioral_analysis['indicators'])
            detection_methods.append('behavioral_analysis')
            
            # 3. Temporal Pattern Analysis (20% weight)
            temporal_analysis = self._analyze_temporal_patterns_bot(user_data, recent_posts)
            temporal_score = temporal_analysis['bot_score']
            bot_score += temporal_score * 0.2
            
            temporal_patterns = temporal_analysis['patterns']
            indicators.extend(temporal_analysis['indicators'])
            detection_methods.append('temporal_analysis')
            
            # 4. Network Pattern Analysis (15% weight)
            if network_data:
                network_analysis = self._analyze_network_patterns(user_data, network_data)
                network_score = network_analysis['bot_score']
                bot_score += network_score * 0.15
                
                network_patterns = network_analysis['patterns']
                indicators.extend(network_analysis['indicators'])
                detection_methods.append('network_analysis')
            
            # 5. Content Pattern Analysis (10% weight)
            if recent_posts:
                content_analysis = self._analyze_content_patterns_bot(recent_posts)
                content_score = content_analysis['bot_score']
                bot_score += content_score * 0.1
                
                indicators.extend(content_analysis['indicators'])
                detection_methods.append('content_analysis')
            
            # Determine automation level
            if bot_score >= 85:
                automation_level = 'CRITICAL'
                bot_type = 'SOPHISTICATED_BOT'
            elif bot_score >= 70:
                automation_level = 'HIGH'
                bot_type = 'ADVANCED_BOT'
            elif bot_score >= 50:
                automation_level = 'MEDIUM'
                bot_type = 'SIMPLE_BOT'
            elif bot_score >= 30:
                automation_level = 'LOW'
                bot_type = 'SEMI_AUTOMATED'
            else:
                automation_level = 'MINIMAL'
                bot_type = 'LIKELY_HUMAN'
            
            # Determine bot type based on patterns
            if 'coordinated_behavior' in indicators:
                bot_type = 'COORDINATED_INAUTHENTIC_BEHAVIOR'
            elif any('misinformation' in ind.lower() for ind in indicators):
                bot_type = 'MISINFORMATION_BOT'
            elif any('spam' in ind.lower() for ind in indicators):
                bot_type = 'SPAM_BOT'
            elif any('propaganda' in ind.lower() for ind in indicators):
                bot_type = 'PROPAGANDA_BOT'
            
            # Calculate sophistication score
            sophistication_factors = [
                len(detection_methods) / 5,  # Method diversity
                len(set(indicators)) / 10,   # Indicator uniqueness
                (100 - bot_score) / 100,     # Evasion capability
                behavioral_patterns.get('profile_completeness', 0.5)
            ]
            sophistication_score = sum(sophistication_factors) / len(sophistication_factors) * 100
            
            # Calculate human probability
            human_probability = max(0, 100 - bot_score)
            
            # Final determination
            is_bot_likely = bot_score > 50
            confidence = min(0.95, (bot_score / 100) + 0.1)
            
            # Update processing stats
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, 'bot_detection')
            
            return BotAnalysis(
                is_bot_likely=is_bot_likely,
                bot_score=min(100, bot_score),
                confidence=confidence,
                indicators=indicators,
                behavioral_patterns=behavioral_patterns,
                automation_level=automation_level,
                bot_type=bot_type,
                sophistication_score=sophistication_score,
                human_probability=human_probability,
                detection_methods=detection_methods,
                temporal_patterns=temporal_patterns,
                linguistic_patterns=linguistic_patterns,
                network_patterns=network_patterns
            )
            
        except Exception as e:
            logger.error(f"Bot behavior analysis error: {str(e)}")
            return BotAnalysis(
                is_bot_likely=False, bot_score=0.0, confidence=0.0,
                indicators=[str(e)], behavioral_patterns={},
                automation_level='UNKNOWN', bot_type='ANALYSIS_FAILED',
                sophistication_score=0.0, human_probability=100.0,
                detection_methods=[], temporal_patterns={},
                linguistic_patterns={}, network_patterns={}
            )
    
    def _analyze_linguistic_patterns(self, posts: List[str]) -> Dict[str, Any]:
        """Analyze linguistic patterns for bot detection"""
        indicators = []
        patterns = {}
        bot_score = 0.0
        
        if not posts:
            return {'bot_score': 0, 'indicators': [], 'patterns': {}}
        
        try:
            # Content repetition analysis
            unique_posts = len(set(posts))
            total_posts = len(posts)
            repetition_ratio = 1 - (unique_posts / total_posts) if total_posts > 0 else 0
            patterns['content_repetition'] = repetition_ratio
            
            if repetition_ratio > 0.8:
                bot_score += 40
                indicators.append("Extremely high content repetition")
            elif repetition_ratio > 0.6:
                bot_score += 25
                indicators.append("High content repetition")
            elif repetition_ratio > 0.4:
                bot_score += 15
                indicators.append("Moderate content repetition")
            
            # Language consistency analysis
            languages = []
            for post in posts:
                lang_info = self.detect_language(post)
                languages.append(lang_info['primary'])
            
            language_consistency = len(set(languages)) / len(languages) if languages else 1
            patterns['language_consistency'] = 1 - language_consistency
            
            if language_consistency > 0.5:  # Highly inconsistent
                bot_score += 20
                indicators.append("Inconsistent language patterns")
            
            # Grammar and syntax analysis
            grammar_scores = []
            for post in posts[:10]:  # Analyze first 10 posts
                if 'TextBlob' in globals():
                    try:
                        blob = TextBlob(post)
                        # Simple grammar check based on sentence structure
                        sentences = blob.sentences
                        if sentences:
                            avg_sentence_length = sum(len(s.words) for s in sentences) / len(sentences)
                            grammar_scores.append(avg_sentence_length)
                    except:
                        pass
            
            if grammar_scores:
                grammar_variance = np.var(grammar_scores)
                patterns['grammar_variance'] = grammar_variance
                
                if grammar_variance < 2:  # Very consistent grammar patterns
                    bot_score += 15
                    indicators.append("Unnaturally consistent grammar patterns")
            
            # Template detection
            template_patterns = self._detect_template_patterns(posts)
            if template_patterns['is_template_based']:
                bot_score += 30
                indicators.append(f"Template-based content detected: {template_patterns['pattern_type']}")
                patterns['template_score'] = template_patterns['confidence']
            
            # Emotional consistency analysis
            emotion_consistency = self._analyze_emotional_consistency(posts)
            patterns['emotional_consistency'] = emotion_consistency
            
            if emotion_consistency > 0.9:  # Unnaturally consistent emotions
                bot_score += 20
                indicators.append("Unnaturally consistent emotional patterns")
            
        except Exception as e:
            logger.debug(f"Linguistic pattern analysis error: {e}")
        
        return {
            'bot_score': min(100, bot_score),
            'indicators': indicators,
            'patterns': patterns
        }
    
    def _analyze_behavioral_patterns(self, user_data: Dict[str, Any], 
                                   posts: List[str]) -> Dict[str, Any]:
        """Analyze behavioral patterns for bot detection"""
        indicators = []
        patterns = {}
        bot_score = 0.0
        
        try:
            # Posting frequency analysis
            posts_per_day = user_data.get('posts_per_day', 1)
            patterns['posting_frequency'] = posts_per_day
            
            if posts_per_day > 200:
                bot_score += 50
                indicators.append("Extremely high posting frequency")
            elif posts_per_day > 100:
                bot_score += 35
                indicators.append("Very high posting frequency")
            elif posts_per_day > 50:
                bot_score += 20
                indicators.append("High posting frequency")
            
            # Profile completeness analysis
            profile_fields = ['bio', 'profile_image', 'location', 'website', 'display_name']
            completed_fields = sum(1 for field in profile_fields if user_data.get(field))
            profile_completeness = completed_fields / len(profile_fields)
            patterns['profile_completeness'] = profile_completeness
            
            if profile_completeness < 0.3:
                bot_score += 25
                indicators.append("Incomplete profile (typical bot behavior)")
            
            # Username analysis
            username = user_data.get('username', '').lower()
            if re.match(r'^user\d+$', username) or re.match(r'^[a-z]+\d{6,}$', username):
                bot_score += 30
                indicators.append("Generic/auto-generated username pattern")
                patterns['username_pattern'] = 'generic'
            
            # Follower-following ratio analysis
            followers = user_data.get('followers', 0)
            following = user_data.get('following', 0)
            
            if following > 0:
                ratio = followers / following
                patterns['follower_ratio'] = ratio
                
                if ratio < 0.01:  # Very low ratio
                    bot_score += 25
                    indicators.append("Extremely low follower-to-following ratio")
                elif ratio < 0.1:
                    bot_score += 15
                    indicators.append("Low follower-to-following ratio")
            
            # Account age vs activity analysis
            account_age_days = user_data.get('account_age_days', 365)
            if account_age_days > 0:
                activity_rate = posts_per_day / (account_age_days / 30)  # Posts per month
                patterns['activity_rate'] = activity_rate
                
                if activity_rate > 1000:  # Extremely high activity rate
                    bot_score += 30
                    indicators.append("Unusually high activity rate for account age")
            
            # Engagement pattern analysis
            avg_engagement = user_data.get('avg_engagement_rate', 0.05)
            patterns['engagement_rate'] = avg_engagement
            
            if avg_engagement < 0.005:  # Very low engagement
                bot_score += 20
                indicators.append("Extremely low engagement rate")
            elif avg_engagement > 0.8:  # Suspiciously high engagement
                bot_score += 15
                indicators.append("Suspiciously high engagement rate")
            
        except Exception as e:
            logger.debug(f"Behavioral pattern analysis error: {e}")
        
        return {
            'bot_score': min(100, bot_score),
            'indicators': indicators,
            'patterns': patterns
        }
    
    def _analyze_temporal_patterns_bot(self, user_data: Dict[str, Any], 
                                     posts: List[str]) -> Dict[str, Any]:
        """Analyze temporal patterns for bot detection"""
        indicators = []
        patterns = {}
        bot_score = 0.0
        
        try:
            # Posting time consistency
            posting_hours = user_data.get('posting_hours', [])
            if posting_hours and len(posting_hours) > 5:
                hour_variance = np.var(posting_hours)
                patterns['posting_hour_variance'] = hour_variance
                
                if hour_variance < 1:  # Very consistent posting times
                    bot_score += 25
                    indicators.append("Unnaturally consistent posting times")
                elif hour_variance < 3:
                    bot_score += 15
                    indicators.append("Somewhat consistent posting times")
            
            # Activity pattern analysis
            if 'activity_pattern' in user_data:
                activity_24h = user_data['activity_pattern']
                if len(activity_24h) == 24:
                    # Check for inhuman patterns (24/7 activity)
                    active_hours = sum(1 for activity in activity_24h if activity > 0)
                    patterns['active_hours_per_day'] = active_hours
                    
                    if active_hours > 20:  # Active more than 20 hours a day
                        bot_score += 35
                        indicators.append("Inhuman activity pattern (24/7 posting)")
                    elif active_hours > 16:
                        bot_score += 20
                        indicators.append("Suspicious activity pattern")
            
            # Response time analysis
            avg_response_time = user_data.get('avg_response_time_seconds', 300)
            patterns['avg_response_time'] = avg_response_time
            
            if avg_response_time < 10:  # Extremely fast responses
                bot_score += 20
                indicators.append("Unnaturally fast response times")
            elif avg_response_time < 30:
                bot_score += 10
                indicators.append("Very fast response times")
            
        except Exception as e:
            logger.debug(f"Temporal pattern analysis error: {e}")
        
        return {
            'bot_score': min(100, bot_score),
            'indicators': indicators,
            'patterns': patterns
        }
    
    def _analyze_network_patterns(self, user_data: Dict[str, Any], 
                                network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network patterns for bot detection"""
        indicators = []
        patterns = {}
        bot_score = 0.0
        
        try:
            # Connection similarity analysis
            similar_connections = network_data.get('similar_connections', 0)
            total_connections = network_data.get('total_connections', 1)
            similarity_ratio = similar_connections / total_connections
            patterns['connection_similarity'] = similarity_ratio
            
            if similarity_ratio > 0.8:
                bot_score += 30
                indicators.append("Highly similar connection patterns")
            elif similarity_ratio > 0.6:
                bot_score += 20
                indicators.append("Similar connection patterns")
            
            # Clustering coefficient
            clustering_coeff = network_data.get('clustering_coefficient', 0)
            patterns['clustering_coefficient'] = clustering_coeff
            
            if clustering_coeff > 0.9:  # Very high clustering
                bot_score += 25
                indicators.append("Unnaturally high network clustering")
            
            # Coordinated behavior indicators
            if network_data.get('coordinated_following', False):
                bot_score += 30
                indicators.append("Coordinated following behavior detected")
            
            if network_data.get('simultaneous_account_creation', False):
                bot_score += 35
                indicators.append("Simultaneous account creation with similar accounts")
            
        except Exception as e:
            logger.debug(f"Network pattern analysis error: {e}")
        
        return {
            'bot_score': min(100, bot_score),
            'indicators': indicators,
            'patterns': patterns
        }
    
    def _analyze_content_patterns_bot(self, posts: List[str]) -> Dict[str, Any]:
        """Analyze content patterns specific to bot detection"""
        indicators = []
        bot_score = 0.0
        
        try:
            if not posts:
                return {'bot_score': 0, 'indicators': []}
            
            # URL sharing patterns
            urls_per_post = []
            for post in posts:
                url_count = len(re.findall(r'http[s]?://\S+', post))
                urls_per_post.append(url_count)
            
            if urls_per_post:
                avg_urls = np.mean(urls_per_post)
                if avg_urls > 2:  # Very high URL sharing
                    bot_score += 20
                    indicators.append("Excessive URL sharing (potential spam bot)")
            
            # Hashtag usage patterns
            hashtag_usage = []
            for post in posts:
                hashtag_count = len(re.findall(r'#\w+', post))
                hashtag_usage.append(hashtag_count)
            
            if hashtag_usage:
                avg_hashtags = np.mean(hashtag_usage)
                hashtag_variance = np.var(hashtag_usage)
                
                if avg_hashtags > 5 and hashtag_variance < 2:
                    bot_score += 15
                    indicators.append("Consistent excessive hashtag usage")
            
            # Mention patterns
            mention_patterns = []
            for post in posts:
                mention_count = len(re.findall(r'@\w+', post))
                mention_patterns.append(mention_count)
            
            if mention_patterns:
                avg_mentions = np.mean(mention_patterns)
                if avg_mentions > 3:
                    bot_score += 10
                    indicators.append("Excessive mention usage")
            
        except Exception as e:
            logger.debug(f"Content pattern analysis error: {e}")
        
        return {
            'bot_score': min(100, bot_score),
            'indicators': indicators
        }
    
    def _detect_template_patterns(self, posts: List[str]) -> Dict[str, Any]:
        """Detect if posts follow template patterns"""
        if len(posts) < 3:
            return {'is_template_based': False, 'confidence': 0.0, 'pattern_type': 'none'}
        
        try:
            # Extract structure patterns
            structures = []
            for post in posts:
                # Analyze structure: URLs, mentions, hashtags, etc.
                structure = {
                    'has_url': bool(re.search(r'http[s]?://\S+', post)),
                    'has_mention': bool(re.search(r'@\w+', post)),
                    'has_hashtag': bool(re.search(r'#\w+', post)),
                    'word_count': len(post.split()),
                    'sentence_count': len(re.split(r'[.!?]+', post))
                }
                structures.append(structure)
            
            # Check for consistent patterns
            pattern_consistency = 0
            total_checks = 0
            
            for key in structures[0].keys():
                if key in ['word_count', 'sentence_count']:
                    values = [s[key] for s in structures]
                    variance = np.var(values)
                    mean_val = np.mean(values)
                    cv = variance / mean_val if mean_val > 0 else 0
                    
                    if cv < 0.2:  # Low coefficient of variation
                        pattern_consistency += 1
                    total_checks += 1
                else:
                    # Boolean features
                    values = [s[key] for s in structures]
                    consistency = len(set(values)) == 1
                    if consistency:
                        pattern_consistency += 1
                    total_checks += 1
            
            confidence = pattern_consistency / total_checks if total_checks > 0 else 0
            
            is_template = confidence > 0.7
            pattern_type = 'template_based' if is_template else 'organic'
            
            return {
                'is_template_based': is_template,
                'confidence': confidence,
                'pattern_type': pattern_type
            }
            
        except Exception as e:
            logger.debug(f"Template pattern detection error: {e}")
            return {'is_template_based': False, 'confidence': 0.0, 'pattern_type': 'unknown'}
    
    def _analyze_emotional_consistency(self, posts: List[str]) -> float:
        """Analyze emotional consistency across posts"""
        if len(posts) < 3:
            return 0.5  # Neutral
        
        try:
            emotion_vectors = []
            for post in posts[:10]:  # Analyze first 10 posts
                sentiment = self.analyze_content_sentiment(post)
                emotion_vector = [
                    sentiment.emotion_scores.get('anger', 0),
                    sentiment.emotion_scores.get('joy', 0),
                    sentiment.emotion_scores.get('sadness', 0),
                    sentiment.emotion_scores.get('fear', 0)
                ]
                emotion_vectors.append(emotion_vector)
            
            if len(emotion_vectors) < 2:
                return 0.5
            
            # Calculate consistency using standard deviation
            emotion_arrays = np.array(emotion_vectors)
            consistency_scores = []
            
            for i in range(emotion_arrays.shape[1]):
                std_dev = np.std(emotion_arrays[:, i])
                consistency = 1 - min(std_dev, 1.0)  # Invert and cap
                consistency_scores.append(consistency)
            
            return np.mean(consistency_scores)
            
        except Exception as e:
            logger.debug(f"Emotional consistency analysis error: {e}")
            return 0.5
    
    def extract_entities(self, text: str) -> EntityResult:
        """
        Advanced named entity extraction with confidence scoring and relationships
        
        Args:
            text: Input text for entity extraction
            
        Returns:
            Enhanced EntityResult with detailed entity information
        """
        start_time = time.time()
        
        try:
            # Initialize entity containers
            persons = []
            organizations = []
            locations = []
            dates = []
            money = []
            phone_numbers = []
            email_addresses = []
            urls = []
            social_handles = []
            cryptocurrencies = []
            vehicles = []
            weapons = []
            drugs = []
            other_entities = defaultdict(list)
            entity_relationships = []
            confidence_scores = {}
            
            language_info = self.detect_language(text)
            primary_language = language_info['primary']
            
            # 1. SpaCy-based NER
            spacy_entities = self._extract_spacy_entities(text, primary_language)
            persons.extend(spacy_entities['persons'])
            organizations.extend(spacy_entities['organizations'])
            locations.extend(spacy_entities['locations'])
            dates.extend(spacy_entities['dates'])
            money.extend(spacy_entities['money'])
            other_entities.update(spacy_entities['other'])
            
            # 2. Pattern-based extraction
            pattern_entities = self._extract_pattern_entities(text)
            phone_numbers.extend(pattern_entities['phones'])
            email_addresses.extend(pattern_entities['emails'])
            urls.extend(pattern_entities['urls'])
            social_handles.extend(pattern_entities['social_handles'])
            cryptocurrencies.extend(pattern_entities['crypto'])
            vehicles.extend(pattern_entities['vehicles'])
            
            # 3. Domain-specific entity extraction
            domain_entities = self._extract_domain_entities(text)
            weapons.extend(domain_entities['weapons'])
            drugs.extend(domain_entities['drugs'])
            
            # 4. Relationship extraction
            entity_relationships = self._extract_entity_relationships(text, {
                'persons': persons,
                'organizations': organizations,
                'locations': locations
            })
            
            # 5. Calculate confidence scores
            confidence_scores = self._calculate_entity_confidence(text, {
                'persons': persons,
                'organizations': organizations,
                'locations': locations,
                'dates': dates,
                'money': money
            })
            
            # 6. Remove duplicates and normalize
            persons = self._normalize_entities(persons)
            organizations = self._normalize_entities(organizations)
            locations = self._normalize_entities(locations)
            dates = self._normalize_entities(dates)
            money = self._normalize_entities(money)
            
            # Remove duplicates from lists
            phone_numbers = list(set(phone_numbers))
            email_addresses = list(set(email_addresses))
            urls = list(set(urls))
            social_handles = list(set(social_handles))
            cryptocurrencies = list(set(cryptocurrencies))
            vehicles = list(set(vehicles))
            weapons = list(set(weapons))
            drugs = list(set(drugs))
            
            # Update processing stats
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, 'entity_extraction')
            
            return EntityResult(
                persons=persons,
                organizations=organizations,
                locations=locations,
                dates=dates,
                money=money,
                phone_numbers=phone_numbers,
                email_addresses=email_addresses,
                urls=urls,
                social_handles=social_handles,
                cryptocurrencies=cryptocurrencies,
                vehicles=vehicles,
                weapons=weapons,
                drugs=drugs,
                other_entities=dict(other_entities),
                entity_relationships=entity_relationships,
                confidence_scores=confidence_scores
            )
            
        except Exception as e:
            logger.error(f"Entity extraction error: {str(e)}")
            return EntityResult(
                persons=[], organizations=[], locations=[], dates=[], money=[],
                phone_numbers=[], email_addresses=[], urls=[], social_handles=[],
                cryptocurrencies=[], vehicles=[], weapons=[], drugs=[],
                other_entities={}, entity_relationships=[], confidence_scores={}
            )
    
    def _extract_spacy_entities(self, text: str, language: str) -> Dict[str, List]:
        """Extract entities using spaCy models"""
        entities = {
            'persons': [], 'organizations': [], 'locations': [],
            'dates': [], 'money': [], 'other': defaultdict(list)
        }
        
        try:
            # Choose appropriate model
            nlp_model = None
            if language == 'english' and nlp_en:
                nlp_model = nlp_en
            elif language == 'hindi' and nlp_hi:
                nlp_model = nlp_hi
            elif nlp_en:  # Fallback to English model
                nlp_model = nlp_en
            
            if nlp_model:
                doc = nlp_model(text[:1000000])  # Limit text length
                
                for ent in doc.ents:
                    entity_info = {
                        'text': ent.text,
                        'label': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'confidence': 0.8  # Default spaCy confidence
                    }
                    
                    if ent.label_ in ['PERSON', 'PER']:
                        entities['persons'].append(entity_info)
                    elif ent.label_ in ['ORG', 'ORGANIZATION']:
                        entities['organizations'].append(entity_info)
                    elif ent.label_ in ['GPE', 'LOC', 'LOCATION', 'PLACE']:
                        entities['locations'].append(entity_info)
                    elif ent.label_ in ['DATE', 'TIME']:
                        entities['dates'].append(entity_info)
                    elif ent.label_ in ['MONEY', 'MONETARY']:
                        entities['money'].append(entity_info)
                    else:
                        entities['other'][ent.label_].append(entity_info)
        
        except Exception as e:
            logger.debug(f"spaCy entity extraction error: {e}")
        
        return entities
    
    def _extract_pattern_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using regex patterns"""
        entities = {
            'phones': [], 'emails': [], 'urls': [], 'social_handles': [],
            'crypto': [], 'vehicles': []
        }
        
        try:
            for pattern_name, pattern in self.entity_patterns.items():
                matches = re.findall(pattern, text, re.IGNORECASE)
                
                if pattern_name == 'indian_phone':
                    entities['phones'].extend(matches)
                elif pattern_name == 'email':
                    entities['emails'].extend(matches)
                elif pattern_name == 'url':
                    entities['urls'].extend(matches)
                elif pattern_name == 'social_handle':
                    entities['social_handles'].extend(matches)
                elif pattern_name in ['bitcoin', 'ethereum']:
                    entities['crypto'].extend(matches)
                elif pattern_name == 'vehicle_number':
                    entities['vehicles'].extend(matches)
        
        except Exception as e:
            logger.debug(f"Pattern entity extraction error: {e}")
        
        return entities
    
    def _extract_domain_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract domain-specific entities (weapons, drugs, etc.)"""
        entities = {'weapons': [], 'drugs': []}
        
        try:
            text_lower = text.lower()
            
            # Weapon detection
            weapon_keywords = []
            for category in ['weapons', 'violence']:
                if category in self.threat_keywords:
                    if isinstance(self.threat_keywords[category], dict):
                        for subcategory in self.threat_keywords[category].values():
                            weapon_keywords.extend(subcategory)
                    else:
                        weapon_keywords.extend(self.threat_keywords[category])
            
            for keyword in weapon_keywords:
                if keyword.lower() in text_lower:
                    entities['weapons'].append(keyword)
            
            # Drug detection
            drug_keywords = []
            if 'drugs' in self.threat_keywords:
                if isinstance(self.threat_keywords['drugs'], dict):
                    for subcategory in self.threat_keywords['drugs'].values():
                        drug_keywords.extend(subcategory)
                else:
                    drug_keywords.extend(self.threat_keywords['drugs'])
            
            for keyword in drug_keywords:
                if keyword.lower() in text_lower:
                    entities['drugs'].append(keyword)
        
        except Exception as e:
            logger.debug(f"Domain entity extraction error: {e}")
        
        return entities
    
    def _extract_entity_relationships(self, text: str, entities: Dict[str, List]) -> List[Dict[str, Any]]:
        """Extract relationships between entities"""
        relationships = []
        
        try:
            # Simple relationship patterns
            relationship_patterns = [
                (r'(\w+)\s+(?:works for|employed by|member of)\s+(\w+)', 'EMPLOYED_BY'),
                (r'(\w+)\s+(?:met|spoke with|contacted)\s+(\w+)', 'CONTACTED'),
                (r'(\w+)\s+(?:lives in|located in|from)\s+(\w+)', 'LOCATED_IN'),
                (r'(\w+)\s+(?:owns|possesses|has)\s+(\w+)', 'OWNS'),
                (r'(\w+)\s+(?:and|with)\s+(\w+)', 'ASSOCIATED_WITH')
            ]
            
            for pattern, relation_type in relationship_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        relationships.append({
                            'entity1': match[0],
                            'entity2': match[1],
                            'relationship': relation_type,
                            'confidence': 0.6
                        })
        
        except Exception as e:
            logger.debug(f"Relationship extraction error: {e}")
        
        return relationships
    
    def _calculate_entity_confidence(self, text: str, entities: Dict[str, List]) -> Dict[str, float]:
        """Calculate confidence scores for extracted entities"""
        confidence_scores = {}
        
        try:
            for entity_type, entity_list in entities.items():
                if entity_list:
                    # Simple confidence based on context and frequency
                    total_confidence = 0
                    for entity in entity_list:
                        entity_text = entity.get('text', entity) if isinstance(entity, dict) else entity
                        
                        # Context-based confidence
                        context_confidence = 0.5  # Base confidence
                        
                        # Increase confidence for proper nouns (capitalized)
                        if entity_text and entity_text[0].isupper():
                            context_confidence += 0.2
                        
                        # Increase confidence for longer entities
                        if len(entity_text.split()) > 1:
                            context_confidence += 0.1
                        
                        # Increase confidence for multiple occurrences
                        occurrences = text.lower().count(entity_text.lower())
                        if occurrences > 1:
                            context_confidence += min(0.2, occurrences * 0.05)
                        
                        total_confidence += min(1.0, context_confidence)
                    
                    confidence_scores[entity_type] = total_confidence / len(entity_list)
        
        except Exception as e:
            logger.debug(f"Entity confidence calculation error: {e}")
        
        return confidence_scores
    
    def _normalize_entities(self, entities: List) -> List[Dict[str, Any]]:
        """Normalize and deduplicate entities"""
        if not entities:
            return []
        
        try:
            normalized = []
            seen_texts = set()
            
            for entity in entities:
                if isinstance(entity, dict):
                    entity_text = entity.get('text', '').strip()
                    if entity_text and entity_text.lower() not in seen_texts:
                        seen_texts.add(entity_text.lower())
                        normalized.append(entity)
                elif isinstance(entity, str):
                    entity_text = entity.strip()
                    if entity_text and entity_text.lower() not in seen_texts:
                        seen_texts.add(entity_text.lower())
                        normalized.append({
                            'text': entity_text,
                            'confidence': 0.7
                        })
            
            return normalized
        
        except Exception as e:
            logger.debug(f"Entity normalization error: {e}")
            return entities if isinstance(entities, list) else []
    
    def detect_coordination(self, posts: List[Dict[str, Any]]) -> CoordinationResult:
        """
        Advanced coordination detection with sophisticated pattern analysis
        """
        try:
            # Import and use the advanced functions
            from .nlp_engine_advanced import AdvancedNLPFunctions
            advanced_functions = AdvancedNLPFunctions(self)
            return advanced_functions.detect_coordination(posts, advanced_analysis=True)
        except Exception as e:
            logger.error(f"Coordination detection error: {str(e)}")
            return CoordinationResult(
                similarity_score=0.0, is_coordinated=False, confidence=0.0,
                similar_patterns=[], coordination_indicators=[],
                coordination_type='ERROR', network_size_estimate=1,
                coordination_sophistication='UNKNOWN', campaign_indicators={},
                temporal_coordination={}, content_coordination={},
                behavioral_coordination={}
            )
    
    def classify_threat_type(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
        Advanced threat classification with multi-model analysis
        
        Args:
            text: Content to classify
            metadata: Additional context information
            
        Returns:
            Detailed threat classification
        """
        try:
            text_lower = text.lower()
            threat_scores = {}
            context_scores = {}
            
            # Enhanced threat scoring with context analysis
            for category, subcategories in self.threat_keywords.items():
                score = 0
                context_weight = 1.0
                
                if isinstance(subcategories, dict):
                    for priority, keywords in subcategories.items():
                        weight = {'high_priority': 3, 'medium_priority': 2, 'context_dependent': 1}.get(priority, 1)
                        
                        for keyword in keywords:
                            if keyword.lower() in text_lower:
                                # Context analysis for keywords
                                context_multiplier = self._analyze_keyword_context(text, keyword)
                                score += weight * context_multiplier
                else:
                    # Backward compatibility
                    for keyword in subcategories:
                        if keyword.lower() in text_lower:
                            score += 1
                
                threat_scores[category] = score
                
                # Apply domain-specific context weights
                if category == 'terrorism' and metadata:
                    if metadata.get('location', '').lower() in ['afghanistan', 'pakistan', 'syria']:
                        context_weight = 1.5
                elif category == 'cybercrime' and 'bitcoin' in text_lower:
                    context_weight = 1.3
                
                context_scores[category] = score * context_weight
            
            # Advanced classification using ML if available
            ml_classification = self._classify_with_ml(text) if self.ml_models else None
            
            # Determine primary threat
            if not context_scores or max(context_scores.values()) == 0:
                return "No Threat Detected"
            
            primary_threat = max(context_scores, key=context_scores.get)
            secondary_threats = [cat for cat, score in context_scores.items() 
                               if score > 0 and cat != primary_threat]
            
            # Enhanced threat mapping with severity
            threat_classifications = {
                'terrorism': {
                    'high': 'Critical Terrorism Threat',
                    'medium': 'Potential Terrorism Activity',
                    'low': 'Terrorism-Related Content'
                },
                'anti_national': {
                    'high': 'Confirmed Anti-National Activity',
                    'medium': 'Suspected Anti-National Content',
                    'low': 'Anti-National Indicators'
                },
                'violence': {
                    'high': 'Imminent Violence Threat',
                    'medium': 'Violence Incitement',
                    'low': 'Violence-Related Content'
                },
                'hate_speech': {
                    'high': 'Severe Hate Speech',
                    'medium': 'Discriminatory Content',
                    'low': 'Prejudicial Language'
                },
                'cybercrime': {
                    'high': 'Active Cybercrime',
                    'medium': 'Cybercrime Planning',
                    'low': 'Cybercrime References'
                },
                'drugs': {
                    'high': 'Drug Trafficking Activity',
                    'medium': 'Drug Distribution Content',
                    'low': 'Drug-Related Discussion'
                },
                'radicalization': {
                    'high': 'Active Radicalization',
                    'medium': 'Radicalization Content',
                    'low': 'Extremist Ideology'
                }
            }
            
            # Determine severity based on score
            primary_score = context_scores[primary_threat]
            if primary_score >= 8:
                severity = 'high'
            elif primary_score >= 4:
                severity = 'medium'
            else:
                severity = 'low'
            
            classification = threat_classifications.get(primary_threat, {}).get(
                severity, f"Unclassified {primary_threat.title()} Threat"
            )
            
            # Add secondary threat information
            if secondary_threats:
                classification += f" (Secondary: {', '.join(secondary_threats[:2])})"
            
            # Add ML classification if available
            if ml_classification and ml_classification != 'unknown':
                classification += f" [ML: {ml_classification}]"
            
            return classification
            
        except Exception as e:
            logger.error(f"Threat classification error: {str(e)}")
            return "Classification Error"
    
    def _classify_with_ml(self, text: str) -> str:
        """Classify threat using machine learning models"""
        try:
            if not self.ml_models or not sklearn_available:
                return 'unknown'
            
            # This would use pre-trained models in production
            # For now, implement a simple heuristic-based classifier
            
            text_lower = text.lower()
            
            # Simple rule-based classification for demonstration
            if any(word in text_lower for word in ['bomb', 'attack', 'terror', 'isis']):
                return 'terrorism_ml'
            elif any(word in text_lower for word in ['hack', 'phishing', 'fraud']):
                return 'cybercrime_ml'
            elif any(word in text_lower for word in ['kill', 'murder', 'violence']):
                return 'violence_ml'
            else:
                return 'unknown'
                
        except Exception as e:
            logger.debug(f"ML classification error: {e}")
            return 'unknown'
    
    def _analyze_keyword_context(self, text: str, keyword: str) -> float:
        """Analyze the context around a keyword to determine relevance"""
        try:
            keyword_lower = keyword.lower()
            text_lower = text.lower()
            
            # Find keyword positions
            positions = []
            start = 0
            while True:
                pos = text_lower.find(keyword_lower, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if not positions:
                return 0.0
            
            context_scores = []
            
            for pos in positions:
                # Extract context window (50 characters before and after)
                start_pos = max(0, pos - 50)
                end_pos = min(len(text), pos + len(keyword) + 50)
                context = text_lower[start_pos:end_pos]
                
                # Analyze context for amplifying or diminishing factors
                score = 1.0  # Base score
                
                # Amplifying contexts
                amplifiers = ['urgent', 'immediate', 'now', 'today', 'tonight', 'plan', 'ready']
                diminishers = ['not', 'never', 'fake', 'joke', 'movie', 'game', 'story']
                
                for amplifier in amplifiers:
                    if amplifier in context:
                        score += 0.2
                
                for diminisher in diminishers:
                    if diminisher in context:
                        score -= 0.3
                
                # Question vs statement context
                if '?' in context:
                    score *= 0.7  # Questions are less threatening than statements
                
                # Exclamation marks increase intensity
                if '!' in context:
                    score *= 1.2
                
                context_scores.append(max(0.0, min(2.0, score)))  # Cap between 0 and 2
            
            return np.mean(context_scores) if context_scores else 1.0
            
        except Exception as e:
            logger.debug(f"Context analysis error: {e}")
            return 1.0
    
    def _analyze_emotions(self, text: str, language: str) -> Dict[str, float]:
        """Analyze emotions in text using lexicon-based approach"""
        try:
            emotion_scores = {
                'anger': 0.0, 'fear': 0.0, 'joy': 0.0,
                'sadness': 0.0, 'disgust': 0.0, 'surprise': 0.0
            }
            
            # Get appropriate emotion lexicon
            lexicon = self.emotion_lexicon.get(language, self.emotion_lexicon.get('english', {}))
            
            if not lexicon:
                return emotion_scores
            
            text_words = text.lower().split()
            word_count = len(text_words)
            
            if word_count == 0:
                return emotion_scores
            
            # Count emotion words
            emotion_counts = {emotion: 0 for emotion in emotion_scores.keys()}
            
            for emotion, words in lexicon.items():
                for word in words:
                    emotion_counts[emotion] += text.lower().count(word)
            
            # Normalize by text length
            for emotion in emotion_scores.keys():
                emotion_scores[emotion] = min(1.0, emotion_counts[emotion] / word_count * 10)
            
            return emotion_scores
            
        except Exception as e:
            logger.debug(f"Emotion analysis error: {e}")
            return {emotion: 0.0 for emotion in ['anger', 'fear', 'joy', 'sadness', 'disgust', 'surprise']}
    
    def _analyze_cultural_context(self, text: str, language: str) -> Dict[str, Any]:
        """Analyze cultural context and cultural sensitivity"""
        try:
            context = {'cultural_markers': [], 'sensitivity_score': 0.0, 'regional_indicators': []}
            
            indian_context = self.cultural_context_db.get('indian_context', {})
            
            text_lower = text.lower()
            
            # Check for cultural markers
            for category, markers in indian_context.items():
                found_markers = [marker for marker in markers if marker.lower() in text_lower]
                if found_markers:
                    context['cultural_markers'].extend(found_markers)
            
            # Check for regional language indicators
            for lang, words in self.cultural_context_db.get('regional_languages', {}).items():
                found_words = [word for word in words if word in text]
                if found_words:
                    context['regional_indicators'].append({
                        'language': lang,
                        'words': found_words
                    })
            
            # Calculate cultural sensitivity score
            sensitive_terms = ['religion', 'caste', 'community', 'minority', 'majority']
            sensitivity_count = sum(1 for term in sensitive_terms if term in text_lower)
            context['sensitivity_score'] = min(1.0, sensitivity_count / 5)
            
            return context
            
        except Exception as e:
            logger.debug(f"Cultural context analysis error: {e}")
            return {'cultural_markers': [], 'sensitivity_score': 0.0, 'regional_indicators': []}
    
    def _detect_cultural_context_flags(self, text: str, cultural_context: Dict[str, Any]) -> List[str]:
        """Detect cultural context flags that might indicate issues"""
        flags = []
        
        try:
            if cultural_context.get('sensitivity_score', 0) > 0.6:
                flags.append('High cultural sensitivity detected')
            
            cultural_markers = cultural_context.get('cultural_markers', [])
            if len(cultural_markers) > 3:
                flags.append('Multiple cultural references detected')
            
            # Check for potentially divisive cultural content
            divisive_patterns = [
                r'hindu vs muslim', r'majority vs minority', r'upper caste', r'lower caste'
            ]
            
            for pattern in divisive_patterns:
                if re.search(pattern, text.lower()):
                    flags.append(f'Divisive cultural pattern: {pattern}')
            
        except Exception as e:
            logger.debug(f"Cultural flag detection error: {e}")
        
        return flags
    
    def _analyze_metadata_risk(self, metadata: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Analyze metadata for risk indicators"""
        risk_data = {'score': 0, 'evidence': [], 'network_indicators': []}
        
        try:
            # Account age risk
            account_age = metadata.get('account_age_days', 365)
            if account_age < 7:
                risk_data['score'] += 20
                risk_data['evidence'].append('Very new account (high risk)')
            elif account_age < 30:
                risk_data['score'] += 10
                risk_data['evidence'].append('New account')
            
            # Activity pattern risk
            posts_per_day = metadata.get('posts_per_day', 1)
            if posts_per_day > 100:
                risk_data['score'] += 25
                risk_data['evidence'].append('Extremely high posting frequency')
            elif posts_per_day > 50:
                risk_data['score'] += 15
                risk_data['evidence'].append('High posting frequency')
            
            # Network risk indicators
            followers = metadata.get('followers', 0)
            following = metadata.get('following', 0)
            
            if following > 0:
                ratio = followers / following
                if ratio < 0.1:
                    risk_data['score'] += 15
                    risk_data['network_indicators'].append('Low follower ratio')
            
            # Geographic risk
            location = metadata.get('location', '').lower()
            high_risk_locations = ['afghanistan', 'pakistan', 'syria', 'iraq']
            if any(loc in location for loc in high_risk_locations):
                risk_data['score'] += 20
                risk_data['evidence'].append(f'High-risk geographic location: {location}')
            
            # Analysis-specific metadata risk
            if analysis_type == 'anti_national':
                # Check for VPN usage, proxy, etc.
                if metadata.get('using_vpn', False):
                    risk_data['score'] += 10
                    risk_data['evidence'].append('VPN usage detected')
                
                if metadata.get('anonymous_posting', False):
                    risk_data['score'] += 15
                    risk_data['evidence'].append('Anonymous posting pattern')
            
        except Exception as e:
            logger.debug(f"Metadata risk analysis error: {e}")
        
        return risk_data
    
    def _analyze_temporal_patterns(self, text: str, timestamp: Any) -> Dict[str, Any]:
        """Analyze temporal patterns for risk assessment"""
        result = {'suspicious': False, 'score': 0, 'indicators': [], 'evidence': []}
        
        try:
            if not timestamp:
                return result
            
            # Convert timestamp if needed
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    return result
            elif not isinstance(timestamp, datetime):
                return result
            
            current_time = datetime.now(timestamp.tzinfo) if timestamp.tzinfo else datetime.now()
            
            # Check posting time
            hour = timestamp.hour
            if 2 <= hour <= 5:  # Very late night/early morning
                result['score'] += 8
                result['indicators'].append('suspicious_timing')
                result['evidence'].append(f'Posted at suspicious hour: {hour:02d}:xx')
                result['suspicious'] = True
            
            # Check for proximity to major events (simplified)
            # In production, this would check against a database of major events
            day_of_week = timestamp.weekday()
            if day_of_week in [4, 5, 6]:  # Friday, Saturday, Sunday
                # Weekend posting might be more suspicious for certain content types
                if any(word in text.lower() for word in ['attack', 'bomb', 'riot']):
                    result['score'] += 5
                    result['indicators'].append('weekend_threat_posting')
            
            # Check recency
            time_diff = current_time - timestamp
            if time_diff.total_seconds() < 3600:  # Posted within last hour
                result['score'] += 3
                result['indicators'].append('recent_posting')
        
        except Exception as e:
            logger.debug(f"Temporal pattern analysis error: {e}")
        
        return result
    
    def _update_processing_stats(self, processing_time: float, operation: str):
        """Update processing statistics"""
        try:
            with self.thread_lock:
                self.processing_stats['total_processed'] += 1
                
                # Update average processing time
                current_avg = self.processing_stats['avg_processing_time']
                total_processed = self.processing_stats['total_processed']
                
                new_avg = ((current_avg * (total_processed - 1)) + processing_time) / total_processed
                self.processing_stats['avg_processing_time'] = new_avg
                
                # Update model usage
                self.processing_stats['model_usage'][operation] += 1
        
        except Exception as e:
            logger.debug(f"Stats update error: {e}")
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Enhanced text similarity calculation"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Tokenize and normalize
            words1 = set(word.lower().strip() for word in text1.split())
            words2 = set(word.lower().strip() for word in text2.split())
            
            if not words1 or not words2:
                return 0.0
            
            # Jaccard similarity
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            jaccard = len(intersection) / len(union) if union else 0.0
            
            # Character-level similarity for better matching
            char_similarity = 0.0
            if len(text1) > 10 and len(text2) > 10:
                # Use character n-grams
                def get_char_ngrams(text, n=3):
                    text = text.lower().replace(' ', '')
                    return set(text[i:i+n] for i in range(len(text)-n+1))
                
                ngrams1 = get_char_ngrams(text1)
                ngrams2 = get_char_ngrams(text2)
                
                if ngrams1 and ngrams2:
                    char_intersection = ngrams1.intersection(ngrams2)
                    char_union = ngrams1.union(ngrams2)
                    char_similarity = len(char_intersection) / len(char_union)
            
            # Combine similarities
            combined_similarity = (jaccard * 0.7) + (char_similarity * 0.3)
            
            return combined_similarity
            
        except Exception as e:
            logger.debug(f"Text similarity calculation error: {e}")
            return 0.0
    
    def generate_evidence_summary(self, content: str, analysis_results: Dict[str, Any] = None,
                                case_id: str = None) -> EvidenceSummary:
        """
        Generate comprehensive evidence summary in police report format
        
        Args:
            content: Original content being analyzed
            analysis_results: Results from various NLP analyses (optional - will run analysis if not provided)
            case_id: Optional case identifier
            
        Returns:
            Enhanced EvidenceSummary formatted for police reports
        """
        try:
            if not case_id:
                case_id = f"CYBER_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(content[:100].encode()).hexdigest()[:8]}"
            
            # If no analysis results provided, run basic analysis
            if analysis_results is None:
                logger.info("No analysis results provided, running comprehensive analysis...")
                analysis_results = self.comprehensive_analysis(content)
            
            # Extract and enhance analysis results
            sentiment = analysis_results.get('sentiment', {})
            threat_analysis = analysis_results.get('threat_analysis', {})
            entities = analysis_results.get('entities', {})
            bot_analysis = analysis_results.get('bot_analysis', {})
            coordination = analysis_results.get('coordination', {})
            risk_score = analysis_results.get('risk_score', 0)
            
            # Enhanced threat level determination
            threat_level = self._determine_enhanced_threat_level(
                risk_score, threat_analysis, bot_analysis, coordination
            )
            
            # Generate executive summary
            summary = self._generate_executive_summary(
                case_id, threat_level, risk_score, content, analysis_results
            )
            
            # Generate detailed analysis
            detailed_analysis = self._generate_detailed_analysis_report(
                content, sentiment, threat_analysis, entities, bot_analysis, 
                coordination, risk_score
            )
            
            # Compile comprehensive evidence points
            evidence_points = self._compile_evidence_points(
                threat_analysis, bot_analysis, entities, coordination, sentiment
            )
            
            # Generate actionable recommendations
            recommended_actions = self._generate_enhanced_recommendations(
                threat_level, risk_score, threat_analysis, bot_analysis
            )
            
            # Enhanced technical details
            technical_details = self._generate_technical_details(
                content, sentiment, entities, analysis_results
            )
            
            # Generate intelligence insights
            intelligence_insights = self._generate_intelligence_insights(
                content, analysis_results, threat_level
            )
            
            # Legal implications assessment
            legal_implications = self._assess_enhanced_legal_implications(
                threat_analysis, risk_score, entities, content
            )
            
            # Chain of custody and forensic markers
            chain_of_custody = self._generate_chain_of_custody(case_id, content)
            forensic_markers = self._extract_forensic_markers(content, entities)
            
            # Correlation data for connecting with other cases
            correlation_data = self._generate_correlation_data(
                entities, threat_analysis, sentiment
            )
            
            # Expert analysis summary
            expert_analysis = self._generate_expert_analysis(
                analysis_results, threat_level, risk_score
            )
            
            # Risk assessment matrix
            risk_assessment = self._generate_risk_assessment_matrix(
                risk_score, threat_analysis, bot_analysis, coordination
            )
            
            return EvidenceSummary(
                case_id=case_id,
                timestamp=datetime.now(),
                threat_level=threat_level,
                summary=summary,
                detailed_analysis=detailed_analysis,
                evidence_points=evidence_points,
                recommended_actions=recommended_actions,
                technical_details=technical_details,
                legal_implications=legal_implications,
                intelligence_insights=intelligence_insights,
                chain_of_custody=chain_of_custody,
                forensic_markers=forensic_markers,
                correlation_data=correlation_data,
                expert_analysis=expert_analysis,
                risk_assessment=risk_assessment
            )
            
        except Exception as e:
            logger.error(f"Evidence summary generation error: {str(e)}")
            return self._generate_error_evidence_summary(case_id, str(e))
    
    def analyze_with_openai(self, content: str, analysis_type: str = "comprehensive", 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhanced OpenAI integration for advanced content analysis
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis to perform
            context: Additional context for analysis
            
        Returns:
            Enhanced analysis results with confidence scoring
        """
        if not self.openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            context = context or {}
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Enhanced prompts for different analysis types
            system_prompts = {
                "comprehensive": """You are an expert cybersecurity analyst and threat intelligence specialist for law enforcement. 
                Analyze content for security threats, terrorism, anti-national activities, hate speech, cybercrime, and radicalization.
                Provide detailed, actionable intelligence suitable for police investigations.""",
                
                "threat_detection": """You are a specialized threat detection expert for law enforcement cybersecurity units.
                Focus specifically on identifying terrorism, violence, anti-national activities, and imminent threats.
                Rate threat levels and provide specific evidence.""",
                
                "bot_detection": """You are an expert in detecting automated accounts, bot networks, and coordinated inauthentic behavior.
                Analyze linguistic patterns, behavioral indicators, and coordination signs.
                Determine likelihood of automated or coordinated behavior.""",
                
                "intelligence_assessment": """You are a senior intelligence analyst specializing in digital forensics and threat assessment.
                Provide strategic intelligence insights, threat actor profiling, and operational recommendations."""
            }
            
            user_prompts = {
                "comprehensive": f"""
                Analyze this content comprehensively for law enforcement intelligence:
                
                Content: {content[:3000]}
                
                Additional Context: {json.dumps(context) if context else 'None'}
                
                Provide analysis including:
                1. Threat Assessment (0-100 scale with justification)
                2. Threat Classification (terrorism, violence, hate speech, cybercrime, etc.)
                3. Key Evidence Points (specific quotes and indicators)
                4. Urgency Level (LOW/MEDIUM/HIGH/CRITICAL)
                5. Recommended Actions (immediate and follow-up)
                6. Intelligence Value (actionable insights)
                7. Legal Considerations (relevant laws and evidence requirements)
                8. Network Analysis (connections, coordination indicators)
                
                Format as structured analysis suitable for police reports.
                """,
                
                "threat_detection": f"""
                Conduct specialized threat detection analysis:
                
                Content: {content[:3000]}
                
                Focus on:
                1. Imminent Threat Indicators (specific threats, timing, targets)
                2. Threat Actor Assessment (individual vs group, sophistication)
                3. Attack Vector Analysis (methods, capabilities, resources)
                4. Escalation Potential (likelihood of action)
                5. Geographic/Temporal Factors (location references, timing)
                6. Evidence Quality (strength of indicators)
                
                Provide threat score (0-100) and specific action recommendations.
                """,
                
                "bot_detection": f"""
                Analyze for automated behavior and coordination:
                
                Content: {content[:3000]}
                
                Evaluate:
                1. Linguistic Authenticity (natural vs artificial language patterns)
                2. Content Patterns (repetition, templates, variations)
                3. Coordination Indicators (timing, similarity, networks)
                4. Bot Sophistication Level (simple spam vs advanced AI)
                5. Purpose Assessment (spam, propaganda, disinformation)
                6. Network Scale Estimation (size of coordinated operation)
                
                Provide bot probability (0-100) and evidence.
                """,
                
                "intelligence_assessment": f"""
                Provide strategic intelligence assessment:
                
                Content: {content[:3000]}
                Context: {json.dumps(context) if context else 'None'}
                
                Deliver:
                1. Strategic Threat Assessment (broader implications)
                2. Actor Profiling (motivations, capabilities, connections)
                3. Operational Intelligence (actionable insights for operations)
                4. Trend Analysis (patterns, escalation, evolution)
                5. Countermeasure Recommendations (prevention, mitigation)
                6. Intelligence Gaps (additional information needed)
                
                Focus on high-level strategic insights for decision makers.
                """
            }
            
            system_prompt = system_prompts.get(analysis_type, system_prompts["comprehensive"])
            user_prompt = user_prompts.get(analysis_type, user_prompts["comprehensive"])
            
            payload = {
                "model": "gpt-4" if analysis_type == "intelligence_assessment" else "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.2,  # Low temperature for consistent, factual analysis
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']
                
                # Parse and structure the response
                structured_analysis = self._parse_openai_response(analysis, analysis_type)
                
                return {
                    "success": True,
                    "analysis_type": analysis_type,
                    "raw_analysis": analysis,
                    "structured_analysis": structured_analysis,
                    "usage": result.get('usage', {}),
                    "model": payload["model"],
                    "confidence": self._assess_openai_confidence(analysis),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_detail = response.text if response.status_code != 429 else "Rate limit exceeded"
                return {
                    "error": f"OpenAI API error: {response.status_code}",
                    "details": error_detail,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"OpenAI analysis error: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def comprehensive_analysis(self, content: str, metadata: Dict[str, Any] = None,
                             user_posts: List[str] = None, context_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis using all advanced NLP functions
        
        Args:
            content: Primary content to analyze
            metadata: Additional metadata about user/content
            user_posts: List of recent posts from the same user
            context_data: Additional contextual information
            
        Returns:
            Complete analysis results with enhanced insights
        """
        start_time = time.time()
        
        try:
            metadata = metadata or {}
            user_posts = user_posts or [content]
            context_data = context_data or {}
            
            results = {
                'analysis_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'engine_version': '2.0.0',
                    'analysis_id': hashlib.md5(f"{content[:100]}{datetime.now().isoformat()}".encode()).hexdigest()
                }
            }
            
            # Core content analysis
            logger.info("Starting sentiment analysis...")
            results['sentiment'] = asdict(self.analyze_content_sentiment(content))
            
            logger.info("Starting entity extraction...")
            results['entities'] = asdict(self.extract_entities(content))
            
            logger.info("Starting risk score calculation...")
            results['risk_score'] = self.calculate_risk_score(content, metadata, context_data)
            
            logger.info("Starting threat classification...")
            results['threat_type'] = self.classify_threat_type(content, metadata)
            
            # Advanced threat analysis
            logger.info("Starting anti-national content detection...")
            results['threat_analysis'] = asdict(self.detect_anti_national_content(content, metadata))
            
            # Bot analysis if user data available
            if metadata:
                logger.info("Starting bot behavior analysis...")
                results['bot_analysis'] = asdict(self.identify_bot_behavior(metadata, user_posts))
            
            # Coordination analysis if multiple posts
            if len(user_posts) > 1:
                logger.info("Starting coordination detection...")
                post_data = [{'content': post, 'metadata': metadata} for post in user_posts]
                results['coordination'] = asdict(self.detect_coordination(post_data))
            
            # OpenAI analysis if available and enabled
            if self.openai_api_key and context_data.get('use_openai', False):
                logger.info("Starting OpenAI analysis...")
                openai_context = {
                    'metadata': metadata,
                    'risk_score': results['risk_score'],
                    'threat_type': results['threat_type']
                }
                results['openai_analysis'] = self.analyze_with_openai(
                    content, "comprehensive", openai_context
                )
            
            # Generate comprehensive evidence summary
            logger.info("Generating evidence summary...")
            results['evidence_summary'] = asdict(
                self.generate_evidence_summary(content, results)
            )
            
            # Overall assessment
            logger.info("Generating overall assessment...")
            results['overall_assessment'] = self._generate_overall_assessment(results)
            
            # Performance metrics
            processing_time = time.time() - start_time
            results['performance_metrics'] = {
                'total_processing_time': processing_time,
                'processing_speed': len(content) / processing_time if processing_time > 0 else 0,
                'cache_usage': self._get_cache_stats(),
                'model_usage': dict(self.processing_stats['model_usage'])
            }
            
            # Update global stats
            self._update_processing_stats(processing_time, 'comprehensive_analysis')
            
            logger.info(f"Comprehensive analysis completed in {processing_time:.2f} seconds")
            
            return results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {str(e)}")
            return {
                "error": str(e),
                "partial_results": results if 'results' in locals() else {},
                "timestamp": datetime.now().isoformat()
            }
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get comprehensive analysis statistics and performance metrics"""
        try:
            with self.thread_lock:
                stats = {
                    'processing_statistics': dict(self.processing_stats),
                    'cache_statistics': self._get_cache_stats(),
                    'model_availability': {
                        'nltk_available': self.sentiment_analyzer is not None,
                        'spacy_english_available': nlp_en is not None,
                        'spacy_hindi_available': nlp_hi is not None,
                        'transformers_available': sentiment_pipeline is not None,
                        'sklearn_available': sklearn_available,
                        'openai_available': self.openai_api_key is not None
                    },
                    'threat_keywords_loaded': len(self.threat_keywords),
                    'patterns_loaded': len(self.anti_national_patterns),
                    'emotion_lexicon_size': sum(len(words) for words in self.emotion_lexicon.get('english', {}).values()),
                    'cultural_context_loaded': len(self.cultural_context_db),
                    'timestamp': datetime.now().isoformat()
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Statistics generation error: {str(e)}")
            return {"error": str(e)}
    
    def _get_cache_stats(self) -> Dict[str, Any]:
        """Get cache usage statistics"""
        try:
            return {
                'content_cache_size': len(self.content_cache),
                'entity_cache_size': len(self.entity_cache),
                'model_cache_size': len(self.model_cache),
                'cache_hits': self.processing_stats.get('cache_hits', 0),
                'cache_hit_ratio': self.processing_stats.get('cache_hits', 0) / max(1, self.processing_stats.get('total_processed', 1))
            }
        except Exception:
            return {"error": "Cache stats unavailable"}
    
    # Helper methods
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using simple methods"""
        try:
            # Simple word-based similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except:
            return 0.0
    
    def _analyze_profile_for_bot_signs(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user profile for bot indicators"""
        score = 0
        indicators = []
        patterns = {}
        
        # Generic usernames
        username = user_data.get('username', '').lower()
        if re.match(r'^user\d+$', username) or re.match(r'^[a-z]+\d{4,}$', username):
            score += 15
            indicators.append("Generic username pattern")
        
        # Profile completeness
        profile_fields = ['bio', 'profile_image', 'location', 'website']
        missing_fields = sum(1 for field in profile_fields if not user_data.get(field))
        if missing_fields >= 3:
            score += 10
            indicators.append("Incomplete profile")
        
        patterns['profile_completeness'] = 1 - (missing_fields / len(profile_fields))
        
        # Account age
        account_age_days = user_data.get('account_age_days', 365)
        if account_age_days < 7:
            score += 20
            indicators.append("Very new account")
        elif account_age_days < 30:
            score += 10
            indicators.append("New account")
        
        patterns['account_age'] = account_age_days
        
        return {'score': score, 'indicators': indicators, 'patterns': patterns}
    
    def _analyze_timing_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timing patterns for bot behavior"""
        score = 0
        indicators = []
        patterns = {}
        
        # Posting times (if available)
        posting_hours = user_data.get('posting_hours', [])
        if posting_hours:
            hour_variance = np.var(posting_hours) if len(posting_hours) > 1 else 0
            if hour_variance < 2:  # Very consistent posting times
                score += 15
                indicators.append("Suspiciously consistent posting times")
            
            patterns['posting_time_variance'] = hour_variance
        
        return {'score': score, 'indicators': indicators, 'patterns': patterns}
    
    def _analyze_user_behavior_similarity(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze similarity in user behavior patterns"""
        coordination_score = 0.0
        patterns = []
        
        # Extract user info from posts
        users = [post.get('user_id', post.get('author', '')) for post in posts]
        unique_users = set(users)
        
        if len(unique_users) > 1:
            # Check for similar account characteristics
            account_ages = []
            follower_counts = []
            
            for post in posts:
                metadata = post.get('metadata', {})
                if metadata.get('account_age_days'):
                    account_ages.append(metadata['account_age_days'])
                if metadata.get('followers'):
                    follower_counts.append(metadata['followers'])
            
            # Similar account ages
            if len(account_ages) > 1:
                age_std = np.std(account_ages)
                age_mean = np.mean(account_ages)
                if age_std < age_mean * 0.1:  # Very similar ages
                    coordination_score += 0.3
                    patterns.append("Similar account ages")
            
            # Similar follower counts
            if len(follower_counts) > 1:
                follower_std = np.std(follower_counts)
                follower_mean = np.mean(follower_counts)
                if follower_std < follower_mean * 0.2:  # Very similar follower counts
                    coordination_score += 0.2
                    patterns.append("Similar follower counts")
        
        return {'coordination_score': coordination_score, 'patterns': patterns}
    
    def _generate_threat_explanation(self, threat_type: str, keywords: List[str],
                                   evidence: List[str], risk_score: float) -> str:
        """Generate explanation for threat detection"""
        if risk_score < 20:
            return f"Low risk content with minimal {threat_type} indicators."
        elif risk_score < 40:
            return f"Moderate {threat_type} content detected with keywords: {', '.join(keywords[:3])}"
        elif risk_score < 60:
            return f"High risk {threat_type} content with multiple threat indicators."
        else:
            return f"Critical {threat_type} threat detected with severe risk indicators requiring immediate attention."
    
    def _generate_detailed_analysis(self, content: str, sentiment: Dict, threat_analysis: Dict,
                                  entities: Dict, bot_analysis: Dict, risk_score: float) -> str:
        """Generate detailed analysis section for evidence summary"""
        analysis = []
        
        analysis.append("CONTENT ANALYSIS:")
        analysis.append(f"- Content length: {len(content)} characters")
        analysis.append(f"- Language: {sentiment.get('language', 'Unknown')}")
        analysis.append(f"- Sentiment: {sentiment.get('label', 'neutral')} (confidence: {sentiment.get('confidence', 0):.2f})")
        
        analysis.append("\nTHREAT ASSESSMENT:")
        analysis.append(f"- Risk score: {risk_score}/100")
        analysis.append(f"- Threat type: {threat_analysis.get('threat_type', 'Unknown')}")
        analysis.append(f"- Severity: {threat_analysis.get('severity', 'Unknown')}")
        
        if entities.get('persons'):
            analysis.append(f"\nENTITIES IDENTIFIED:")
            analysis.append(f"- Persons: {', '.join(entities['persons'][:5])}")
        
        if entities.get('locations'):
            analysis.append(f"- Locations: {', '.join(entities['locations'][:5])}")
        
        if bot_analysis.get('bot_score', 0) > 30:
            analysis.append(f"\nBOT ANALYSIS:")
            analysis.append(f"- Bot likelihood: {bot_analysis['bot_score']:.1f}%")
            analysis.append(f"- Key indicators: {', '.join(bot_analysis.get('indicators', [])[:3])}")
        
        return '\n'.join(analysis)
    
    def _generate_recommended_actions(self, risk_score: float, threat_analysis: Dict) -> List[str]:
        """Generate recommended actions based on analysis"""
        actions = []
        
        if risk_score >= 80:
            actions.extend([
                "IMMEDIATE ESCALATION: Notify senior officers and cybercrime unit",
                "Evidence preservation: Secure all digital evidence",
                "Legal review: Consult with legal team for potential charges",
                "Investigation: Launch comprehensive investigation"
            ])
        elif risk_score >= 60:
            actions.extend([
                "Enhanced monitoring: Increase surveillance of subject",
                "Evidence collection: Gather additional digital evidence",
                "Risk assessment: Evaluate potential for escalation",
                "Coordination: Share intelligence with relevant units"
            ])
        elif risk_score >= 40:
            actions.extend([
                "Continued monitoring: Maintain surveillance",
                "Documentation: Record all activities and communications",
                "Analysis: Conduct deeper behavioral analysis"
            ])
        else:
            actions.extend([
                "Routine monitoring: Include in regular surveillance",
                "Documentation: Log for future reference"
            ])
        
        return actions
    
    def _assess_legal_implications(self, threat_analysis: Dict, risk_score: float) -> str:
        """Assess legal implications of the analysis"""
        if risk_score >= 80:
            return """
            HIGH LEGAL RISK: Content may violate multiple sections of Indian Penal Code including:
            - Section 153A (Promoting enmity between groups)
            - Section 295A (Deliberate insult to religion)
            - Section 124A (Sedition)
            - IT Act Section 66A (Offensive content)
            Recommend immediate legal consultation and evidence preservation.
            """
        elif risk_score >= 60:
            return """
            MODERATE LEGAL RISK: Content may violate:
            - IT Act provisions on offensive content
            - Possible hate speech violations
            Recommend legal review and continued monitoring.
            """
        elif risk_score >= 40:
            return """
            LOW LEGAL RISK: Content requires monitoring but may not constitute
            immediate legal violations. Document for future reference.
            """
        else:
            return "MINIMAL LEGAL RISK: No immediate legal concerns identified."
    
    def _generate_overall_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment summary"""
        risk_score = results.get('risk_score', 0)
        threat_analysis = results.get('threat_analysis', {})
        bot_analysis = results.get('bot_analysis', {})
        
        assessment = {
            'overall_risk': 'CRITICAL' if risk_score >= 80 else
                          'HIGH' if risk_score >= 60 else
                          'MEDIUM' if risk_score >= 40 else
                          'LOW',
            'primary_concerns': [],
            'confidence': 0.0,
            'requires_action': risk_score >= 40
        }
        
        if threat_analysis.get('risk_score', 0) > 50:
            assessment['primary_concerns'].append('Security threat detected')
        
        if bot_analysis.get('bot_score', 0) > 60:
            assessment['primary_concerns'].append('Automated behavior detected')
        
        # Calculate overall confidence
        confidences = []
        if threat_analysis.get('confidence'):
            confidences.append(threat_analysis['confidence'])
        if bot_analysis.get('confidence'):
            confidences.append(bot_analysis['confidence'])
        
        assessment['confidence'] = np.mean(confidences) if confidences else 0.5
        
        return assessment
    
    def _determine_enhanced_threat_level(self, risk_score: float, threat_analysis: Dict, 
                                       bot_analysis: Dict, coordination: Dict) -> str:
        """Determine enhanced threat level with multiple factors"""
        base_level = "MINIMAL"
        
        if risk_score >= 90:
            base_level = "CRITICAL"
        elif risk_score >= 75:
            base_level = "HIGH"
        elif risk_score >= 50:
            base_level = "MEDIUM"
        elif risk_score >= 25:
            base_level = "LOW"
        
        # Amplification factors
        amplifiers = 0
        
        if threat_analysis.get('severity') == 'CRITICAL':
            amplifiers += 1
        
        if bot_analysis.get('automation_level') in ['HIGH', 'CRITICAL']:
            amplifiers += 1
        
        if coordination.get('is_coordinated') and coordination.get('coordination_sophistication') == 'HIGHLY_SOPHISTICATED':
            amplifiers += 1
        
        # Upgrade threat level based on amplifiers
        if amplifiers >= 2 and base_level in ['LOW', 'MEDIUM']:
            if base_level == 'LOW':
                base_level = 'MEDIUM'
            elif base_level == 'MEDIUM':
                base_level = 'HIGH'
        elif amplifiers >= 1 and base_level == 'MINIMAL':
            base_level = 'LOW'
        
        return base_level
    
    def _generate_error_evidence_summary(self, case_id: str, error_msg: str) -> EvidenceSummary:
        """Generate error evidence summary"""
        return EvidenceSummary(
            case_id=case_id or f"ERROR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            threat_level="UNKNOWN",
            summary=f"Analysis Error: {error_msg}",
            detailed_analysis="Analysis could not be completed due to system error.",
            evidence_points=[f"Error: {error_msg}"],
            recommended_actions=["Review system logs", "Retry analysis", "Manual review required"],
            technical_details={"error": error_msg, "timestamp": datetime.now().isoformat()},
            legal_implications="Unable to assess due to analysis error.",
            intelligence_insights=[],
            chain_of_custody=[],
            forensic_markers={},
            correlation_data={},
            expert_analysis={},
            risk_assessment={}
        )
