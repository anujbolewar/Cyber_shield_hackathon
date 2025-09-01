"""
Sentiment analysis utilities for social media monitoring
"""

import re
import random
from typing import Dict, List, Tuple

class SentimentAnalyzer:
    """Simple sentiment analysis class"""
    
    def __init__(self):
        # Positive words
        self.positive_words = {
            'amazing', 'awesome', 'excellent', 'fantastic', 'great', 'love', 'perfect',
            'wonderful', 'outstanding', 'brilliant', 'superb', 'incredible', 'magnificent',
            'spectacular', 'marvelous', 'exceptional', 'phenomenal', 'terrific', 'fabulous',
            'delightful', 'impressive', 'remarkable', 'splendid', 'beautiful', 'gorgeous',
            'lovely', 'charming', 'pleasant', 'enjoyable', 'satisfied', 'happy', 'pleased',
            'thrilled', 'excited', 'grateful', 'thankful', 'appreciate', 'recommend'
        }
        
        # Negative words
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'disgusting',
            'disappointing', 'frustrating', 'annoying', 'useless', 'pathetic', 'ridiculous',
            'absurd', 'outrageous', 'unacceptable', 'inadequate', 'inferior', 'defective',
            'broken', 'failed', 'failure', 'problem', 'issue', 'bug', 'error', 'glitch',
            'slow', 'expensive', 'overpriced', 'cheap', 'poor', 'low-quality', 'mediocre',
            'disappointed', 'frustrated', 'angry', 'upset', 'confused', 'concerned',
            'worried', 'skeptical', 'doubtful', 'suspicious', 'complain', 'complaint'
        }
        
        # Intensifiers
        self.intensifiers = {
            'very': 1.5, 'extremely': 2.0, 'incredibly': 2.0, 'absolutely': 1.8,
            'totally': 1.5, 'completely': 1.7, 'really': 1.3, 'quite': 1.2,
            'somewhat': 0.8, 'rather': 0.9, 'fairly': 0.9, 'slightly': 0.7,
            'super': 1.6, 'ultra': 1.8, 'mega': 1.7
        }
        
        # Negation words
        self.negations = {
            'not', 'no', 'never', 'none', 'nothing', 'nowhere', 'neither',
            'nobody', 'cannot', 'cant', 'could not', 'couldnt', 'will not',
            'wont', 'should not', 'shouldnt', 'do not', 'dont', 'does not',
            'doesnt', 'did not', 'didnt', 'is not', 'isnt', 'was not',
            'wasnt', 'are not', 'arent', 'were not', 'werent'
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of given text"""
        if not text:
            return {'score': 0.0, 'confidence': 0.0, 'category': 'Neutral'}
        
        # Clean and tokenize text
        cleaned_text = self._clean_text(text)
        tokens = self._tokenize(cleaned_text)
        
        # Calculate sentiment score
        score = self._calculate_sentiment_score(tokens)
        
        # Determine category
        category = self._categorize_sentiment(score)
        
        # Calculate confidence (simplified)
        confidence = min(abs(score), 1.0)
        
        return {
            'score': score,
            'confidence': confidence,
            'category': category
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions and hashtags (but keep the text)
        text = re.sub(r'[@#](\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    def _calculate_sentiment_score(self, tokens: List[str]) -> float:
        """Calculate sentiment score from tokens"""
        score = 0.0
        intensifier = 1.0
        negation = False
        
        for i, token in enumerate(tokens):
            # Check for intensifiers
            if token in self.intensifiers:
                intensifier = self.intensifiers[token]
                continue
            
            # Check for negations
            if token in self.negations:
                negation = True
                continue
            
            # Calculate base sentiment
            token_score = 0.0
            if token in self.positive_words:
                token_score = 1.0
            elif token in self.negative_words:
                token_score = -1.0
            
            # Apply modifiers
            if token_score != 0:
                token_score *= intensifier
                if negation:
                    token_score *= -1
                score += token_score
                
                # Reset modifiers
                intensifier = 1.0
                negation = False
        
        # Normalize score
        if len(tokens) > 0:
            score = score / len(tokens)
        
        # Clamp between -1 and 1
        score = max(-1.0, min(1.0, score))
        
        return score
    
    def _categorize_sentiment(self, score: float) -> str:
        """Categorize sentiment score"""
        if score > 0.2:
            return 'Positive'
        elif score < -0.2:
            return 'Negative'
        else:
            return 'Neutral'
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """Analyze sentiment for multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]
    
    def get_sentiment_distribution(self, texts: List[str]) -> Dict[str, int]:
        """Get sentiment distribution for a list of texts"""
        results = self.analyze_batch(texts)
        distribution = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        
        for result in results:
            category = result['category']
            distribution[category] += 1
        
        return distribution
    
    def get_average_sentiment(self, texts: List[str]) -> float:
        """Get average sentiment score for a list of texts"""
        if not texts:
            return 0.0
        
        results = self.analyze_batch(texts)
        scores = [result['score'] for result in results]
        
        return sum(scores) / len(scores)

