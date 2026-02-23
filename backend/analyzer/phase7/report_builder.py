"""
Phase 7: Dataset Governance System

Professional PDF report builder with in-memory image embedding.
"""

from typing import Dict, Any
from datetime import datetime
import os
import io
import tempfile
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
    
    def generate_pdf_report(self, report: Dict[str, Any], figures: Dict[str, Any]) -> str:
        """
        Generate comprehensive PDF report with embedded visualizations.
        
        Args:
            report: Combined report from Phase 4-6 analysis
            figures: Dictionary of matplotlib figure objects
            
        Returns:
            Path to generated PDF file
        """
        import tempfile
        try:
            # Test reportlab import first
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            # Create PDF document
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            filename = f"{self.output_dir}/bias_governance_report_{timestamp.replace(':', '-')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom title style
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor=colors.black
            )
            
            # === PAGE 1: Cover Page ===
            story.append(Paragraph("Dataset Intelligence & Bias Governance Report", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
            story.append(Paragraph("System Version: Phase 7 Professional v1.0", styles['Normal']))
            story.append(Spacer(1, 40))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            phase5_results = report.get("phase5_results", {})
            if phase5_results:
                exec_summary = phase5_results.get("executive_summary", {})
                assessment = exec_summary.get('overall_assessment', 'N/A')
                
                # Professional narrative summary
                dataset_overview = report.get("dataset_overview", {})
                total_rows = dataset_overview.get('total_rows', 0)
                dataset_type = dataset_overview.get('dataset_type', 'unknown').upper()
                
                narrative = f"This report presents a structured bias and risk assessment of the dataset used for predictive modeling. "
                
                if dataset_type == 'TABULAR':
                    narrative += f"The dataset contains {total_rows:,} observations and is classified as a structured tabular dataset. "
                elif dataset_type == 'NLP':
                    narrative += f"The dataset contains {total_rows:,} observations and is classified as an NLP dataset. "
                else:
                    narrative += f"The dataset contains {total_rows:,} observations and is classified as a {dataset_type.lower()} dataset. "
                
                overall_risk = report.get("overall_risk", {})
                risk_level = overall_risk.get('risk_level', 'N/A')
                risk_percentage = overall_risk.get('risk_percentage', 0)
                
                narrative += f"Overall bias risk is assessed as {risk_level.lower()} ({risk_percentage}%), "
                
                # Add specific bias findings
                bias_analysis = report.get("bias_analysis", {})
                demographic_bias = bias_analysis.get("demographic_bias", {})
                linguistic_bias = bias_analysis.get("linguistic_bias", {})
                
                if demographic_bias.get("detected"):
                    narrative += f"with demographic bias detected in {', '.join(demographic_bias.get('columns', []))}. "
                else:
                    narrative += f"with no demographic bias patterns detected. "
                
                if linguistic_bias.get("detected"):
                    narrative += f"Linguistic bias was identified with a score of {linguistic_bias.get('score', 0):.2f}. "
                else:
                    narrative += f"No linguistic bias patterns were detected. "
                
                # Add class imbalance context
                ml_training = report.get("ml_training", {})
                imbalance_ratio = ml_training.get('class_imbalance_ratio', 0)
                if imbalance_ratio > 1.5:
                    narrative += f"Moderate class imbalance (ratio: {imbalance_ratio:.2f}) was identified as the primary risk factor. "
                else:
                    narrative += f"Class balance is acceptable (ratio: {imbalance_ratio:.2f}). "
                
                # Add benchmarking info
                phase6_results = report.get("phase6_results", {})
                if phase6_results:
                    percentile = phase6_results.get("risk_percentile", 0)
                    position = phase6_results.get("market_position", 'N/A')
                    narrative += f"Based on ecosystem benchmarking, the dataset falls within the {percentile}th risk percentile ({position}), "
                
                # Add deployment decision
                deployment = phase5_results.get("deployment", {})
                decision = deployment.get("deployment_decision", "Pending")
                confidence = deployment.get("confidence_score", 0)
                
                narrative += f"and deployment with standard monitoring is recommended with {int(confidence * 100)}% confidence."
                
                story.append(Paragraph(narrative, styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Key Insights
                key_insights = exec_summary.get('key_insights', [])
                if key_insights:
                    story.append(Paragraph("Key Findings:", styles['Heading3']))
                    for insight in key_insights:
                        story.append(Paragraph(f"• {insight}", styles['Normal']))
                    story.append(Spacer(1, 20))
            
            story.append(PageBreak())
            
            # === PAGE 2: Dataset Overview ===
            story.append(Paragraph("Dataset Overview", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            dataset_overview = report.get("dataset_overview", {})
            ml_training = report.get("ml_training", {})
            
            # Dataset explanation
            total_rows = dataset_overview.get('total_rows', 0)
            dataset_type = dataset_overview.get('dataset_type', 'unknown')
            target_column = dataset_overview.get('target_column', 'N/A')
            available_columns = dataset_overview.get('available_columns', [])
            
            explanation = f"The dataset consists of {total_rows:,} records with {len(available_columns)} features, "
            explanation += f"designed for {dataset_type.lower()} analysis. "
            explanation += f"The target variable '{target_column}' represents the prediction objective. "
            
            # Add imbalance explanation
            imbalance_ratio = ml_training.get('class_imbalance_ratio', 0)
            if imbalance_ratio > 1.5:
                explanation += f"The class imbalance ratio of {imbalance_ratio:.2f} indicates moderate imbalance between classes, "
                explanation += f"which may impact model performance and requires careful consideration during training and evaluation."
            else:
                explanation += f"The class distribution is well-balanced (ratio: {imbalance_ratio:.2f}), "
                explanation += f"providing a solid foundation for unbiased model training."
            
            story.append(Paragraph(explanation, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Dataset information table
            overview_data = [
                ['Metric', 'Value'],
                ['Total Rows', f"{total_rows:,}"],
                ['Dataset Type', dataset_type.title()],
                ['Target Column', target_column],
                ['Available Features', str(len(available_columns))],
                ['Class Imbalance Ratio', f"{imbalance_ratio:.2f}"],
                ['Imbalance Interpretation', 'Moderate' if imbalance_ratio > 1.5 else 'Balanced']
            ]
            
            table = Table(overview_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 30))
            
            # Embed Class Distribution Chart
            if figures.get("class_distribution"):
                story.append(Paragraph("Class Distribution Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(Paragraph("The following chart illustrates the distribution of classes in the dataset, providing insight into potential imbalance issues that may affect model training and performance evaluation.", styles['Normal']))
                story.append(Spacer(1, 12))
                img = self._embed_figure(figures["class_distribution"])
                if img:
                    story.append(img)
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # === PAGE 3: Model Performance ===
            story.append(Paragraph("Model Performance", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            # Model metrics explanation
            model = ml_training.get('model', 'Random Forest')
            f1_score = ml_training.get('f1_score', 0)
            accuracy = ml_training.get('accuracy', 0)
            
            # Fix accuracy formatting - avoid double multiplication
            if accuracy > 1:
                accuracy_formatted = f"{accuracy:.1f}%"
            else:
                accuracy_formatted = f"{accuracy * 100:.1f}%"
            
            performance_desc = 'moderate' if f1_score < 0.8 else 'good'
            
            explanation = f"The {model} model achieved {accuracy_formatted} accuracy with an F1 score of {f1_score:.3f}, "
            explanation += f"indicating {performance_desc} predictive capability across classes. "
            
            if f1_score > 0.8:
                explanation += f"The high F1 score suggests balanced performance in both precision and recall, "
                explanation += f"indicating the model handles class distributions effectively."
            elif f1_score > 0.6:
                explanation += f"The F1 score indicates reasonable performance, though there may be room for improvement "
                explanation += f"through feature engineering or hyperparameter tuning."
            else:
                explanation += f"The F1 score suggests challenges in achieving balanced predictions, "
                explanation += f"requiring further analysis and potential model adjustments."
            
            story.append(Paragraph(explanation, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Performance metrics table
            metrics_data = [
                ['Metric', 'Value', 'Interpretation'],
                ['Accuracy', accuracy_formatted, 'Overall correct predictions'],
                ['F1 Score', f"{f1_score:.3f}", 'Balance of precision and recall'],
                ['Model Type', model, 'Algorithm used'],
                ['Class Imbalance', f"{ml_training.get('class_imbalance_ratio', 0):.2f}", 'Dataset balance ratio']
            ]
            
            metrics_table = Table(metrics_data)
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 30))
            
            # Embed Confusion Matrix
            if figures.get("confusion_matrix"):
                story.append(Paragraph("Confusion Matrix Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(Paragraph("The confusion matrix provides detailed insight into model performance by showing correct and incorrect classifications for each class. This visualization helps identify specific areas where the model may be struggling and informs targeted improvements.", styles['Normal']))
                story.append(Spacer(1, 12))
                img = self._embed_figure(figures["confusion_matrix"])
                if img:
                    story.append(img)
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # === PAGE 4: Bias Analysis ===
            story.append(Paragraph("Bias Analysis", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            bias_analysis = report.get("bias_analysis", {})
            overall_risk = report.get("overall_risk", {})
            
            # Bias summary explanation
            risk_level = overall_risk.get('risk_level', 'N/A')
            risk_percentage = overall_risk.get('risk_percentage', 0)
            
            explanation = f"The comprehensive bias analysis reveals a {risk_level.lower()} overall risk level of {risk_percentage}%. "
            
            # Add component analysis
            breakdown = overall_risk.get('breakdown', {})
            if breakdown:
                max_component = max(breakdown.items(), key=lambda x: x[1])
                explanation += f"The primary contributor to this risk assessment is {max_component[0]} bias at {max_component[1]}%, "
                explanation += f"which requires focused attention in the mitigation strategy."
            
            story.append(Paragraph(explanation, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Bias summary table
            bias_summary_data = [
                ['Component', 'Risk Score', 'Status', 'Impact'],
                ['Overall Risk', f"{risk_percentage}%", risk_level, 'High' if risk_percentage > 30 else 'Medium' if risk_percentage > 15 else 'Low']
            ]
            
            # Add breakdown components
            for component, score in breakdown.items():
                status = 'Critical' if score > 30 else 'Moderate' if score > 15 else 'Low'
                impact = 'High' if score > 30 else 'Medium' if score > 15 else 'Low'
                bias_summary_data.append([component.title(), f"{score}%", status, impact])
            
            bias_table = Table(bias_summary_data)
            bias_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(bias_table)
            story.append(Spacer(1, 30))
            
            # Embed Bias Components Chart
            if figures.get("bias_components"):
                story.append(Paragraph("Bias Component Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(Paragraph("This visualization breaks down the bias analysis into key components, highlighting which areas contribute most to the overall risk assessment and require targeted mitigation efforts.", styles['Normal']))
                story.append(Spacer(1, 12))
                img = self._embed_figure(figures["bias_components"])
                if img:
                    story.append(img)
                story.append(Spacer(1, 20))
            
            # Embed Risk Breakdown Chart
            if figures.get("risk_breakdown"):
                story.append(Paragraph("Risk Breakdown Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(Paragraph("The risk breakdown chart provides a detailed view of how different bias types contribute to the overall risk score, enabling precise identification of mitigation priorities.", styles['Normal']))
                story.append(Spacer(1, 12))
                img = self._embed_figure(figures["risk_breakdown"])
                if img:
                    story.append(img)
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # === PAGE 5: Risk Intelligence ===
            story.append(Paragraph("Risk Intelligence", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            phase6_results = report.get("phase6_results", {})
            if phase6_results:
                profile = phase6_results.get("profile", {})
                percentile = phase6_results.get("risk_percentile", 0)
                position = phase6_results.get("market_position", 'N/A')
                
                # Risk intelligence explanation
                explanation = f"The risk intelligence assessment places this dataset at the {percentile}th percentile among similar datasets, "
                explanation += f"indicating {position.lower()}. "
                
                if percentile < 25:
                    explanation += f"This exceptional positioning suggests the dataset exhibits lower bias characteristics than approximately {100-percentile}% of comparable datasets."
                elif percentile < 50:
                    explanation += f"This favorable positioning indicates the dataset demonstrates better bias characteristics than the median dataset."
                elif percentile < 75:
                    explanation += f"This positioning suggests the dataset exhibits moderate bias characteristics that fall within the typical range."
                else:
                    explanation += f"This elevated positioning indicates the dataset exhibits higher bias characteristics than most comparable datasets."
                
                story.append(Paragraph(explanation, styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Dataset fingerprint table
                fingerprint_data = [
                    ['Characteristic', 'Value'],
                    ['Dataset Fingerprint', profile.get('fingerprint', 'N/A')],
                    ['Domain', profile.get('domain', 'N/A')],
                    ['Task Type', profile.get('task', 'N/A')],
                    ['Dataset Size', profile.get('size', 'N/A')],
                    ['Balance Status', profile.get('balance', 'N/A')],
                    ['Risk Percentile', f"{percentile}%"],
                    ['Market Position', position]
                ]
                
                fingerprint_table = Table(fingerprint_data)
                fingerprint_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(fingerprint_table)
                story.append(Spacer(1, 30))
            
            # Embed Percentile Chart
            if figures.get("risk_percentile"):
                story.append(Paragraph("Risk Percentile Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(Paragraph("This visualization shows the dataset's risk position relative to the broader ecosystem of similar datasets, providing context for the risk assessment and deployment decision.", styles['Normal']))
                story.append(Spacer(1, 12))
                img = self._embed_figure(figures["risk_percentile"])
                if img:
                    story.append(img)
                story.append(Spacer(1, 20))
            
            story.append(PageBreak())
            
            # === PAGE 6: Mitigation & Deployment ===
            story.append(Paragraph("Mitigation & Deployment", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            if phase5_results:
                mitigation = phase5_results.get("mitigation", {})
                deployment = phase5_results.get("deployment", {})
                
                # Mitigation explanation
                actions = mitigation.get("recommended_actions", [])
                if actions:
                    explanation = f"Based on the comprehensive bias analysis, {len(actions)} key mitigation actions are recommended to address identified risks. "
                    explanation += f"These actions range from technical interventions to process improvements, with an estimated implementation timeline of {mitigation.get('estimated_timeline', 'N/A')}. "
                    explanation += f"The implementation complexity is assessed as {mitigation.get('implementation_complexity', 'N/A')}."
                    
                    story.append(Paragraph(explanation, styles['Normal']))
                    story.append(Spacer(1, 20))
                
                # Mitigation details table
                mitigation_data = [
                    ['Aspect', 'Details'],
                    ['Recommended Actions', f"{len(actions)} strategies identified"],
                    ['Implementation Timeline', mitigation.get('estimated_timeline', 'N/A')],
                    ['Complexity', mitigation.get('implementation_complexity', 'N/A')],
                    ['Priority', 'High' if risk_level == 'High' else 'Medium' if risk_level == 'Moderate' else 'Low']
                ]
                
                mitigation_table = Table(mitigation_data)
                mitigation_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(mitigation_table)
                story.append(Spacer(1, 30))
                
                # Detailed Actions
                story.append(Paragraph("Recommended Mitigation Actions", styles['Heading2']))
                story.append(Spacer(1, 12))
                for i, action in enumerate(actions[:5], 1):
                    story.append(Paragraph(f"{i}. {action}", styles['Normal']))
                    story.append(Spacer(1, 8))
                
                story.append(Spacer(1, 20))
                
                # Final Deployment Decision
                story.append(Paragraph("Final Deployment Decision", styles['Heading2']))
                story.append(Spacer(1, 15))
                
                decision = deployment.get("deployment_decision", "Pending")
                confidence = deployment.get("confidence_score", 0)
                
                # Bold decision statement
                decision_color = "#00AA00" if "Deploy" in decision else "#AA0000"
                decision_style = ParagraphStyle('FinalDecision', parent=styles['Heading2'], 
                                                textColor=colors.HexColor(decision_color),
                                                fontSize=16,
                                                spaceAfter=20)
                story.append(Paragraph(decision.upper(), decision_style))
                
                # Decision explanation
                if "Deploy" in decision:
                    decision_explanation = f"The dataset and model are approved for deployment with {int(confidence * 100)}% confidence. "
                    decision_explanation += "Standard monitoring protocols should be implemented to ensure ongoing bias detection and performance tracking."
                elif "Proceed" in decision:
                    decision_explanation = f"The dataset is approved for deployment with enhanced monitoring, with {int(confidence * 100)}% confidence. "
                    decision_explanation += "Additional bias mitigation measures should be implemented before full production deployment."
                else:
                    decision_explanation = f"Deployment is not recommended at this time due to identified bias risks. "
                    decision_explanation += f"Comprehensive mitigation and re-evaluation are required before deployment consideration."
                
                story.append(Paragraph(decision_explanation, styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Confidence indicator
                confidence_data = [
                    ['Metric', 'Value'],
                    ['Decision Confidence', f"{int(confidence * 100)}%"],
                    ['Risk Level', risk_level],
                    ['Deployment Status', decision]
                ]
                
                confidence_table = Table(confidence_data)
                confidence_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(confidence_table)
            
            # Build PDF
            try:
                doc.build(story)
                print(f"✅ PDF generated successfully: {filename}")
                return filename
            except Exception as pdf_error:
                print(f"❌ PDF build error: {pdf_error}")
                return None
            
        except ImportError as e:
            print(f"❌ ReportLab import error: {e}")
            print("❌ CRITICAL: ReportLab is required for PDF generation!")
            return None
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return None
    
    def _embed_figure(self, fig):
        """Embed matplotlib figure into PDF using in-memory buffer."""
        try:
            import io
            from reportlab.platypus import Image
            from reportlab.lib.units import inch
            
            # Save figure to in-memory buffer
            buffer = io.BytesIO()
            fig.savefig(buffer, format='PNG', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            
            # Create image from buffer
            img = Image(buffer)
            img.drawWidth = 5*inch
            img.drawHeight = 3.5*inch
            
            # Close the figure to free memory
            import matplotlib.pyplot as plt
            plt.close(fig)
            
            return img
            
        except Exception as e:
            print(f"❌ Error embedding figure: {e}")
            return None
