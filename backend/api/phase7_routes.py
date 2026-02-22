"""
Phase 7: Dataset Governance System API Routes

API endpoints for generating governance reports and visualizations.
"""

import os
import sys
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
import logging
import zipfile
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer.phase7.phase7_engine import Phase7Engine

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/phase7", tags=["Phase 7 - Dataset Governance"])

# Initialize Phase 7 engine
engine = Phase7Engine()


@router.post("/generate")
async def generate_governance_report(final_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive governance report with visualizations.
    
    Args:
        final_report: Complete report from Phase 4-6 analysis
        
    Returns:
        Governance report with visualizations and PDF
    """
    try:
        logger.info("Starting Phase 7 governance report generation")
        
        # Validate input
        if not final_report:
            raise HTTPException(status_code=400, detail="Empty report provided")
        
        # Generate governance report
        result = engine.generate_governance_report(final_report)
        
        logger.info("Phase 7 governance report completed successfully")
        return {
            "success": True,
            "phase": 7,
            "results": result,
            "message": "Governance report generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in Phase 7 generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phase 7 generation failed: {str(e)}")


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download generated files (PDF or images).
    
    Args:
        filename: Name of file to download
        
    Returns:
        File download response
    """
    try:
        # Security check - only allow specific file types and paths
        allowed_extensions = ['.pdf', '.png']
        allowed_dirs = ['outputs/reports', 'outputs/visuals']
        
        file_path = None
        for directory in allowed_dirs:
            potential_path = os.path.join(directory, filename)
            if os.path.exists(potential_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in allowed_extensions:
                    file_path = potential_path
                    break
        
        if not file_path:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Check if file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return file for download
        from fastapi.responses import FileResponse
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/pdf' if filename.endswith('.pdf') else 'image/png'
        )
        
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/download-visuals")
async def download_visuals_zip():
    """
    Download all visualizations as a ZIP file.
    
    Returns:
        ZIP file with all PNG visualizations
    """
    try:
        # Create ZIP file
        zip_path = "outputs/visuals.zip"
        visual_dir = "outputs/visuals"
        
        if not os.path.exists(visual_dir):
            raise HTTPException(status_code=404, detail="No visualizations available")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(visual_dir):
                for file in files:
                    if file.endswith('.png'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, visual_dir)
                        zipf.write(file_path, arcname)
        
        # Return ZIP file
        from fastapi.responses import FileResponse
        return FileResponse(
            path=zip_path,
            filename="visual_insights.zip",
            media_type='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Error creating ZIP file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"ZIP creation failed: {str(e)}")
