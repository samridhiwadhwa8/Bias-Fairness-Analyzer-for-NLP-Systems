"""
Kaggle Suggester Module - Phase 6
Structural archetype-based dataset suggestions, not name-based.
"""

from typing import Dict, Any, List


class KaggleSuggester:
    """Suggests Kaggle datasets based on structural archetypes."""
    
    def __init__(self):
        # Archetype mappings based on structure, not specific datasets
        self.archetypes = {
            "nlp_classification_medium": [
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
                },
                {
                    "name": "Yelp Reviews Polarity",
                    "domain": "reviews",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/yelp-dataset",
                    "bias_risk": "medium", 
                    "description": "Business reviews with sentiment labels",
                    "advantages": ["Real-world data", "Multi-class", "Well-studied"]
                }
            ],
            "tabular_classification_medium": [
                {
                    "name": "Credit Card Fraud Detection",
                    "domain": "finance",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud",
                    "bias_risk": "high",
                    "description": "European credit card transactions with fraud labels",
                    "advantages": ["Real financial data", "Imbalanced challenge", "Standard benchmark"]
                },
                {
                    "name": "Home Credit Default Risk",
                    "domain": "finance",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/kamilpytl/home-credit-default-risk",
                    "bias_risk": "high",
                    "description": "Loan default prediction with demographic features",
                    "advantages": ["Real-world impact", "Comprehensive features", "Regulatory relevance"]
                },
                {
                    "name": "IBM HR Analytics Employee Attrition",
                    "domain": "hr",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/pavansubhr/employee-attrition",
                    "bias_risk": "high",
                    "description": "Employee attrition with workforce demographics",
                    "advantages": ["HR domain focus", "Demographic features", "Business impact"]
                }
            ],
            "tabular_classification_small": [
                {
                    "name": "Loan Eligibility Prediction",
                    "domain": "finance",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/wordsforhuman/loan-eligibility-prediction",
                    "bias_risk": "medium",
                    "description": "Loan approval prediction with customer demographics",
                    "advantages": ["Smaller scale", "Manageable complexity", "Financial domain"]
                },
                {
                    "name": "Heart Disease Prediction",
                    "domain": "health",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/redwankar/heart-disease-prediction",
                    "bias_risk": "medium",
                    "description": "Cardiovascular disease prediction with clinical features",
                    "advantages": ["Healthcare impact", "Clinical features", "Manageable size"]
                }
            ],
            "tabular_regression_medium": [
                {
                    "name": "US Census Income Dataset",
                    "domain": "government",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/ucml/adult-census-income",
                    "bias_risk": "medium",
                    "description": "Adult census income prediction with demographic features",
                    "advantages": ["Well-documented", "Standard benchmark", "Real-world demographics"]
                },
                {
                    "name": "Student Performance Prediction",
                    "domain": "education",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/datasets/laurabernaldo/student-performance-prediction",
                    "bias_risk": "low",
                    "description": "Student academic performance with demographic factors",
                    "advantages": ["Educational impact", "Lower bias risk", "Well-structured"]
                }
            ]
        }
    
    def suggest(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest datasets based on structural archetype.
        """
        print(f"DEBUG KAGGLE: Received profile type: {type(profile)}")
        print(f"DEBUG KAGGLE: Profile value: {profile}")
        
        if not isinstance(profile, dict):
            print(f"DEBUG KAGGLE: ERROR: Profile is not a dict, it's {type(profile)}")
            raise ValueError(f"KaggleSuggester expects dict profile, got {type(profile)}")
        
        dataset_type = profile.get("dataset_type", "tabular")
        task = profile.get("task", "unknown")
        size = profile.get("size", "medium")
        
        # Build archetype key
        archetype_key = f"{dataset_type}_{task}_{size}"
        
        # Get matching archetypes
        exact_matches = self.archetypes.get(archetype_key, [])
        
        # Fallback to broader categories
        if not exact_matches:
            broader_key = f"{dataset_type}_{task}"
            for key, datasets in self.archetypes.items():
                if broader_key in key:
                    exact_matches = datasets
                    break
        
        # Fallback to domain-specific
        if not exact_matches:
            domain = profile.get("domain", "general")
            for key, datasets in self.archetypes.items():
                for dataset in datasets:
                    if dataset.get("domain") == domain:
                        exact_matches.append(dataset)
        
        return exact_matches[:3]  # Return top 3 matches
