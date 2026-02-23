"""
Phase 7: Dataset Governance System

Main engine for orchestrating Phase 7 reporting and visualization.
"""

import os
import sys
from typing import Dict, Any, List
from datetime import datetime
import io
import contextlib
import shutil
from datetime import datetime


class Phase7Engine:
    """Main engine for Phase 7 Dataset Governance System."""
    
    def __init__(self):
        self.visual_engine = None
        self.report_builder = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize visual and report components."""
        try:
            from .visual_engine import VisualEngine
            from .report_builder import ReportBuilder
            self.visual_engine = VisualEngine()
            self.report_builder = ReportBuilder()
        except ImportError as e:
            print(f"Warning: Could not import Phase 7 components: {e}")
    
    def generate_governance_report(self, final_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete governance report from Phase 4-6 analysis.
        
        Args:
            final_report: Combined report containing all Phase 4-6 results
            
        Returns:
            Dictionary with visual paths and PDF path
        """
        try:
            # Generate all visualizations
            visual_paths = []
            if self.visual_engine:
                with contextlib.redirect_stdout(io.StringIO()):
                    visual_paths = self.visual_engine.generate_all_visuals(final_report)
            
            # Generate PDF report
            pdf_path = None
            if self.report_builder:
                with contextlib.redirect_stdout(io.StringIO()):
                    pdf_path = self.report_builder.generate_pdf_report(final_report, visual_paths)
            
            return {
                "visual_paths": visual_paths,
                "pdf_path": pdf_path,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"Error in Phase 7 generation: {e}")
            return {
                "visual_paths": [],
                "pdf_path": None,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def cleanup_outputs(self):
        """Clean up output directories."""
        try:
            # Clean up old files (older than 24 hours)
            import time
            current_time = time.time()
            
            for directory in ["outputs/visuals", "outputs/reports"]:
                if os.path.exists(directory):
                    for filename in os.listdir(directory):
                        filepath = os.path.join(directory, filename)
                        if os.path.isfile(filepath):
                            file_age = current_time - os.path.getmtime(filepath)
                            if file_age > 86400:  # 24 hours in seconds
                                os.remove(filepath)
                                print(f"Cleaned old file: {filepath}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
