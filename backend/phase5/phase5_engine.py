"""
Phase 5 Unified Engine
Orchestrates all Phase 5 modules for comprehensive risk intelligence.
"""

from typing import Dict, Any, List

from .risk_interpreter import RiskInterpreter
from .mitigation_engine import MitigationEngine
from .deployment_advisor import DeploymentAdvisor
from .compliance_mapper import ComplianceMapper


class Phase5Engine:
    """Unified Phase 5 Risk Intelligence Engine."""
    
    def __init__(self):
        """Initialize all Phase 5 modules."""
        self.interpreter = RiskInterpreter()
        self.mitigation = MitigationEngine()
        self.deployment = DeploymentAdvisor()
        self.compliance = ComplianceMapper()
    
    def execute(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute comprehensive Phase 5 analysis on bias report.
        
        Args:
            report: Complete bias analysis report from core analyzer
            
        Returns:
            Dictionary with comprehensive risk intelligence and actionable insights
        """
        # Execute all Phase 5 modules with safe handling
        overall_risk = report.get("overall_risk") or {}
        interpretation = self.interpreter.interpret(overall_risk) or {}
        mitigation = self.mitigation.recommend(report) or {}
        deployment = self.deployment.evaluate(report) or {}
        compliance = self.compliance.map_compliance(report) or {}
        
        # Generate executive summary with safe handling
        executive_summary = self._generate_executive_summary(
            interpretation, mitigation, deployment, compliance
        ) or {}
        
        # Create action plan with safe handling
        action_plan = self._create_action_plan(deployment, mitigation, compliance) or {}
        
        return {
            "executive_summary": executive_summary,
            "interpretation": interpretation,
            "mitigation": mitigation,
            "deployment": deployment,
            "compliance": compliance,
            "action_plan": action_plan,
            "metadata": {
                "phase5_version": "1.0.0",
                "analysis_timestamp": "2025-02-21",
                "modules_executed": ["risk_interpreter", "mitigation_engine", 
                                  "deployment_advisor", "compliance_mapper"]
            }
        }
    
    def _generate_executive_summary(self, interpretation: Dict[str, Any], 
                                 mitigation: Dict[str, Any],
                                 deployment: Dict[str, Any],
                                 compliance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary for stakeholders."""
        
        # Safe extraction with defaults
        risk_level = interpretation.get("risk_level", "Low") if interpretation else "Low"
        deployment_decision = deployment.get("deployment_decision", "Approved") if deployment else "Approved"
        regulatory_risk = compliance.get("regulatory_risk", {}).get("level", "Low") if compliance and compliance.get("regulatory_risk") else "Low"
        
        # Key insights
        key_insights = [
            f"Risk Level: {risk_level} ({interpretation.get('risk_percentage', 0)}%)" if interpretation else "Risk Level: Low (0%)",
            f"Deployment Decision: {deployment_decision}",
            f"Regulatory Risk: {regulatory_risk}",
            f"Mitigation Complexity: {mitigation.get('implementation_complexity', 'Low')}" if mitigation else "Mitigation Complexity: Low"
        ]
        
        # Immediate actions
        immediate_actions = []
        if "Comprehensive Mitigation Required" in deployment_decision:
            immediate_actions.append("Initiate comprehensive mitigation plan")
        if "Performance Improvement Required" in deployment_decision:
            immediate_actions.append("Focus on model performance improvement")
        if regulatory_risk in ["Medium", "High"]:
            immediate_actions.append("Initiate compliance review")
        if mitigation and mitigation.get("priority_actions"):
            immediate_actions.extend(mitigation.get("priority_actions", [])[:2])
        
        # Timeline overview
        timeline = interpretation.get("deployment_timeline", "Immediate") if interpretation else "Immediate"
        mitigation_timeline = mitigation.get("estimated_timeline", "1-2 weeks") if mitigation else "1-2 weeks"
        
        return {
            "overall_assessment": self._get_overall_assessment(deployment_decision, regulatory_risk),
            "key_insights": key_insights,
            "immediate_actions": immediate_actions,
            "timeline_overview": {
                "deployment": timeline,
                "mitigation": mitigation_timeline
            },
            "stakeholder_impact": self._assess_stakeholder_impact(risk_level, regulatory_risk)
        }
    
    def _create_action_plan(self, deployment: Dict[str, Any],
                          mitigation: Dict[str, Any],
                          compliance: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured action plan."""
        
        # Safe extraction with defaults
        deployment_conditions = deployment.get("deployment_conditions", []) if deployment else []
        mitigation_actions = mitigation.get("recommended_actions", []) if mitigation else []
        compliance_requirements = compliance.get("compliance_requirements", []) if compliance else []
        deployment_decision = deployment.get("deployment_decision", "") if deployment else ""
        
        # Prioritize actions
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # High priority actions
        if "Comprehensive Mitigation Required" in deployment_decision:
            high_priority.extend([
                "Address significant bias issues",
                "Implement comprehensive mitigation plan"
            ])
        elif "Performance Improvement Required" in deployment_decision:
            high_priority.extend([
                "Improve model performance metrics",
                "Optimize algorithm efficiency"
            ])
        
        if mitigation and mitigation.get("priority_actions"):
            high_priority.extend(mitigation.get("priority_actions", []))
        
        # Medium priority actions
        medium_priority.extend(mitigation_actions[:3])
        medium_priority.extend(compliance_requirements[:2])
        
        # Low priority actions
        low_priority.extend(mitigation_actions[3:])
        low_priority.extend(compliance_requirements[2:])
        
        return {
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "success_criteria": self._define_success_criteria(deployment, mitigation, compliance),
            "resource_requirements": self._estimate_resources(mitigation, compliance)
        }
    
    def _get_overall_assessment(self, deployment_decision: str, regulatory_risk: str) -> str:
        """Get overall assessment."""
        if deployment_decision == "Blocked" or regulatory_risk == "High":
            return "HIGH SEVERITY - Comprehensive mitigation required"
        elif deployment_decision == "Conditional Approval" or regulatory_risk == "Medium":
            return "ELEVATED SEVERITY - Mitigation recommended before scale"
        else:
            return "NORMAL - Proceed with standard monitoring"
    
    def _assess_stakeholder_impact(self, risk_level: str, regulatory_risk: str) -> Dict[str, str]:
        """Assess impact on different stakeholders."""
        return {
            "executive": self._get_executive_impact(risk_level, regulatory_risk),
            "technical": self._get_technical_impact(risk_level),
            "legal": self._get_legal_impact(regulatory_risk),
            "business": self._get_business_impact(risk_level, regulatory_risk)
        }
    
    def _get_executive_impact(self, risk_level: str, regulatory_risk: str) -> str:
        """Get executive-level impact."""
        if risk_level == "High" or regulatory_risk == "High":
            return "High - Strategic decision required, potential reputational risk"
        elif risk_level == "Moderate" or regulatory_risk == "Medium":
            return "Medium - Monitor closely, allocate resources for mitigation"
        else:
            return "Low - Standard oversight sufficient"
    
    def _get_technical_impact(self, risk_level: str) -> str:
        """Get technical team impact."""
        if risk_level == "High":
            return "High - Major refactoring and retraining required"
        elif risk_level == "Moderate":
            return "Medium - Targeted improvements needed"
        else:
            return "Low - Minor adjustments and monitoring"
    
    def _get_legal_impact(self, regulatory_risk: str) -> str:
        """Get legal team impact."""
        if regulatory_risk == "High":
            return "High - Legal review required, potential compliance issues"
        elif regulatory_risk == "Medium":
            return "Medium - Documentation and review needed"
        else:
            return "Low - Standard compliance procedures"
    
    def _get_business_impact(self, risk_level: str, regulatory_risk: str) -> str:
        """Get business impact."""
        if risk_level == "High" or regulatory_risk == "High":
            return "High - Potential deployment delays, compliance costs"
        elif risk_level == "Moderate" or regulatory_risk == "Medium":
            return "Medium - Some delay, mitigation costs expected"
        else:
            return "Low - Minimal business impact"
    
    def _define_success_criteria(self, deployment: Dict[str, Any],
                              mitigation: Dict[str, Any],
                              compliance: Dict[str, Any]) -> List[str]:
        """Define success criteria for action plan."""
        criteria = []
        
        if deployment.get("deployment_decision") != "Approved":
            criteria.append("Reduce bias risk to acceptable levels")
            criteria.append("Meet minimum performance thresholds")
        
        if compliance.get("regulatory_risk", {}).get("level") != "Low":
            criteria.append("Address all compliance requirements")
            criteria.append("Complete documentation for audit")
        
        criteria.extend([
            "Implement monitoring framework",
            "Validate mitigation effectiveness"
        ])
        
        return criteria
    
    def _estimate_resources(self, mitigation: Dict[str, Any], 
                          compliance: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate resource requirements."""
        complexity = mitigation.get("implementation_complexity", "Low")
        regulatory_level = compliance.get("regulatory_risk", {}).get("level", "Low")
        
        # Resource estimation based on complexity and regulatory requirements
        if complexity == "High" or regulatory_level == "High":
            return {
                "team_size": "4-6 people",
                "timeline": "8-12 weeks",
                "budget": "High",
                "expertise": ["ML Engineers", "Legal Counsel", "Compliance Officers", "Domain Experts"]
            }
        elif complexity == "Medium" or regulatory_level == "Medium":
            return {
                "team_size": "2-4 people",
                "timeline": "4-8 weeks",
                "budget": "Medium",
                "expertise": ["ML Engineers", "Legal/Compliance"]
            }
        else:
            return {
                "team_size": "1-2 people",
                "timeline": "1-4 weeks",
                "budget": "Low",
                "expertise": ["ML Engineers"]
            }
