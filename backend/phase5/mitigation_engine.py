"""
Mitigation Engine Module
Recommends specific mitigation strategies based on bias analysis.
"""

from typing import Dict, Any, List


class MitigationEngine:
    """Provides targeted mitigation recommendations based on bias patterns."""
    
    def recommend(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mitigation recommendations based on bias analysis.
        
        Args:
            report: Complete bias analysis report
            
        Returns:
            Dictionary with specific mitigation recommendations
        """
        dataset_type = report.get("dataset_overview", {}).get("dataset_type", "tabular")
        bias = report.get("bias_analysis", {})
        overall_risk = report.get("overall_risk") or {}
        
        recommendations = []
        priority_actions = []
        technical_strategies = []
        
        # Dataset-specific recommendations
        if dataset_type == "tabular":
            recommendations.extend(self._get_tabular_mitigations(bias))
        else:  # NLP
            recommendations.extend(self._get_nlp_mitigations(bias))
        
        # Component-specific high-priority actions
        priority_actions = self._get_priority_actions(bias, overall_risk)
        
        # Technical implementation strategies
        technical_strategies = self._get_technical_strategies(bias, dataset_type)
        
        return {
            "recommended_actions": recommendations,
            "priority_actions": priority_actions,
            "technical_strategies": technical_strategies,
            "implementation_complexity": self._assess_complexity(recommendations),
            "estimated_timeline": self._estimate_timeline(recommendations)
        }
    
    def _get_tabular_mitigations(self, bias: Dict[str, Any]) -> List[str]:
        """Get tabular-specific mitigation recommendations."""
        recommendations = []
        
        if bias.get("demographic_bias", {}).get("detected"):
            recommendations.append("Apply fairness-aware reweighting (e.g., disparate impact remover)")
            recommendations.append("Evaluate disparate impact ratio and equal opportunity metrics")
            recommendations.append("Consider adversarial debiasing for protected attributes")
        
        # Class imbalance mitigations
        if bias.get("class_imbalance_details", {}).get("ratio", 0) > 2:
            recommendations.append("Implement SMOTE or balanced sampling techniques")
            recommendations.append("Use class-weighted loss functions during training")
            recommendations.append("Consider data augmentation for minority classes")
        
        return recommendations
    
    def _get_nlp_mitigations(self, bias: Dict[str, Any]) -> List[str]:
        """Get NLP-specific mitigation recommendations."""
        recommendations = []
        
        if bias.get("linguistic_bias", {}).get("detected", False):
            recommendations.append("Perform balanced data augmentation across demographic groups")
            recommendations.append("Audit class-level sentiment skew and adjust training data")
            recommendations.append("Apply domain adaptation techniques for linguistic fairness")
        
        if bias.get("toxicity_bias", {}).get("detected", False):
            recommendations.append("Implement toxicity filtering and content moderation")
            recommendations.append("Use bias-aware language models and fine-tuning")
            recommendations.append("Add content safety layers in the pipeline")
        
        return recommendations
    
    def _get_priority_actions(self, bias: Dict[str, Any], overall_risk: Dict[str, Any]) -> List[str]:
        """Get high-priority immediate actions based on centralized risk level."""
        actions = []
        risk_level = overall_risk.get("risk_level", "Low")
        
        if risk_level == "High":
            actions.append("Initiate comprehensive mitigation plan")
            actions.append("Conduct full fairness audit immediately")
        elif risk_level == "Moderate":
            actions.append("Implement targeted bias mitigation")
            actions.append("Schedule enhanced monitoring")
        
        # Add demographic-specific actions if detected
        if overall_risk.get("bias_analysis", {}).get("demographic_bias", {}).get("detected", False):
            actions.append("Review protected attribute handling in data pipeline")
        
        return actions
    
    def _get_technical_strategies(self, bias: Dict[str, Any], dataset_type: str) -> List[str]:
        """Get technical implementation strategies."""
        strategies = []
        
        if dataset_type == "tabular":
            strategies.extend([
                "Implement fairlearn mitigation pipelines",
                "Use cross-group fairness metrics for validation",
                "Apply post-processing calibration techniques"
            ])
        else:
            strategies.extend([
                "Implement bias-aware tokenization strategies",
                "Use demographic parity constraints in training",
                "Apply counterfactual data augmentation"
            ])
        
        return strategies
    
    def _assess_complexity(self, recommendations: List[str]) -> str:
        """Assess implementation complexity."""
        if len(recommendations) <= 2:
            return "Low"
        elif len(recommendations) <= 5:
            return "Medium"
        else:
            return "High"
    
    def _estimate_timeline(self, recommendations: List[str]) -> str:
        """Estimate implementation timeline."""
        if len(recommendations) <= 2:
            return "1-2 weeks"
        elif len(recommendations) <= 5:
            return "3-6 weeks"
        else:
            return "6-12 weeks"
