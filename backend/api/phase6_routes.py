"""
Phase 6 API Routes
Dataset Intelligence & Ecosystem Analysis endpoints.
"""

import sys
import os
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

# Add the analyzer directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analyzer'))

from phase6.phase6_engine import Phase6Engine


router = APIRouter(prefix="/phase6", tags=["Phase 6"])


@router.post("/analyze")
async def phase6_analysis(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform Phase 6 dataset intelligence analysis.
    
    Args:
        report: Complete bias analysis report
        
    Returns:
        Phase 6 analysis results
    """
    try:
        engine = Phase6Engine()
        result = engine.analyze(report)

        return {
            "success": True,
            "phase": 6,
            "results": result
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Phase 6 analysis failed: {str(e)}")
