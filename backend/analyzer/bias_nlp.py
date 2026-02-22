"""
NLP Bias Analysis Module
Detects linguistic bias in text datasets.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, Any, List, Optional
from collections import Counter


class NLPBiasAnalyzer:
    """Analyzes bias in NLP/text datasets."""
    
    def __init__(self):
        # Toxic words patterns
        self.toxic_patterns = [
            r'\b(hate|kill|stupid|idiot|dumb|ugly|disgusting|worthless)\b',
            r'\b(bitch|bastard|asshole|moron|retard)\b',
            r'\b(terrorist|criminal|thief|liar|cheat)\b'
        ]
        
        # Gender pronouns
        self.male_pronouns = ['he', 'him', 'his', 'himself']
        self.female_pronouns = ['she', 'her', 'hers', 'herself']
        
        # Sentiment words
        self.positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'best', 'love', 'perfect', 'awesome']
        self.negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'disgusting', 'disappointing', 'poor', 'fail']
    
    def analyze_bias(self, df: pd.DataFrame, text_col: str, target_col: str, 
                    demographic_cols: List[tuple]) -> Dict[str, Any]:
        """
        Perform comprehensive NLP bias analysis.
        
        Args:
            df: Input DataFrame
            text_col: Text column name
            target_col: Target column name
            demographic_cols: List of demographic column tuples
            
        Returns:
            Dictionary with bias analysis results
        """
        print(f"Performing NLP bias analysis on text column: {text_col}")
        
        # Extract text data
        texts = df[text_col].fillna('').astype(str)
        
        # Calculate individual bias components
        toxicity_score = self._detect_toxicity(texts)
        gender_pronoun_score = self._analyze_gender_pronouns(texts)
        sentiment_score = self._analyze_sentiment(texts, df, target_col)
        
        # Calculate overall linguistic bias score
        linguistic_score = (toxicity_score + gender_pronoun_score + sentiment_score) / 3
        
        # Additional NLP-specific metrics
        text_complexity = self._analyze_text_complexity(texts)
        word_diversity = self._analyze_word_diversity(texts)
        
        return {
            'bias_type': 'NLP Linguistic Bias',
            'linguistic_score': round(linguistic_score, 3),
            'toxicity_score': round(toxicity_score, 3),
            'gender_pronoun_score': round(gender_pronoun_score, 3),
            'sentiment_score': round(sentiment_score, 3),
            'text_complexity': text_complexity,
            'word_diversity': word_diversity,
            'demographic_columns_found': len(demographic_cols),
            'analysis_details': {
                'toxic_words_detected': self._get_toxic_words_count(texts),
                'pronoun_imbalance': self._get_pronoun_imbalance(texts),
                'sentiment_gap': self._get_sentiment_gap(texts, df, target_col)
            }
        }
    
    def _detect_toxicity(self, texts: pd.Series) -> float:
        """Detect toxic language in text."""
        toxic_count = 0
        total_texts = len(texts)
        
        for text in texts:
            text_lower = text.lower()
            for pattern in self.toxic_patterns:
                matches = re.findall(pattern, text_lower)
                toxic_count += len(matches)
        
        # Normalize by total texts
        toxicity_rate = toxic_count / total_texts if total_texts > 0 else 0
        return min(toxicity_rate, 1.0)  # Cap at 1.0
    
    def _analyze_gender_pronouns(self, texts: pd.Series) -> float:
        """Analyze gender pronoun imbalance."""
        male_count = 0
        female_count = 0
        
        for text in texts:
            text_lower = text.lower()
            words = text_lower.split()
            
            male_count += sum(1 for word in words if word in self.male_pronouns)
            female_count += sum(1 for word in words if word in self.female_pronouns)
        
        total_pronouns = male_count + female_count
        if total_pronouns == 0:
            return 0.0
        
        # Calculate imbalance (0 = balanced, 1 = completely imbalanced)
        imbalance = abs(male_count - female_count) / total_pronouns
        return imbalance
    
    def _analyze_sentiment(self, texts: pd.Series, df: pd.DataFrame, target_col: str) -> float:
        """Analyze sentiment bias across target classes."""
        if target_col not in df.columns:
            return 0.0
        
        sentiment_by_class = {}
        
        for class_val in df[target_col].unique():
            class_mask = df[target_col] == class_val
            class_texts = texts[class_mask]
            
            positive_count = 0
            negative_count = 0
            
            for text in class_texts:
                text_lower = text.lower()
                words = text_lower.split()
                
                positive_count += sum(1 for word in words if word in self.positive_words)
                negative_count += sum(1 for word in words if word in self.negative_words)
            
            total_sentiment = positive_count + negative_count
            if total_sentiment > 0:
                sentiment_ratio = positive_count / total_sentiment
                sentiment_by_class[class_val] = sentiment_ratio
            else:
                sentiment_by_class[class_val] = 0.5  # Neutral
        
        # Calculate sentiment gap between classes
        if len(sentiment_by_class) < 2:
            return 0.0
        
        sentiments = list(sentiment_by_class.values())
        sentiment_gap = max(sentiments) - min(sentiments)
        
        return sentiment_gap
    
    def _analyze_text_complexity(self, texts: pd.Series) -> Dict[str, float]:
        """Analyze text complexity metrics."""
        avg_sentence_length = []
        avg_word_length = []
        
        for text in texts:
            sentences = text.split('.')
            words = text.split()
            
            if sentences:
                avg_sentence_length.append(len(words) / len(sentences))
            if words:
                avg_word_length.append(np.mean([len(word) for word in words]))
        
        return {
            'avg_sentence_length': round(np.mean(avg_sentence_length), 2) if avg_sentence_length else 0,
            'avg_word_length': round(np.mean(avg_word_length), 2) if avg_word_length else 0,
            'complexity_score': round(np.mean(avg_sentence_length) / 20, 3) if avg_sentence_length else 0  # Normalized
        }
    
    def _analyze_word_diversity(self, texts: pd.Series) -> Dict[str, float]:
        """Analyze word diversity (unique words / total words)."""
        all_words = []
        for text in texts:
            words = text.lower().split()
            all_words.extend(words)
        
        if not all_words:
            return {'diversity_score': 0.0, 'unique_words': 0, 'total_words': 0}
        
        unique_words = len(set(all_words))
        total_words = len(all_words)
        diversity_score = unique_words / total_words
        
        return {
            'diversity_score': round(diversity_score, 3),
            'unique_words': unique_words,
            'total_words': total_words
        }
    
    def _get_toxic_words_count(self, texts: pd.Series) -> Dict[str, int]:
        """Get count of toxic words by category."""
        toxic_counts = {
            'hate_speech': 0,
            'profanity': 0,
            'insults': 0
        }
        
        for text in texts:
            text_lower = text.lower()
            
            # Hate speech
            toxic_counts['hate_speech'] += len(re.findall(r'\b(hate|kill|terrorist)\b', text_lower))
            
            # Profanity
            toxic_counts['profanity'] += len(re.findall(r'\b(bitch|bastard|asshole)\b', text_lower))
            
            # Insults
            toxic_counts['insults'] += len(re.findall(r'\b(stupid|idiot|dumb|moron|retard)\b', text_lower))
        
        return toxic_counts
    
    def _get_pronoun_imbalance(self, texts: pd.Series) -> Dict[str, Any]:
        """Get detailed pronoun imbalance analysis."""
        male_count = 0
        female_count = 0
        
        for text in texts:
            text_lower = text.lower()
            words = text_lower.split()
            
            male_count += sum(1 for word in words if word in self.male_pronouns)
            female_count += sum(1 for word in words if word in self.female_pronouns)
        
        total = male_count + female_count
        
        return {
            'male_pronouns': male_count,
            'female_pronouns': female_count,
            'total_pronouns': total,
            'male_percentage': round(male_count / total * 100, 1) if total > 0 else 0,
            'female_percentage': round(female_count / total * 100, 1) if total > 0 else 0,
            'imbalance_ratio': round(male_count / female_count, 2) if female_count > 0 else float('inf')
        }
    
    def _get_sentiment_gap(self, texts: pd.Series, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """Get detailed sentiment gap analysis."""
        if target_col not in df.columns:
            return {}
        
        sentiment_by_class = {}
        
        for class_val in df[target_col].unique():
            class_mask = df[target_col] == class_val
            class_texts = texts[class_mask]
            
            positive_count = 0
            negative_count = 0
            
            for text in class_texts:
                text_lower = text.lower()
                words = text_lower.split()
                
                positive_count += sum(1 for word in words if word in self.positive_words)
                negative_count += sum(1 for word in words if word in self.negative_words)
            
            total_sentiment = positive_count + negative_count
            sentiment_by_class[str(class_val)] = {
                'positive_words': positive_count,
                'negative_words': negative_count,
                'total_sentiment_words': total_sentiment,
                'positive_ratio': round(positive_count / total_sentiment, 3) if total_sentiment > 0 else 0.5
            }
        
        return sentiment_by_class
