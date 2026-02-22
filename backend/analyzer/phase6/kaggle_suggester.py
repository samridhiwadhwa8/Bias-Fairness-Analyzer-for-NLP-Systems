"""
Kaggle Suggester Module - Phase 6
Structural archetype-based dataset suggestions, not name-based.
"""

from typing import Dict, Any, List


class KaggleSuggester:
    """Suggests Kaggle datasets based on structural archetypes."""
    
    def __init__(self):
        # Archetype mappings based on domain + structure, not just structure
        self.archetypes = {
            # Demographic datasets
            "demographic_tabular_classification_medium": [
                {
                    "name": "US Census Income Dataset",
                    "domain": "demographic",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/uciml/adult-census-income",
                    "bias_risk": "medium",
                    "description": "Adult census income prediction with demographic features",
                    "advantages": ["Real demographic data", "Well-studied", "Standard benchmark"]
                },
                {
                    "name": "Student Performance Prediction",
                    "domain": "education",
                    "source": "Kaggle", 
                    "url": "https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data",
                    "bias_risk": "medium",
                    "description": "Student academic performance with demographic factors",
                    "advantages": ["Educational focus", "Multi-dimensional", "Research validated"]
                }
            ],
            
            # Finance datasets
            "finance_tabular_classification_medium": [
                {
                    "name": "Credit Card Fraud Detection",
                    "domain": "finance",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud",
                    "bias_risk": "high",
                    "description": "Credit card transactions with fraud labels",
                    "advantages": ["Real financial data", "Imbalanced learning", "Industry relevant"]
                },
                {
                    "name": "Home Credit Default Risk",
                    "domain": "finance", 
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/c/home-credit-default-risk-prediction",
                    "bias_risk": "high",
                    "description": "Loan application data with default predictions",
                    "advantages": ["Large scale", "Real financial risk", "Comprehensive features"]
                }
            ],
            
            # HR datasets
            "hr_tabular_classification_medium": [
                {
                    "name": "HR Attrition Prediction",
                    "domain": "hr",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset",
                    "bias_risk": "medium",
                    "description": "Employee attrition with workplace demographics",
                    "advantages": ["HR focused", "Workplace demographics", "Business impact"]
                }
            ],
            
            # Health datasets
            "health_tabular_classification_medium": [
                {
                    "name": "Heart Disease Prediction",
                    "domain": "health",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/redwankar/heart-disease-prediction",
                    "bias_risk": "medium",
                    "description": "Cardiovascular disease prediction with clinical features",
                    "advantages": ["Medical focus", "Patient outcomes", "Clinical relevance"]
                }
            ],
            
            # Social media datasets
            "social_media_tabular_classification_medium": [
                {
                    "name": "Toxic Comment Classification Challenge",
                    "domain": "social_media",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge",
                    "bias_risk": "high",
                    "description": "Wikipedia comments with toxicity labels",
                    "advantages": ["Large scale", "Multi-class labels", "Community benchmarked"]
                }
            ],
            
            # Fallback structural archetypes (domain-agnostic)
            "tabular_classification_medium": [
                {
                    "name": "Titanic - Machine Learning from Disaster",
                    "domain": "general",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/c/titanic",
                    "bias_risk": "medium",
                    "description": "Classic classification problem with demographic features",
                    "advantages": ["Well-studied", "Educational", "Clean dataset"]
                }
            ],
            
            # NLP archetypes
            "social_media_nlp_classification_medium": [
                {
                    "name": "Toxic Comment Classification Challenge",
                    "domain": "social_media",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge",
                    "bias_risk": "high",
                    "description": "Wikipedia comments with toxicity labels",
                    "advantages": ["Large scale", "Multi-class labels", "Community benchmarked"]
                },
                {
                    "name": "Sentiment140 Dataset",
                    "domain": "social_media", 
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/kazanova/sentiment140",
                    "bias_risk": "medium",
                    "description": "Twitter sentiment with demographic annotations",
                    "advantages": ["Large scale", "Well-labeled", "Standard benchmark"]
                }
            ],
            
            "reviews_nlp_classification_medium": [
                {
                    "name": "Yelp Reviews Polarity",
                    "domain": "reviews",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/yelp-dataset",
                    "bias_risk": "medium", 
                    "description": "Customer reviews with sentiment labels",
                    "advantages": ["Real business data", "Multi-class", "Well-structured"]
                },
                {
                    "name": "Amazon Reviews",
                    "domain": "reviews",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews",
                    "bias_risk": "medium",
                    "description": "Product reviews with ratings and text",
                    "advantages": ["Large scale", "Real reviews", "Rating data"]
                }
            ],
            
            "general_nlp_classification_medium": [
                {
                    "name": "IMDB Movie Reviews",
                    "domain": "general_nlp",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews",
                    "bias_risk": "medium",
                    "description": "Movie reviews with sentiment labels",
                    "advantages": ["Classic benchmark", "Clean text", "Well-balanced"]
                }
            ]
        }
    
    def suggest(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest datasets based on domain + structural archetype.
        
        Args:
            profile: Dataset profile with domain, task, size, dataset_type
            
        Returns:
            List of similar dataset suggestions
        """
        print(f"DEBUG KAGGLE: Received profile type: {type(profile)}")
        print(f"DEBUG KAGGLE: Profile value: {profile}")
        
        if not isinstance(profile, dict):
            raise ValueError(f"KaggleSuggester expects dict profile, got {type(profile)}")
        
        # Extract profile components
        domain = profile.get("domain", "general")
        dataset_type = profile.get("dataset_type", "tabular")
        task = profile.get("task", "classification")
        size = profile.get("size", "medium")
        
        print(f"DEBUG KAGGLE: Extracted - domain: {domain}, type: {dataset_type}, task: {task}, size: {size}")
        
        # Try domain-specific archetype first
        full_key = f"{domain}_{dataset_type}_{task}_{size}"
        print(f"DEBUG KAGGLE: Trying domain-specific key: {full_key}")
        
        exact_matches = self.archetypes.get(full_key, [])
        
        if exact_matches:
            print(f"DEBUG KAGGLE: Found {len(exact_matches)} domain-specific matches")
            return exact_matches
        
        # Fallback to structural-only archetype
        fallback_key = f"{dataset_type}_{task}_{size}"
        print(f"DEBUG KAGGLE: Trying fallback key: {fallback_key}")
        
        fallback_matches = self.archetypes.get(fallback_key, [])
        
        if fallback_matches:
            print(f"DEBUG KAGGLE: Found {len(fallback_matches)} fallback matches")
            return fallback_matches
        
        print("DEBUG KAGGLE: No matches found, returning empty list")
        return []
