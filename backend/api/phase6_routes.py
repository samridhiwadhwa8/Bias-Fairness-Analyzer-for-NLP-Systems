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
from pydantic import BaseModel

# Define Phase 6 request model
class Phase6Request(BaseModel):
    report: Dict[str, Any]

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
async def analyze_dataset_intelligence(request: Phase6Request):
    """Analyze dataset intelligence and ecosystem positioning."""
    try:
        print(" Phase 6 API called - Starting analysis...")
        print(f"DEBUG API: Request received: {request}")
        
        # Get the full report from Phase 4
        report = request.report
        print(f"DEBUG API: Received report type: {type(report)}")
        print(f"DEBUG API: Received report keys: {list(report.keys()) if isinstance(report, dict) else 'Not a dict'}")
        
        if not report:
            print("DEBUG API: Report is empty or None")
            raise HTTPException(status_code=400, detail="No report data provided")
        
        # Initialize Phase 6 engine
        print(" Initializing Phase 6 engine...")
        phase6_engine = Phase6Engine()
        
        # Run Phase 6 analysis
        print(" Running Phase 6 analysis...")
        results = phase6_engine.analyze(report)
        
        print(f"DEBUG API: Results type: {type(results)}")
        print(f"DEBUG API: Results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        if not results:
            print("DEBUG API: Results is empty or None")
            raise HTTPException(status_code=500, detail="Phase 6 analysis returned no results")
        
        # Validate results structure
        if not isinstance(results, dict):
            print(f"DEBUG API: Results is not a dict: {results}")
            raise HTTPException(status_code=500, detail="Phase 6 analysis returned invalid data structure")
        
        response = {
            "success": True,
            "phase": "6",
            "analysis_type": "dataset_intelligence",
            "results": results
        }
        
        print(f"DEBUG API: Final response type: {type(response)}")
        print(f"DEBUG API: Final response structure: {response}")
        print(" Phase 6 API completed successfully!")
        
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
