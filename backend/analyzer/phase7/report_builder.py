"""
Phase 7: Dataset Governance System

Report builder for generating professional PDF reports from Phase 4-6 analysis.
"""

from typing import Dict, Any, List
from datetime import datetime
import os


class ReportBuilder:
    """Generate professional PDF reports from bias analysis results."""
    
    def __init__(self):
        self.output_dir = "outputs/reports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdf_report(self, report: Dict[str, Any], visual_paths: List[str]) -> str:
        """
        Generate comprehensive PDF report with visualizations.
        
        Args:
            report: Combined report from Phase 4-6 analysis
            visual_paths: List of generated visualization file paths
            
        Returns:
            Path to generated PDF file
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            # Create PDF document
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            filename = f"{self.output_dir}/bias_governance_report_{timestamp.replace(':', '-')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title Page
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor=colors.black
            )
            
            story.append(Paragraph("Dataset Intelligence & Bias Governance Report", title_style))
            story.append(Spacer(1, 50))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Risk Intelligence
            phase5_results = report.get("phase5_results", {})
            if phase5_results:
                exec_summary = phase5_results.get("executive_summary", {})
                story.append(Paragraph(f"Overall Assessment: {exec_summary.get('overall_assessment', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Risk Level: {exec_summary.get('key_insights', ['N/A'])[0] if exec_summary.get('key_insights') else 'N/A'}", styles['Normal']))
                story.append(Paragraph(f"Deployment Decision: {exec_summary.get('key_insights', ['N/A'])[1] if len(exec_summary.get('key_insights', [])) > 1 else 'N/A'}", styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Dataset Overview
            story.append(Paragraph("Dataset Overview", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            dataset_overview = report.get("dataset_overview", {})
            story.append(Paragraph(f"Total Rows: {dataset_overview.get('total_rows', 'N/A'):,}", styles['Normal']))
            story.append(Paragraph(f"Dataset Type: {dataset_overview.get('dataset_type', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"Target Column: {dataset_overview.get('target_column', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Bias Analysis
            story.append(Paragraph("Bias Analysis", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            bias_analysis = report.get("bias_analysis", {})
            demo_bias = bias_analysis.get("demographic_bias", {})
            story.append(Paragraph(f"Demographic Bias Detected: {'Yes' if demo_bias.get('detected', False) else 'No'}", styles['Normal']))
            story.append(Paragraph(f"Demographic Bias Score: {demo_bias.get('score', 0):.3f}", styles['Normal']))
            
            # Dataset Intelligence
            story.append(Paragraph("Dataset Intelligence", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            phase6_results = report.get("phase6_results", {})
            if phase6_results:
                profile = phase6_results.get("profile", {})
                story.append(Paragraph(f"Dataset Fingerprint: {profile.get('fingerprint', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Domain: {profile.get('domain', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Risk Percentile: {phase6_results.get('risk_percentile', 'N/A')}th percentile", styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Visual Insights Section
            story.append(Paragraph("Visual Insights", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Add visualizations (simplified - just mention they're included)
            story.append(Paragraph("Visualizations included in this report:", styles['Normal']))
            for i, path in enumerate(visual_paths, 1):
                story.append(Paragraph(f"{i}. {os.path.basename(path)}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return filename
            
        except ImportError:
            # Fallback if reportlab not available
            print("Warning: reportlab not available, using simple text output")
            return self._generate_text_fallback(report, visual_paths)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def _generate_text_fallback(self, report: Dict[str, Any], visual_paths: List[str]) -> str:
        """Generate simple text report as fallback."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")
        filename = f"{self.output_dir}/bias_governance_report_{timestamp.replace(':', '-')}.txt"
        
        with open(filename, 'w') as f:
            f.write("Dataset Intelligence & Bias Governance Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            
            phase5_results = report.get("phase5_results", {})
            if phase5_results:
                exec_summary = phase5_results.get("executive_summary", {})
                f.write(f"Overall Assessment: {exec_summary.get('overall_assessment', 'N/A')}\n")
                f.write(f"Risk Level: {exec_summary.get('key_insights', ['N/A'])[0] if exec_summary.get('key_insights') else 'N/A'}\n")
            
            f.write("\nDATASET OVERVIEW\n")
            f.write("-" * 20 + "\n")
            
            dataset_overview = report.get("dataset_overview", {})
            f.write(f"Total Rows: {dataset_overview.get('total_rows', 'N/A')}\n")
            f.write(f"Dataset Type: {dataset_overview.get('dataset_type', 'N/A')}\n")
            
            return filename
