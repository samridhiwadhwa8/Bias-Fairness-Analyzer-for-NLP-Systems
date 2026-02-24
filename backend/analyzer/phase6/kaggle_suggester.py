"""
Kaggle Suggester - Phase 6
Dataset archetype matching and alternative suggestions.
"""

from typing import Dict, List, Any


class KaggleSuggester:
    """Dataset archetype matching and suggestion engine."""
    
    ARCHETYPES = {
        "med-cls-T-MI": [
            {"name": "Pima Indians Diabetes", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database"},
            {"name": "Heart Disease ", "domain": "medical", "url": "https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset"},
            {"name": "Breast Cancer Wisconsin", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data"}
        ],
        "med-cls-S-MI": [
            {"name": "Diabetes Dataset", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database"},
            {"name": "Stroke Prediction Dataset", "domain": "medical", "url": "https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset"},
            {"name": "Chronic Kidney Disease", "domain": "medical", "url": "https://www.kaggle.com/datasets/mansoordaku/ckdisease"}
        ],
        "med-cls-M-HI": [
            {"name": "Heart Failure Prediction", "domain": "medical", "url": "https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction"},
            {"name": "Liver Disease Dataset", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/liver-disease-analysis"},
            {"name": "Parkinson's Disease", "domain": "medical", "url": "https://www.kaggle.com/datasets/vikasukani/parkinsons-disease-data"}
        ],
        "soc-cls-M-MI": [
            {"name": "Sentiment140", "domain": "social_media", "url": "https://www.kaggle.com/datasets/kazanova/sentiment140"},
            {"name": "Twitter Hate Speech", "domain": "social_media", "url": "https://www.kaggle.com/datasets/vsmaya/hate-speech-and-offensive-language"},
            {"name": "Toxic Comment Classification", "domain": "social_media", "url": "https://www.kaggle.com/datasets/julian3833/jigsaw-toxic-comment-classification-challenge"}
        ],
        "soc-cls-S-MI": [
            {"name": "Twitter Sentiment Analysis", "domain": "social_media", "url": "https://www.kaggle.com/datasets/crowdflower/twitter-sentiment-analysis"},
            {"name": "Reddit Comments", "domain": "social_media", "url": "https://www.kaggle.com/datasets/reddit/reddit-comments-may-2015"},
            {"name": "IMDB Movie Reviews", "domain": "social_media", "url": "https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"}
        ],
        "soc-cls-L-MI": [
            {"name": "Jigsaw Toxicity", "domain": "social_media", "url": "https://www.kaggle.com/datasets/julian3833/jigsaw-toxic-comment-classification-challenge"},
            {"name": "Wikipedia Toxic Comments", "domain": "social_media", "url": "https://www.kaggle.com/datasets/julian3833/jigsaw-toxic-comment-classification-challenge"},
            {"name": "Twitter Hate Speech", "domain": "social_media", "url": "https://www.kaggle.com/datasets/vsmaya/hate-speech-and-offensive-language"}
        ],
        "demo-cls-M-HI": [
            {"name": "Adult Census Income", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/adult-census-income"},
            {"name": "German Credit Data", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/german-credit"},
            {"name": "Taiwan Credit Default", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients"}
        ],
        "demo-cls-S-MI": [
            {"name": "UCI Adult", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/adult-census-income"},
            {"name": "Credit Risk Dataset", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/german-credit"},
            {"name": "Bank Marketing Dataset", "domain": "demographic", "url": "https://www.kaggle.com/datasets/henriqueyamahita/bank-marketing-dataset"}
        ],
        "demo-cls-L-HI": [
            {"name": "Home Credit Default Risk", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients"},
            {"name": "Bureau of Labor Statistics", "domain": "demographic", "url": "https://www.kaggle.com/datasets/paulbrabban/household-poverty-in-the-us"},
            {"name": "Adult Census Income", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/adult-census-income"}
        ],
        "fin-cls-M-HI": [
            {"name": "Default of Credit Card Clients", "domain": "financial", "url": "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients"},
            {"name": "Lending Club Loan Data", "domain": "financial", "url": "https://www.kaggle.com/datasets/wordsforthewise/lending-club-loan-data"},
            {"name": "Home Equity Dataset", "domain": "financial", "url": "https://www.kaggle.com/datasets/wordsforthewise/lending-club-loan-data"}
        ],
        "fin-cls-S-MI": [
            {"name": "Bank Marketing Dataset", "domain": "financial", "url": "https://www.kaggle.com/datasets/henriqueyamahita/bank-marketing-dataset"},
            {"name": "Credit Scoring", "domain": "financial", "url": "https://www.kaggle.com/datasets/uciml/german-credit"},
            {"name": "German Credit Data", "domain": "financial", "url": "https://www.kaggle.com/datasets/uciml/german-credit"}
        ],
        "gen-cls-M-MI": [
            {"name": "Wine Quality Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/wine-quality"},
            {"name": "Iris Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/iris"},
            {"name": "Breast Cancer Wisconsin", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin"}
        ],
        "gen-cls-S-B": [
            {"name": "Titanic Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/brendan4577/titanic-dataset"},
            {"name": "Heart Disease UCI", "domain": "general", "url": "https://www.kaggle.com/datasets/redwankar/song-data-heart-disease-uci"},
            {"name": "Wine Quality Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/wine-quality"}
        ],
        "gen-cls-L-B": [
            {"name": "Mushroom Classification", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/mushroom-classification"},
            {"name": "Banknote Authentication", "domain": "general", "url": "https://www.kaggle.com/datasets/riteshlchandra/banknote-authentication"},
            {"name": "Iris Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/iris"}
        ]
    }

    def suggest(self, fingerprint: str) -> List[Dict[str, Any]]:
        """
        Suggest alternative datasets based on fingerprint using layered matching.
        
        Args:
            fingerprint: Dataset fingerprint string
            
        Returns:
            List of alternative dataset suggestions (max 3)
        """
        parts = fingerprint.split('-')
        
        if len(parts) == 4:
            domain, task, size, balance = parts

            # Level 1: full match
            key_full = f"{domain}-{task}-{size}-{balance}"
            if key_full in self.ARCHETYPES:
                return self.ARCHETYPES[key_full][:3]

            # Level 2: ignore balance
            key_no_balance = f"{domain}-{task}-{size}"
            matches = [k for k in self.ARCHETYPES if k.startswith(key_no_balance)]
            if matches:
                return self.ARCHETYPES[matches[0]][:3]

            # Level 3: ignore size
            key_domain_task = f"{domain}-{task}"
            matches = [k for k in self.ARCHETYPES if k.startswith(key_domain_task)]
            if matches:
                return self.ARCHETYPES[matches[0]][:3]

            # Level 4: domain only
            matches = [k for k in self.ARCHETYPES if k.startswith(domain)]
            if matches:
                return self.ARCHETYPES[matches[0]][:3]

        # Fallback: domain-based suggestions
        if len(parts) >= 2:
            domain = parts[0]
            
            # Popular datasets by domain
            suggestions = []
            if domain == "med":
                suggestions = [
                    {"name": "Pima Indians Diabetes", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database"},
                    {"name": "Heart Disease UCI", "domain": "medical", "url": "https://www.kaggle.com/datasets/redwankar/song-data-heart-disease-uci"},
                    {"name": "Breast Cancer Wisconsin", "domain": "medical", "url": "https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin"}
                ]
            elif domain == "demo":
                suggestions = [
                    {"name": "Adult Census Income", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/adult-census-income"},
                    {"name": "German Credit Data", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/german-credit"},
                    {"name": "UCI Adult", "domain": "demographic", "url": "https://www.kaggle.com/datasets/uciml/adult-census-income"}
                ]
            elif domain == "fin":
                suggestions = [
                    {"name": "Default of Credit Card Clients", "domain": "financial", "url": "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients"},
                    {"name": "Lending Club Loan Data", "domain": "financial", "url": "https://www.kaggle.com/datasets/wordsforthewise/lending-club-loan-data"},
                    {"name": "Home Equity Dataset", "domain": "financial", "url": "https://www.kaggle.com/datasets/wordsforthewise/lending-club-loan-data"}
                ]
            elif domain == "soc":
                suggestions = [
                    {"name": "Sentiment140", "domain": "social_media", "url": "https://www.kaggle.com/datasets/kazanova/sentiment140"},
                    {"name": "Twitter Hate Speech", "domain": "social_media", "url": "https://www.kaggle.com/datasets/vsmaya/hate-speech-and-offensive-language"},
                    {"name": "IMDB Movie Reviews", "domain": "social_media", "url": "https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"}
                ]
            else:  # gen
                suggestions = [
                    {"name": "Iris Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/iris"},
                    {"name": "Wine Quality Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/uciml/wine-quality"},
                    {"name": "Titanic Dataset", "domain": "general", "url": "https://www.kaggle.com/datasets/brendan4577/titanic-dataset"}
                ]
            
            return suggestions[:3]  # Return max 3
        
        return []
