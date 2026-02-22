"""
Risk Interpreter Module
Converts numeric risk into business meaning and deployment guidance.
"""

from typing import Dict, Any


class RiskInterpreter:
    """Converts numeric risk assessment into actionable business intelligence."""
    
    def interpret(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret risk levels and provide deployment guidance.
        
        Args:
            risk_assessment: Overall risk assessment from analyzer
            
        Returns:
            Dictionary with interpreted business meaning
        """
        level = risk_assessment.get("risk_level", "Low")
        percentage = risk_assessment.get("risk_percentage", 0)
        
        # Business interpretation logic
        if level == "Low":
            action = "Deploy with standard monitoring"
            severity = "Normal"
            monitoring = "Standard monitoring required"
            timeline = "Immediate deployment possible"
            
        elif level == "Moderate":
            action = "Conditional approval with mitigation"
            severity = "Elevated"
            monitoring = "Enhanced monitoring and periodic bias reviews"
            timeline = "Mitigation recommended before scale (2-4 weeks)"
            
        else:  # High
            action = "Conditional approval with comprehensive mitigation"
            severity = "High"
            monitoring = "Continuous monitoring with bias alerts"
            timeline = "Comprehensive mitigation required before scale (6-8 weeks)"
        
        return {
            "risk_level": level,
            "risk_percentage": percentage,
            "deployment_action": action,
            "severity_category": severity,
            "monitoring_requirements": monitoring,
            "deployment_timeline": timeline,
            "business_impact": self._assess_business_impact(level, percentage)
        }
    
    def _assess_business_impact(self, level: str, percentage: float) -> str:
        """Assess potential business impact."""
        if level == "Low":
            return "Minimal operational risk"
        elif level == "Moderate":
            return "Potential regulatory and reputational risk"
        else:
            return "High regulatory, legal, and reputational exposure"