def analyze_sentiment(text: str) -> Dict[str, float]:
    """Convenience function for sentiment analysis"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_sentiment(text)

def analyze_sentiment_trends(sentiment_scores: List[float], window_size: int = 5) -> List[float]:
    """Analyze sentiment trends using moving average"""
    if len(sentiment_scores) < window_size:
        return sentiment_scores
    
    trends = []
    for i in range(len(sentiment_scores) - window_size + 1):
        window = sentiment_scores[i:i + window_size]
        avg = sum(window) / len(window)
        trends.append(avg)
    
    return trends

def detect_sentiment_anomalies(sentiment_scores: List[float], threshold: float = 2.0) -> List[int]:
    """Detect sentiment anomalies using standard deviation"""
    if len(sentiment_scores) < 3:
        return []
    
    mean_score = sum(sentiment_scores) / len(sentiment_scores)
    variance = sum((x - mean_score) ** 2 for x in sentiment_scores) / len(sentiment_scores)
    std_dev = variance ** 0.5
    
    anomalies = []
    for i, score in enumerate(sentiment_scores):
        if abs(score - mean_score) > threshold * std_dev:
            anomalies.append(i)
    
    return anomalies

def classify_emotion(text: str) -> Dict[str, float]:
    """Classify emotions in text (simplified version)"""
    # Emotion keywords
    emotions = {
        'joy': ['happy', 'joy', 'excited', 'thrilled', 'delighted', 'cheerful', 'elated'],
        'anger': ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated'],
        'sadness': ['sad', 'depressed', 'disappointed', 'upset', 'down', 'blue', 'gloomy'],
        'fear': ['afraid', 'scared', 'worried', 'anxious', 'nervous', 'terrified', 'concerned'],
        'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'unexpected'],
        'disgust': ['disgusted', 'disgusting', 'revolting', 'repulsive', 'awful', 'terrible']
    }
    
    text_lower = text.lower()
    emotion_scores = {}
    
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[emotion] = score / len(keywords) if keywords else 0
    
    return emotion_scores

def get_sentiment_insights(sentiment_data: List[Dict[str, float]]) -> Dict[str, any]:
    """Generate insights from sentiment analysis results"""
    if not sentiment_data:
        return {}
    
    scores = [data['score'] for data in sentiment_data]
    categories = [data['category'] for data in sentiment_data]
    
    insights = {
        'total_analyzed': len(sentiment_data),
        'average_score': sum(scores) / len(scores),
        'score_range': max(scores) - min(scores),
        'positive_ratio': categories.count('Positive') / len(categories),
        'negative_ratio': categories.count('Negative') / len(categories),
        'neutral_ratio': categories.count('Neutral') / len(categories),
        'most_positive': max(scores),
        'most_negative': min(scores),
        'volatility': calculate_volatility(scores)
    }
    
    # Generate recommendations
    insights['recommendations'] = generate_sentiment_recommendations(insights)
    
    return insights

def calculate_volatility(scores: List[float]) -> float:
    """Calculate sentiment volatility (standard deviation)"""
    if len(scores) < 2:
        return 0.0
    
    mean = sum(scores) / len(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    return variance ** 0.5

def generate_sentiment_recommendations(insights: Dict[str, any]) -> List[str]:
    """Generate recommendations based on sentiment insights"""
    recommendations = []
    
    if insights['negative_ratio'] > 0.3:
        recommendations.append("High negative sentiment detected. Consider addressing customer concerns.")
    
    if insights['volatility'] > 0.5:
        recommendations.append("High sentiment volatility. Monitor for potential issues or opportunities.")
    
    if insights['positive_ratio'] > 0.7:
        recommendations.append("Strong positive sentiment. Consider amplifying successful strategies.")
    
    if insights['average_score'] < -0.2:
        recommendations.append("Overall negative sentiment. Immediate attention recommended.")
    
    if not recommendations:
        recommendations.append("Sentiment levels appear stable. Continue monitoring.")
    
    return recommendations

# Mock advanced sentiment analysis functions for demonstration
def advanced_sentiment_analysis(text: str) -> Dict[str, any]:
    """Advanced sentiment analysis with aspect-based sentiment"""
    # In a real implementation, this would use more sophisticated NLP
    base_analysis = analyze_sentiment(text)
    
    # Mock aspect-based sentiment
    aspects = {
        'product_quality': random.uniform(-1, 1),
        'customer_service': random.uniform(-1, 1),
        'price_value': random.uniform(-1, 1),
        'user_experience': random.uniform(-1, 1)
    }
    
    return {
        'overall': base_analysis,
        'aspects': aspects,
        'confidence': random.uniform(0.7, 0.95),
        'language': 'en',  # Mock language detection
        'subjectivity': random.uniform(0.3, 0.9)  # Mock subjectivity score
    }
