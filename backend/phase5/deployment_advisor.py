"""
Deployment Advisor Module
Converts bias analysis and model performance into deployment decisions.
"""

from typing import Dict, Any


class DeploymentAdvisor:
    """Provides deployment go/no-go decisions based on risk and performance."""
    
    def evaluate(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate deployment readiness based on bias and performance metrics.
        
        Args:
            report: Complete bias analysis report
            
        Returns:
            Dictionary with deployment decision and rationale
        """
        risk = (report.get("overall_risk") or {}).get("risk_percentage", 0)
        risk_level = (report.get("overall_risk") or {}).get("risk_level", "Low")
        
        # Extract performance metrics
        ml_results = report.get("ml_training", {})
        accuracy = ml_results.get("accuracy", 0)
        f1_score = ml_results.get("f1_score", 0)
        
        # Business context factors
        has_demographic_bias = report.get("bias_analysis", {}).get("demographic_bias", {}).get("detected", False)
        class_imbalance_ratio = report.get("ml_training", {}).get("class_imbalance_details", {}).get("ratio", 1)
        
        # Decision logic
        decision, confidence, rationale = self._make_decision(
            risk, risk_level, accuracy, f1_score, has_demographic_bias, class_imbalance_ratio
        )
        
        # Deployment conditions
        conditions = self._get_deployment_conditions(decision, risk, accuracy)
        
        # Monitoring requirements
        monitoring = self._get_monitoring_requirements(decision, risk_level)
        
        return {
            "deployment_decision": decision,
            "confidence_score": confidence,
            "decision_rationale": rationale,
            "deployment_conditions": conditions,
            "monitoring_requirements": monitoring,
            "performance_thresholds_met": self._check_performance_thresholds(accuracy, f1_score),
            "risk_acceptable": risk < 70
        }
    
    def _make_decision(self, risk: float, risk_level: str, accuracy: float, 
                      f1_score: float, has_demographic_bias: bool, 
                      class_imbalance_ratio: float) -> tuple:
        """Make deployment decision based on centralized risk level."""
        
        # Decision logic based on aggregated risk level only
        if risk_level == "High":
            return "Conditional Approval - Comprehensive Mitigation Required", 0.95, [
                "High aggregated risk exceeds standard threshold",
                "Comprehensive mitigation required before scale",
                "Enhanced monitoring and compliance review needed"
            ]
        
        elif risk_level == "Moderate":
            # Check if performance is also poor
            if accuracy < 60:
                return "Conditional Approval - Performance Improvement Required", 0.90, [
                    "Moderate risk combined with suboptimal performance",
                    "Both bias mitigation and performance enhancement needed",
                    "Performance improvement required before scale"
                ]
            else:
                return "Conditional Approval", 0.80, [
                    "Moderate aggregated risk detected",
                    "Mitigation recommended before scale",
                    "Enhanced monitoring required"
                ]
        
        else:  # Low risk
            return "Deploy with Standard Monitoring", 0.85, [
                "Low aggregated risk within acceptable range",
                "Standard deployment protocols apply",
                "Regular monitoring sufficient"
            ]
    
    def _get_deployment_conditions(self, decision: str, risk: float, accuracy: float) -> list:
        """Get specific conditions for deployment."""
        conditions = []
        
        if decision == "Approved":
            conditions.append("Standard monitoring dashboard setup")
            conditions.append("Quarterly bias review schedule")
            
        elif decision == "Conditional Approval":
            conditions.append("Enhanced monitoring with bias alerts")
            conditions.append("Monthly bias audit reports")
            conditions.append("Mitigation plan implementation within 30 days")
            if risk >= 50:
                conditions.append("Stakeholder approval required")
            if accuracy < 70:
                conditions.append("Performance improvement plan")
                
        else:  # Blocked
            conditions.append("Comprehensive bias mitigation required")
            conditions.append("Model performance improvement needed")
            conditions.append("Re-evaluation after mitigation")
            if risk >= 70:
                conditions.append("External audit recommended")
        
        return conditions
    
    def _get_monitoring_requirements(self, decision: str, risk_level: str) -> Dict[str, Any]:
        """Get monitoring requirements based on decision."""
        if decision == "Approved":
            return {
                "frequency": "Quarterly",
                "metrics": ["accuracy", "demographic parity", "equal opportunity"],
                "alert_thresholds": {"bias_increase": 0.1, "performance_drop": 0.05}
            }
        elif decision == "Conditional Approval":
            return {
                "frequency": "Monthly",
                "metrics": ["accuracy", "demographic parity", "equal opportunity", "disparate impact"],
                "alert_thresholds": {"bias_increase": 0.05, "performance_drop": 0.03}
            }
        else:  # Blocked
            return {
                "frequency": "Weekly (during mitigation)",
                "metrics": ["all fairness metrics", "performance metrics"],
                "alert_thresholds": {"any_bias_increase": 0.01, "performance_drop": 0.01}
            }
    
    def _check_performance_thresholds(self, accuracy: float, f1_score: float) -> Dict[str, bool]:
        """Check if performance thresholds are met."""
        return {
            "accuracy_threshold_met": accuracy >= 60,
            "f1_threshold_met": f1_score >= 0.6,
            "minimum_performance_met": accuracy >= 50
        }
