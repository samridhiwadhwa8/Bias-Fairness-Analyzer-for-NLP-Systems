"""
Phase 7: Dataset Governance System

Report builder for generating professional PDF reports from Phase 4-6 analysis.
"""

from typing import Dict, Any, List
from datetime import datetime
import os
import io
import tempfile


class ReportBuilder:
    """Generate professional PDF reports from bias analysis results."""
    
    def __init__(self):
        import tempfile
        # Use system temp directory instead of project directory
        self.output_dir = tempfile.gettempdir() + "/bias_reports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdf_report(self, report: Dict[str, Any], visual_paths: List[str]) -> str:
        """
        Generate comprehensive PDF report with embedded visualizations.
        
        Args:
            report: Combined report from Phase 4-6 analysis
            visual_paths: List of generated visualization file paths
            
        Returns:
            Path to generated PDF file
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
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
                
                # Risk Assessment Narrative
                risk_level = exec_summary.get('overall_assessment', 'N/A')
                risk_percentage = exec_summary.get('key_insights', ['N/A'])[0] if exec_summary.get('key_insights') else 'N/A'
                
                if 'Risk Level:' in risk_percentage:
                    risk_num = risk_percentage.split('(')[1].split('%')[0]
                    risk_desc = f"The dataset presents a {risk_level} risk level at {risk_num}% overall risk, "
                else:
                    risk_desc = f"The dataset presents a {risk_level} risk level, "
                
                risk_desc += self._get_risk_interpretation(risk_level)
                
                story.append(Paragraph(f"Risk Assessment: {risk_desc}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Dataset Overview
            story.append(Paragraph("Dataset Overview", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            dataset_overview = report.get("dataset_overview", {})
            story.append(Paragraph(f"Dataset Characteristics: The analysis was performed on a {dataset_overview.get('dataset_type', 'unknown').lower()} dataset containing {dataset_overview.get('total_rows', 'N/A'):,} rows with {len(dataset_overview.get('available_columns', []))} features.", styles['Normal']))
            story.append(Paragraph(f"Target Variable: {dataset_overview.get('target_column', 'N/A')} was used as the prediction target.", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Bias Analysis
            story.append(Paragraph("Bias Analysis", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            bias_analysis = report.get("bias_analysis", {})
            demo_bias = bias_analysis.get("demographic_bias", {})
            story.append(Paragraph(f"Demographic Bias: {'Detected' if demo_bias.get('detected', False) else 'Not Detected'} with a bias score of {demo_bias.get('score', 0):.3f}", styles['Normal']))
            
            if demo_bias.get('detected', False):
                story.append(Paragraph(f"Impact: Protected attributes including {demo_bias.get('columns', [])} show potential bias requiring mitigation before deployment.", styles['Normal']))
            
            # Model Performance
            story.append(Paragraph("Model Performance", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            ml_training = report.get("ml_training", {})
            f1_score = ml_training.get('f1_score', 0)
            performance_desc = 'moderate' if f1_score < 0.8 else 'good'
            story.append(Paragraph(f"Model Performance: The {ml_training.get('model', 'Random Forest')} model achieved {ml_training.get('accuracy', 0):.1%} accuracy with an F1 score of {f1_score:.3f}, indicating {performance_desc} predictive performance.", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Dataset Intelligence
            story.append(Paragraph("Dataset Intelligence", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            phase6_results = report.get("phase6_results", {})
            if phase6_results:
                profile = phase6_results.get("profile", {})
                story.append(Paragraph(f"Dataset Fingerprint: {profile.get('fingerprint', 'N/A')} categorizes this dataset as {profile.get('domain', 'N/A')}-{profile.get('task', 'N/A')}-{profile.get('size', 'N/A')}-{profile.get('balance', 'N/A')}", styles['Normal']))
                
                percentile = phase6_results.get("risk_percentile", 0)
                position = phase6_results.get("market_position", 'N/A')
                story.append(Paragraph(f"Market Position: The dataset ranks at the {percentile}th percentile, positioning it {position} compared to similar datasets in the ecosystem.", styles['Normal']))
            
            # Add embedded visualizations
            story.append(Paragraph("Visual Insights", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Embed each visualization directly in PDF
            for i, path in enumerate(visual_paths, 1):
                if os.path.exists(path):
                    try:
                        # Read image into memory
                        with open(path, 'rb') as img_file:
                            img_data = img_file.read()
                        
                        # Create image from memory
                        img = Image(img_data)
                        img.drawWidth = 6*inch
                        img.drawHeight = 4*inch
                        
                        story.append(Paragraph(f"Figure {i}: {os.path.basename(path)}", styles['Heading3']))
                        story.append(img)
                        story.append(Spacer(1, 6))
                        print(f"✅ Embedded image {i}: {os.path.basename(path)}")
                    except Exception as img_error:
                        print(f"❌ Error embedding image {path}: {img_error}")
                        story.append(Paragraph(f"Figure {i}: {os.path.basename(path)} (embedding failed)", styles['Normal']))
                else:
                    print(f"⚠️ Image file not found: {path}")
                    story.append(Paragraph(f"Figure {i}: {os.path.basename(path)} (file not found)", styles['Normal']))
            story.append(Spacer(1, 12))
            
            if phase5_results:
                deployment = phase5_results.get("deployment", {})
                mitigation = phase5_results.get("mitigation", {})
                
                story.append(Paragraph("Recommended Actions:", styles['Heading3']))
                for action in mitigation.get("recommended_actions", [])[:3]:
                    story.append(Paragraph(f"• {action}", styles['Normal']))
                
                story.append(Paragraph(f"Implementation Timeline: {mitigation.get('estimated_timeline', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Complexity: {mitigation.get('implementation_complexity', 'N/A')}", styles['Normal']))
            
            # Final Decision
            story.append(Paragraph("Deployment Decision", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            if phase5_results:
                deployment_decision = deployment.get("deployment_decision", "Pending")
                confidence = deployment.get("confidence_score", 0)
                
                decision_color = "green" if "Deploy" in deployment_decision else "red"
                story.append(Paragraph(f"Final Decision: {deployment_decision} (Confidence: {int(confidence * 100)}%)", styles['Normal'], textColor=colors.HexColor(decision_color)))
            
            # Build PDF
            try:
                doc.build(story)
                print(f"✅ PDF generated successfully: {filename}")
                return filename
            except Exception as pdf_error:
                print(f"❌ PDF build error: {pdf_error}")
                # Fallback to text if PDF fails
                return self._generate_text_fallback(report, visual_paths)
            
        except ImportError:
            # Fallback if reportlab not available
            print("Warning: reportlab not available, using simple text output")
            return self._generate_text_fallback(report, visual_paths)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def _get_risk_interpretation(self, risk_level: str) -> str:
        """Get narrative interpretation of risk level."""
        interpretations = {
            "Low": "indicating minimal operational risk and standard deployment protocols are appropriate. Regular monitoring should be sufficient to maintain model fairness and performance over time.",
            "Moderate": "suggesting potential regulatory and reputational risks that require targeted mitigation strategies. Enhanced monitoring and bias mitigation measures are recommended before full deployment.",
            "High": "indicating significant bias issues that pose substantial regulatory and business risks. Comprehensive mitigation plan and re-evaluation are required before any deployment consideration."
        }
        return interpretations.get(risk_level, "Risk level requires further analysis.")
    
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
            f.write(f"Total Rows: {dataset_overview.get('total_rows', 'N/A'):,}\n")
            f.write(f"Dataset Type: {dataset_overview.get('dataset_type', 'N/A')}\n")
            f.write(f"Target Column: {dataset_overview.get('target_column', 'N/A')}\n")
            
            return filename
