"""
Phase 7: Dataset Governance System

Visual engine for generating charts and reports from Phase 4-6 analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List
import os
from datetime import datetime


class VisualEngine:
    """Generate professional visualizations for bias analysis reports."""
    
    def __init__(self):
        self.output_dir = "outputs/visuals"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_all_visuals(self, report: Dict[str, Any]) -> List[str]:
        """
        Generate all required visualizations and return file paths.
        
        Args:
            report: Combined report from Phase 4-6 analysis
            
        Returns:
            List of generated image file paths
        """
        image_paths = []
        
        # 1. Class Distribution Bar Chart
        class_path = self._generate_class_distribution(report)
        if class_path:
            image_paths.append(class_path)
        
        # 2. Risk Breakdown Bar Chart
        risk_path = self._generate_risk_breakdown(report)
        if risk_path:
            image_paths.append(risk_path)
        
        # 3. Bias Component Chart
        bias_path = self._generate_bias_components(report)
        if bias_path:
            image_paths.append(bias_path)
        
        # 4. Risk Percentile Position Chart
        percentile_path = self._generate_percentile_chart(report)
        if percentile_path:
            image_paths.append(percentile_path)
        
        return image_paths
    
    def _generate_class_distribution(self, report: Dict[str, Any]) -> str:
        """Generate class distribution bar chart."""
        try:
            ml_training = report.get("ml_training", {})
            class_dist = ml_training.get("class_distribution", {})
            
            if not class_dist:
                return None
            
            plt.figure(figsize=(10, 6))
            classes = list(class_dist.keys())
            counts = list(class_dist.values())
            
            bars = plt.bar(classes, counts, color='#2E86AB', alpha=0.8)
            plt.title('Class Distribution', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Classes', fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for bar, count in zip(bars, counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        str(count), ha='center', va='bottom')
            
            plt.tight_layout()
            
            filename = f"{self.output_dir}/class_distribution.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating class distribution: {e}")
            return None
    
    def _generate_risk_breakdown(self, report: Dict[str, Any]) -> str:
        """Generate risk breakdown bar chart."""
        try:
            overall_risk = report.get("overall_risk", {})
            breakdown = overall_risk.get("breakdown", {})
            
            if not breakdown:
                return None
            
            plt.figure(figsize=(10, 6))
            components = list(breakdown.keys())
            values = list(breakdown.values())
            
            colors = ['#E74C3C', '#3498DB', '#2E86AB', '#F39C12', '#1ABC9C']
            bars = plt.bar(components, values, color=colors[:len(components)], alpha=0.8)
            plt.title('Risk Breakdown by Component', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Risk Components', fontsize=12)
            plt.ylabel('Risk Contribution (%)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', alpha=0.3)
            
            # Add value labels
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{value}%', ha='center', va='bottom')
            
            plt.tight_layout()
            
            filename = f"{self.output_dir}/risk_breakdown.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating risk breakdown: {e}")
            return None
    
    def _generate_bias_components(self, report: Dict[str, Any]) -> str:
        """Generate bias component chart."""
        try:
            bias_analysis = report.get("bias_analysis", {})
            
            # Extract bias scores
            demo_score = bias_analysis.get("demographic_bias", {}).get("score", 0)
            linguistic_score = bias_analysis.get("linguistic_bias", {}).get("score", 0)
            toxicity_score = bias_analysis.get("linguistic_bias", {}).get("toxicity_score", 0)
            sentiment_score = bias_analysis.get("linguistic_bias", {}).get("sentiment_gap", 0)
            
            plt.figure(figsize=(10, 6))
            components = ['Demographic', 'Linguistic', 'Toxicity', 'Sentiment']
            scores = [demo_score, linguistic_score, toxicity_score, sentiment_score]
            
            colors = ['#E74C3C', '#3498DB', '#F39C12', '#1ABC9C']
            bars = plt.bar(components, scores, color=colors, alpha=0.8)
            plt.title('Bias Component Analysis', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Bias Components', fontsize=12)
            plt.ylabel('Bias Score', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', alpha=0.3)
            
            # Add value labels
            for bar, score in zip(bars, scores):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{score:.3f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            filename = f"{self.output_dir}/bias_components.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating bias components: {e}")
            return None
    
    def _generate_percentile_chart(self, report: Dict[str, Any]) -> str:
        """Generate risk percentile position chart."""
        try:
            phase6_results = report.get("phase6_results", {})
            percentile = phase6_results.get("risk_percentile", 0)
            
            plt.figure(figsize=(10, 6))
            
            # Create percentile gauge chart
            categories = ['Low Risk', 'Moderate Risk', 'High Risk']
            positions = [25, 50, 75]  # Percentile positions
            
            # Current position
            current_pos = percentile
            current_color = '#2E86AB' if percentile <= 33 else '#F39C12' if percentile <= 66 else '#E74C3C'
            
            # Background zones
            plt.axvspan(0, 33, alpha=0.2, color='green', label='Low Risk Zone')
            plt.axvspan(33, 66, alpha=0.2, color='yellow', label='Moderate Risk Zone')
            plt.axvspan(66, 100, alpha=0.2, color='red', label='High Risk Zone')
            
            # Current position line
            plt.axvline(x=current_pos, color=current_color, linewidth=3, label=f'Current: {percentile}th percentile')
            
            plt.xlim(0, 100)
            plt.ylim(0, 1)
            plt.yticks([])
            plt.xlabel('Risk Percentile', fontsize=12)
            plt.title('Dataset Risk Position', fontsize=16, fontweight='bold', pad=20)
            plt.legend(loc='upper right')
            plt.grid(axis='x', alpha=0.3)
            
            plt.tight_layout()
            
            filename = f"{self.output_dir}/risk_percentile.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating percentile chart: {e}")
            return None
