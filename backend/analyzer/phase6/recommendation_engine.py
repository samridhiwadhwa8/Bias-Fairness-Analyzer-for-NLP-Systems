"""
Recommendation Engine Module - Phase 6
Clean recommendations based on risk level and profile.
"""

from typing import Dict, Any, List


class RecommendationEngine:
    """Generates recommendations based on risk level and structural profile."""
    
    def generate(self, report: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate risk-based recommendations with evidence-driven executive summary.
        
        Args:
            report: Complete bias analysis report from Phase 4
            profile: Dataset profile from profiler
            
        Returns:
            Comprehensive recommendations and deployment guidance
        """
        overall_risk = report.get("overall_risk", {})
        risk_level = overall_risk.get("risk_level", "Low")
        risk_percentage = overall_risk.get("risk_percentage", 0.0)
        
        bias_analysis = report.get("bias_analysis", {})
        demographic_bias = bias_analysis.get("demographic_bias", {})
        demographic_score = demographic_bias.get("score", 0.0)
        
        profile_balance = profile.get("balance", "balanced")
        
        # Evidence-driven executive summary
        summary_parts = []
        
        # Add risk percentage
        summary_parts.append(f"Dataset shows {risk_percentage}% overall risk")
        
        # Add imbalance severity if highly imbalanced
        if profile_balance == "highly_imbalanced":
            summary_parts.append("with severe class imbalance requiring resampling")
        
        # Add fairness warning if high demographic bias
        if demographic_score > 0.6:
            summary_parts.append("and significant demographic bias requiring mitigation")
        
        # Add deployment recommendation based on risk level
        if risk_level == "High":
            summary_parts.append("Comprehensive bias mitigation required before production deployment")
        elif risk_level == "Moderate":
            summary_parts.append("Targeted bias mitigation recommended before deployment")
        else:
            summary_parts.append("Suitable for deployment with monitoring")
        
        executive_summary = ". ".join(summary_parts) + "."
        
        # Generate recommendations
        recommendations = self._get_recommendations(risk_level, profile)
        
        # Deployment decision
        deployment_decision = self._get_deployment_decision(risk_level, risk_percentage)
        
        # Next steps
        next_steps = self._get_next_steps(risk_level)
        
        return {
            "executive_summary": executive_summary,
            "risk_assessment": {
                "level": risk_level,
                "percentage": risk_percentage,
                "interpretation": self._interpret_risk_level(risk_level)
            },
            "deployment_decision": deployment_decision,
            "recommendations": recommendations,
            "next_steps": next_steps,
            "evidence_factors": {
                "imbalance_severity": profile_balance,
                "demographic_bias_score": demographic_score,
                "risk_percentage": risk_percentage
            }
        }
    
    def _get_recommendations(self, risk_level: str, profile: Dict[str, Any]) -> List[str]:
        """Get recommendations based on risk level and profile."""
        if risk_level == "High":
            return [
                "Execute comprehensive bias mitigation before production scale",
                "Implement enhanced monitoring and validation",
                "Consider dataset alternatives for high-risk applications"
            ]
        elif risk_level == "Moderate":
            return [
                "Execute targeted bias mitigation before deployment",
                "Implement enhanced monitoring protocols",
                "Schedule regular bias audits"
            ]
        else:  # Low
            return [
                "Deploy with standard monitoring",
                "Schedule periodic bias reviews",
                "Maintain current mitigation strategies"
            ]
    
    def _get_next_steps(self, risk_level: str) -> List[str]:
        """Get next steps based on risk level."""
        if risk_level == "High":
            return [
                "Execute comprehensive bias mitigation",
                "Evaluate alternative datasets",
                "Implement enhanced monitoring"
            ]
        elif risk_level == "Moderate":
            return [
                "Execute targeted bias mitigation",
                "Schedule enhanced monitoring",
                "Consider dataset alternatives"
            ]
        else:  # Low
            return [
                "Deploy with standard monitoring",
                "Continue bias monitoring",
                "Document compliance measures"
            ]
    
    def _get_deployment_decision(self, risk_level: str, risk_percentage: float) -> str:
        """Get deployment decision based on risk level and percentage."""
        if risk_level == "High":
            return "Deferred - Requires comprehensive bias mitigation"
        elif risk_level == "Moderate":
            return "Conditional - Requires targeted bias mitigation"
        else:  # Low
            return "Approved - Deploy with standard monitoring"
    
    def _interpret_risk_level(self, risk_level: str) -> str:
        """Interpret risk level for executive summary."""
        if risk_level == "High":
            return "Significant bias risks detected"
        elif risk_level == "Moderate":
            return "Moderate bias risks present"
        else:
            return "Low bias risks detected"
