"""
Phase 6 API Routes
REST endpoints for clean Dataset Intelligence & Ecosystem Layer.
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

# Import new clean Phase 6 engine
from analyzer.phase6.phase6_engine import Phase6Engine

router = APIRouter(prefix="/phase6", tags=["Phase 6 - Dataset Intelligence"])

# Initialize Phase 6 engine
phase6_engine = Phase6Engine()


@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify Phase 6 API is working."""
    return {
        "message": "Phase 6 API is working",
        "status": "healthy",
        "timestamp": str(datetime.now())
    }


@router.post("/analyze")
async def analyze_dataset_intelligence(report: Dict[str, Any]):
    """
    Analyze dataset intelligence with clean structural profiling.
    
    Args:
        report: Complete bias analysis report from Phase 4
        
    Returns:
        Comprehensive dataset intelligence and recommendations
    """
    try:
        if not report:
            raise HTTPException(status_code=400, detail="Report data is required")
        
        print(f"DEBUG API: Received report type: {type(report)}")
        print(f"DEBUG API: Received report keys: {list(report.keys()) if isinstance(report, dict) else 'Not a dict'}")
        print(f"DEBUG API: Report overview: {report.get('dataset_overview', {})}")
        
        # Execute Phase 6 analysis
        results = phase6_engine.analyze(report)
        print(f"DEBUG API: Phase 6 results type: {type(results)}")
        print(f"DEBUG API: Phase 6 results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        print(f"DEBUG API: Profile from results: {type(results.get('profile', 'NOT_FOUND'))}")
        if isinstance(results, dict) and isinstance(results.get('profile'), dict):
            print(f"DEBUG API: Profile keys: {list(results['profile'].keys())}")
        else:
            print(f"DEBUG API: Profile is not a dict or is missing")
        
        response = {
            "success": True,
            "phase": "6",
            "analysis_type": "dataset_intelligence",
            "results": results
        }
        
        print(f"DEBUG API: Final response type: {type(response)}")
        print(f"DEBUG API: Final response: {response}")
        
        return response
        
    except Exception as e:
        print(f"DEBUG API: Exception occurred: {str(e)}")
        import traceback
        print(f"DEBUG API: Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Phase 6 analysis failed: {str(e)}")


@router.get("/archetypes")
async def get_available_archetypes():
    """
    Get available dataset archetypes for suggestions.
    
    Returns:
        List of supported archetypes and example datasets
    """
    try:
        # Return archetypes from Kaggle suggester
        archetypes = phase6_engine.kaggle.archetypes
        
        return {
            "success": True,
            "archetypes": list(archetypes.keys()),
            "total_archetypes": len(archetypes),
            "example_datasets": {
                archetype: datasets[:2] for archetype, datasets in archetypes.items()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve archetypes: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for Phase 6."""
    return {
        "status": "healthy",
        "phase": "6",
        "service": "Dataset Intelligence & Ecosystem Layer",
        "architecture": "clean_structural_profiling",
        "components": {
            "profiler": "active",
            "benchmark_engine": "active",
            "recommendation_engine": "active",
            "kaggle_suggester": "active"
        }
    }
