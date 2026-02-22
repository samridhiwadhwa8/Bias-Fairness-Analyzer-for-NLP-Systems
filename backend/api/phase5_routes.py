"""
Phase 5 API Routes
Provides REST endpoints for Phase 5 Risk Intelligence Engine.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase5.phase5_engine import Phase5Engine

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/phase5", tags=["Phase 5 - Risk Intelligence"])

# Initialize Phase 5 engine
engine = Phase5Engine()


@router.post("/analyze")
async def phase5_analysis(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute comprehensive Phase 5 risk intelligence analysis.
    
    Args:
        report: Complete bias analysis report from core analyzer
        
    Returns:
        Comprehensive risk intelligence with actionable insights
    """
    try:
        logger.info("Starting Phase 5 analysis")
        
        # Validate input
        if not report:
            raise HTTPException(status_code=400, detail="Empty report provided")
        
        if "overall_risk" not in report:
            raise HTTPException(status_code=400, detail="Missing overall_risk in report")
        
        # Execute Phase 5 analysis
        result = engine.execute(report)
        
        logger.info("Phase 5 analysis completed successfully")
        return {
            "success": True,
            "phase": 5,
            "results": result
        }
        
    except Exception as e:
        logger.error(f"Error in Phase 5 analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phase 5 analysis failed: {str(e)}")


@router.post("/interpret-risk")
async def interpret_risk(risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret risk levels and provide deployment guidance.
    
    Args:
        risk_assessment: Overall risk assessment from analyzer
        
    Returns:
        Risk interpretation with deployment guidance
    """
    try:
        return engine.interpreter.interpret(risk_assessment)
    except Exception as e:
        logger.error(f"Error in risk interpretation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Risk interpretation failed: {str(e)}")


@router.post("/recommend-mitigation")
async def recommend_mitigation(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate mitigation recommendations based on bias analysis.
    
    Args:
        report: Complete bias analysis report
        
    Returns:
        Specific mitigation recommendations
    """
    try:
        return engine.mitigation.recommend(report)
    except Exception as e:
        logger.error(f"Error in mitigation recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Mitigation recommendation failed: {str(e)}")


@router.post("/evaluate-deployment")
async def evaluate_deployment(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate deployment readiness based on bias and performance.
    
    Args:
        report: Complete bias analysis report
        
    Returns:
        Deployment decision and rationale
    """
    try:
        return engine.deployment.evaluate(report)
    except Exception as e:
        logger.error(f"Error in deployment evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deployment evaluation failed: {str(e)}")


@router.post("/map-compliance")
async def map_compliance(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map bias analysis to regulatory compliance requirements.
    
    Args:
        report: Complete bias analysis report
        
    Returns:
        Compliance assessment and requirements
    """
    try:
        return engine.compliance.map_compliance(report)
    except Exception as e:
        logger.error(f"Error in compliance mapping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compliance mapping failed: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for Phase 5 engine.
    
    Returns:
        Health status
    """
    return {"status": "healthy", "service": "Phase 5 Risk Intelligence Engine"}
