"""
Risk Assessment Engine
Calculates weighted risk scores using universal aggregation logic.
"""

from typing import Dict, Any, List


class RiskEngine:
    """Calculates overall risk scores using consistent weighted aggregation."""
    
    def __init__(self):
        # Universal weight dictionaries
        self.NLP_WEIGHTS = {
            "linguistic": 0.40,
            "toxicity": 0.30,
            "sentiment": 0.20,
            "class_imbalance": 0.10
        }
        
        self.TABULAR_WEIGHTS = {
            "demographic": 0.60,
            "class_imbalance": 0.40
        }
        
        # Universal risk level thresholds
        self.RISK_THRESHOLDS = {
            "low": 40,
            "moderate": 70,
            "high": 100
        }
    
    def _normalize_class_imbalance(self, ratio: float) -> float:
        """
        Normalize class imbalance ratio to 0-1 range for risk calculation.
        
        Args:
            ratio: Class imbalance ratio (max_class_count / min_class_count)
            
        Returns:
            Normalized score between 0-1
        """
        if ratio <= 1.0:
            return 0.0  # Perfectly balanced
        elif ratio <= 1.5:
            return 0.2  # Very mild imbalance
        elif ratio <= 2.0:
            return 0.4  # Mild imbalance
        elif ratio <= 3.0:
            return 0.6  # Moderate imbalance
        elif ratio <= 4.0:
            return 0.8  # High imbalance
        else:
            return 1.0  # Severe imbalance
    
    def calculate_risk(self, 
                      demographic_score: float = 0.0,
                      linguistic_score: float = 0.0,
                      toxicity_score: float = 0.0,
                      sentiment_score: float = 0.0,
                      class_imbalance_ratio: float = 0.0,
                      dataset_type: str = 'tabular',
                      has_demographic_columns: bool = False) -> Dict[str, Any]:
        """
        Calculate weighted risk score using universal aggregation logic.
        
        Args:
            demographic_score: Demographic bias score (0-1)
            linguistic_score: Linguistic bias score (0-1)
            toxicity_score: Toxicity score (0-1)
            sentiment_score: Sentiment gap score (0-1)
            class_imbalance_ratio: Class imbalance ratio (normalized 0-1)
            dataset_type: 'nlp' or 'tabular'
            has_demographic_columns: Whether demographic columns were detected
            
        Returns:
            Dictionary with comprehensive risk assessment
        """
        # Debug: Print input parameters
        print(f"*** RISK ENGINE INPUT DEBUG ***")
        print(f"demographic_score: {demographic_score}")
        print(f"linguistic_score: {linguistic_score}")
        print(f"toxicity_score: {toxicity_score}")
        print(f"sentiment_score: {sentiment_score}")
        print(f"class_imbalance_ratio: {class_imbalance_ratio}")
        print(f"dataset_type: {dataset_type}")
        print(f"has_demographic_columns: {has_demographic_columns}")
        
        # Defensive safeguards - ensure no None values
        scores = {
            'demographic': float(demographic_score or 0.0),
            'linguistic': float(linguistic_score or 0.0),
            'toxicity': float(toxicity_score or 0.0),
            'sentiment': float(sentiment_score or 0.0),
            'class_imbalance': self._normalize_class_imbalance(float(class_imbalance_ratio or 0.0))
        }
        
        print(f"*** NORMALIZED SCORES: {scores} ***")
        
        if dataset_type.lower() == 'nlp':
            return self._calculate_nlp_risk_universal(scores, has_demographic_columns)
        else:
            return self._calculate_tabular_risk_universal(scores)
    
    def _calculate_nlp_risk_universal(self, scores: Dict[str, float], has_demographic: bool) -> Dict[str, Any]:
        """Calculate NLP risk using universal aggregation logic."""
        
        # Adjust weights if demographic columns exist
        weights = self.NLP_WEIGHTS.copy()
        if has_demographic:
            # Add demographic weight and scale others proportionally
            weights = {
                "demographic": 0.10,
                "linguistic": 0.36,  # 0.40 * 0.9
                "toxicity": 0.27,    # 0.30 * 0.9
                "sentiment": 0.18,   # 0.20 * 0.9
                "class_imbalance": 0.09  # 0.10 * 0.9
            }
        
        # Calculate component contributions
        component_contributions = {}
        for component, weight in weights.items():
            contribution = scores[component] * weight * 100  # Convert to percentage
            component_contributions[component] = round(contribution, 2)
        
        # Calculate total risk percentage
        risk_percentage = sum(component_contributions.values())
        
        # Determine risk level using universal thresholds
        risk_level = self._determine_risk_level_universal(risk_percentage)
        
        # Generate conditional recommendations
        recommendations = self._generate_recommendations_universal(
            risk_level, 'nlp', scores, component_contributions
        )
        
        return {
            'dataset_type': 'nlp',
            'risk_level': risk_level,
            'risk_percentage': round(risk_percentage, 1),
            'component_scores': component_contributions,
            'weights_used': weights,
            'raw_scores': scores,
            'recommendations': recommendations,
            'requires_attention': risk_level in ['Moderate', 'High'],
            'risk_factors': self._identify_risk_factors_universal(component_contributions, 'nlp')
        }
    
    def _calculate_tabular_risk_universal(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate tabular risk using universal aggregation logic."""
        
        # Calculate component contributions
        component_contributions = {}
        for component, weight in self.TABULAR_WEIGHTS.items():
            contribution = scores[component] * weight * 100  # Convert to percentage
            component_contributions[component] = round(contribution, 2)
        
        # Calculate total risk percentage
        risk_percentage = sum(component_contributions.values())
        
        # Determine risk level using universal thresholds
        risk_level = self._determine_risk_level_universal(risk_percentage)
        
        # Generate conditional recommendations
        recommendations = self._generate_recommendations_universal(
            risk_level, 'tabular', scores, component_contributions
        )
        
        return {
            'dataset_type': 'tabular',
            'risk_level': risk_level,
            'risk_percentage': round(risk_percentage, 1),
            'component_scores': component_contributions,
            'weights_used': self.TABULAR_WEIGHTS,
            'raw_scores': scores,
            'recommendations': recommendations,
            'requires_attention': risk_level in ['Moderate', 'High'],
            'risk_factors': self._identify_risk_factors_universal(component_contributions, 'tabular')
        }
    
    def _determine_risk_level_universal(self, risk_percentage: float) -> str:
        """Determine risk level using universal thresholds."""
        if risk_percentage < self.RISK_THRESHOLDS["low"]:
            return "Low"
        elif risk_percentage < self.RISK_THRESHOLDS["moderate"]:
            return "Moderate"
        else:
            return "High"
    
    def _generate_recommendations_universal(self, risk_level: str, dataset_type: str,
                                          raw_scores: Dict[str, float], 
                                          contributions: Dict[str, float]) -> List[str]:
        """Generate recommendations based on universal numeric logic."""
        recommendations = []
        
        # Base recommendations by risk level
        if risk_level == "Low":
            recommendations.append("Dataset appears to have low overall bias risk")
            recommendations.append("Continue monitoring for bias in production")
        elif risk_level == "Moderate":
            recommendations.append("Moderate bias detected - consider mitigation strategies")
            recommendations.append("Review sensitive attribute handling and representation")
        else:  # High
            recommendations.append("High bias risk detected - immediate mitigation required")
            recommendations.append("Comprehensive review of data collection and labeling processes needed")
        
        # Conditional recommendations based on component thresholds
        if raw_scores.get('sentiment', 0) > 0.6:
            recommendations.append("Address significant sentiment bias through balanced data collection")
        elif raw_scores.get('sentiment', 0) > 0.3:
            recommendations.append("Monitor sentiment representation across different classes")
        
        if raw_scores.get('demographic', 0) > 0.3:
            recommendations.append("Implement demographic bias mitigation techniques")
        elif raw_scores.get('demographic', 0) > 0.1:
            recommendations.append("Review demographic representation in dataset")
        
        if raw_scores.get('class_imbalance', 0) > 3:  # Using ratio, not normalized
            recommendations.append("Implement re-sampling or class balancing techniques")
        elif raw_scores.get('class_imbalance', 0) > 1.5:
            recommendations.append("Consider class imbalance mitigation strategies")
        
        # Dataset-specific recommendations
        if dataset_type == 'nlp':
            if raw_scores.get('toxicity', 0) > 0.2:
                recommendations.append("Implement content filtering and toxicity reduction")
            if raw_scores.get('linguistic', 0) > 0.3:
                recommendations.append("Review linguistic patterns across demographic groups")
        else:
            if contributions.get('demographic', 0) > 20:  # 20% contribution threshold
                recommendations.append("Consider fairness-aware ML algorithms")
        
        return recommendations
    
    def _identify_risk_factors_universal(self, contributions: Dict[str, float], dataset_type: str) -> List[str]:
        """Identify specific risk factors based on contribution percentages."""
        risk_factors = []
        
        for component, contribution in contributions.items():
            if contribution > 15:  # 15% contribution threshold
                if component == 'demographic':
                    risk_factors.append("Significant demographic bias detected")
                elif component == 'linguistic':
                    risk_factors.append("Linguistic patterns show bias indicators")
                elif component == 'toxicity':
                    risk_factors.append("High toxicity detected in content")
                elif component == 'sentiment':
                    risk_factors.append("Significant sentiment bias across classes")
                elif component == 'class_imbalance':
                    risk_factors.append("Class imbalance may affect model performance")
        
        return risk_factors
    
    def get_risk_summary(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of risk assessment."""
        risk_level = risk_assessment.get('risk_level', 'Unknown')
        risk_percentage = risk_assessment.get('risk_percentage', 0)
        dataset_type = risk_assessment.get('dataset_type', 'unknown')
        
        return {
            'risk_level': risk_level,
            'risk_percentage': risk_percentage,
            'dataset_type': dataset_type,
            'summary': f"{dataset_type.title()} dataset has {risk_level.lower()} bias risk ({risk_percentage}%)",
            'recommendations': risk_assessment.get('recommendations', []),
            'requires_attention': risk_assessment.get('requires_attention', False),
            'priority': self._get_priority_universal(risk_level)
        }
    
    def _get_priority_universal(self, risk_level: str) -> str:
        """Get priority level based on universal risk levels."""
        if risk_level == 'Low':
            return 'Low'
        elif risk_level == 'Moderate':
            return 'Medium'
        else:
            return 'High'
