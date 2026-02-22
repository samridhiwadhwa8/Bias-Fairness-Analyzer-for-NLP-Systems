"""
Compliance Mapper Module
Maps detected bias to regulatory exposure and compliance requirements.
"""

from typing import Dict, Any, List


class ComplianceMapper:
    """Maps bias analysis to regulatory compliance and legal exposure."""
    
    def map_compliance(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map bias analysis to regulatory compliance requirements.
        
        Args:
            report: Complete bias analysis report
            
        Returns:
            Dictionary with compliance assessment and requirements
        """
        bias = report.get("bias_analysis", {})
        overall_risk = report.get("overall_risk") or {}
        dataset_type = report.get("dataset_overview", {}).get("dataset_type", "tabular")
        
        # Extract key compliance factors
        demo_detected = bias.get("demographic_bias", {}).get("detected", False)
        demo_score = bias.get("demographic_bias", {}).get("score", 0)
        risk_level = overall_risk.get("risk_level", "Low")
        risk_percentage = overall_risk.get("risk_percentage", 0)
        
        # Compliance assessment
        regulatory_risk = self._assess_regulatory_risk(demo_detected, demo_score, risk_level)
        legal_exposure = self._assess_legal_exposure(demo_detected, risk_percentage, dataset_type)
        compliance_requirements = self._get_compliance_requirements(demo_detected, risk_level)
        
        # Framework mappings
        applicable_frameworks = self._get_applicable_frameworks(demo_detected, dataset_type)
        
        return {
            "regulatory_risk": regulatory_risk,
            "legal_exposure": legal_exposure,
            "compliance_requirements": compliance_requirements,
            "applicable_frameworks": applicable_frameworks,
            "audit_requirements": self._get_audit_requirements(risk_level),
            "documentation_needs": self._get_documentation_needs(demo_detected, risk_level)
        }
    
    def _assess_regulatory_risk(self, demo_detected: bool, demo_score: float, risk_level: str) -> Dict[str, Any]:
        """Assess regulatory risk based on centralized risk level."""
        if not demo_detected:
            return {
                "level": "Low",
                "description": "No protected attributes detected - minimal regulatory risk",
                "review_required": False,
                "priority": "Low"
            }
        
        # Primary decision based on aggregated risk level
        if risk_level == "High":
            return {
                "level": "High",
                "description": "High aggregated risk with protected attributes detected",
                "review_required": True,
                "priority": "Elevated",
                "regulations": ["EEOC guidelines", "Fair Housing Act", "Equal Credit Opportunity Act"]
            }
        elif risk_level == "Moderate":
            return {
                "level": "Medium",
                "description": "Moderate aggregated risk with protected attributes detected",
                "review_required": True,
                "priority": "Medium",
                "regulations": ["EEOC guidelines", "Industry-specific fairness standards"]
            }
        else:  # Low risk level
            return {
                "level": "Low",
                "description": "Low aggregated risk with protected attributes detected",
                "review_required": False,
                "priority": "Low",
                "regulations": ["General fairness guidelines"]
            }
    
    def _assess_legal_exposure(self, demo_detected: bool, risk_percentage: float, dataset_type: str) -> Dict[str, Any]:
        """Assess potential legal exposure."""
        if not demo_detected:
            return {
                "exposure_level": "Minimal",
                "risk_categories": [],
                "mitigation_priority": "Low"
            }
        
        risk_categories = []
        if risk_percentage > 70:
            risk_categories.extend([
                "Discrimination claims",
                "Regulatory penalties",
                "Class action lawsuits",
                "Reputational damage"
            ])
        elif risk_percentage > 40:
            risk_categories.extend([
                "Regulatory scrutiny",
                "Compliance violations",
                "Contractual breaches"
            ])
        else:
            risk_categories.extend([
                "Minor compliance issues",
                "Documentation requirements"
            ])
        
        return {
            "exposure_level": self._map_exposure_level(risk_percentage),
            "risk_categories": risk_categories,
            "mitigation_priority": self._map_priority(risk_percentage),
            "jurisdictional_considerations": self._get_jurisdictions(dataset_type)
        }
    
    def _get_compliance_requirements(self, demo_detected: bool, risk_level: str) -> List[str]:
        """Get specific compliance requirements."""
        requirements = []
        
        if demo_detected:
            requirements.extend([
                "Document bias mitigation efforts",
                "Implement fairness monitoring",
                "Conduct regular bias audits",
                "Provide explainability for decisions"
            ])
        
        if risk_level in ["Moderate", "High"]:
            requirements.extend([
                "External compliance review",
                "Stakeholder notification",
                "Regulatory filing (if applicable)",
                "Incident response plan"
            ])
        
        if risk_level == "High":
            requirements.extend([
                "Legal counsel consultation",
                "Comprehensive impact assessment",
                "Remediation timeline documentation"
            ])
        
        return requirements
    
    def _get_applicable_frameworks(self, demo_detected: bool, dataset_type: str) -> List[str]:
        """Get applicable compliance frameworks."""
        frameworks = ["General Data Protection Regulation (GDPR)"]
        
        if demo_detected:
            frameworks.extend([
                "AI Act (EU)",
                "NIST AI Risk Management Framework",
                "IEEE 7003 Standard for Algorithmic Bias Considerations"
            ])
        
        if dataset_type == "nlp":
            frameworks.extend([
                "ISO/IEC 23894:2023 (Information technology — Artificial intelligence — Guidance on AI risk management)",
                "NIST Language Technology Evaluation Standards"
            ])
        else:
            frameworks.extend([
                "Fairlearn Toolkit Guidelines",
                "IBM AI Fairness 360 Framework"
            ])
        
        return frameworks
    
    def _get_audit_requirements(self, risk_level: str) -> Dict[str, Any]:
        """Get audit requirements based on risk level."""
        if risk_level == "High":
            return {
                "frequency": "Quarterly",
                "scope": "Comprehensive",
                "external_required": True,
                "documentation": "Full audit trail required"
            }
        elif risk_level == "Moderate":
            return {
                "frequency": "Semi-annual",
                "scope": "Targeted",
                "external_required": False,
                "documentation": "Key metrics documentation required"
            }
        else:
            return {
                "frequency": "Annual",
                "scope": "Basic",
                "external_required": False,
                "documentation": "Standard compliance documentation"
            }
    
    def _get_documentation_needs(self, demo_detected: bool, risk_level: str) -> List[str]:
        """Get documentation requirements."""
        needs = ["Model documentation", "Performance metrics"]
        
        if demo_detected:
            needs.extend([
                "Fairness assessment report",
                "Bias mitigation documentation",
                "Protected attribute handling procedures"
            ])
        
        if risk_level in ["Moderate", "High"]:
            needs.extend([
                "Risk assessment documentation",
                "Stakeholder communication records",
                "Compliance checklists"
            ])
        
        return needs
    
    def _map_exposure_level(self, risk_percentage: float) -> str:
        """Map risk percentage to exposure level."""
        if risk_percentage >= 70:
            return "High"
        elif risk_percentage >= 40:
            return "Medium"
        else:
            return "Low"
    
    def _map_priority(self, risk_percentage: float) -> str:
        """Map risk percentage to mitigation priority."""
        if risk_percentage >= 70:
            return "Critical"
        elif risk_percentage >= 40:
            return "High"
        else:
            return "Medium"
    
    def _get_jurisdictions(self, dataset_type: str) -> List[str]:
        """Get relevant jurisdictions based on dataset type."""
        jurisdictions = ["US (Federal)", "EU"]
        
        if dataset_type == "nlp":
            jurisdictions.extend(["US (State-level - California, Illinois)", "Canada"])
        else:
            jurisdictions.extend(["US (State-level - New York, Massachusetts)"])
        
        return jurisdictions
