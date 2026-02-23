import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, Any

def safe_get(report, *keys, default=None):
    """Safely get nested dictionary values."""
    data = report
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key)
        if data is None:
            return default
    return data

def generate_dashboard(report: Dict[str, Any]):
    """
    Generate a 2x2 dashboard with 4 professional charts.
    
    Args:
        report: Combined report from Phase 4-6 analysis
        
    Returns:
        matplotlib figure object (not saved to disk)
    """
    # Create 2x2 grid layout
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.patch.set_facecolor('white')
    
    # Extract data using safe_get
    class_dist = safe_get(report, "ml_training", "class_imbalance_details", "class_distribution", default={})
    bias_breakdown = safe_get(report, "overall_risk", "breakdown", default={})
    overall_risk = safe_get(report, "overall_risk", default={})
    risk_percentile = safe_get(report, "phase6", "risk_percentile", default=None)
    market_position = safe_get(report, "phase6", "market_position", default="N/A")
    fingerprint = safe_get(report, "phase6", "profile", "fingerprint", default="Unavailable")
    domain = safe_get(report, "phase6", "profile", "domain", default="Unavailable")
    task = safe_get(report, "phase6", "profile", "task", default="Unavailable")
    size = safe_get(report, "phase6", "profile", "size", default="Unavailable")
    balance = safe_get(report, "phase6", "profile", "balance", default="Unavailable")
    dataset_overview = safe_get(report, "dataset_overview", default={})
    
    # === TOP-LEFT: Class Distribution ===
    ax = axes[0, 0]
    if class_dist:
        classes = list(class_dist.keys())
        counts = list(class_dist.values())
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c'][:len(classes)]
        
        bars = ax.bar(classes, counts, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        ax.set_title("Class Distribution", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Class", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(counts)*0.01,
                    f'{count:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Class Distribution", fontsize=12, fontweight='bold')
    
    # === TOP-RIGHT: Bias Components ===
    ax = axes[0, 1]
    
    # Debug output
    print(f"🔍 BIAS DEBUG: bias_breakdown = {bias_breakdown}")
    
    if bias_breakdown:
        components = list(bias_breakdown.keys())
        values = list(bias_breakdown.values())
        colors = ['#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][:len(components)]
        
        # Create horizontal bar chart
        y_pos = np.arange(len(components))
        bars = ax.barh(y_pos, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([comp.title() for comp in components])
        ax.set_xlabel("Risk Score", fontsize=10)
        ax.set_title("Bias Components", fontsize=12, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, values)):
            ax.text(val + max(values)*0.01, i, f'{val}', ha='left', va='center', fontsize=9, fontweight='bold')
        
        # Add bias analysis summary
        bias_analysis = report.get("bias_analysis", {})
        demographic_bias = bias_analysis.get("demographic_bias", {})
        linguistic_bias = bias_analysis.get("linguistic_bias", {})
        
        # Add bias detection status
        demo_detected = demographic_bias.get("detected", False)
        demo_score = demographic_bias.get("score", 0)
        demo_columns = demographic_bias.get("columns", [])
        
        ling_detected = linguistic_bias.get("detected", False)
        ling_score = linguistic_bias.get("score", 0)
        
        bias_summary = f"Demographic Bias: {'Detected' if demo_detected else 'Not Detected'} (Score: {demo_score:.2f})"
        if demo_columns:
            bias_summary += f" - Columns: {', '.join(demo_columns)}"
        
        bias_summary += f"\nLinguistic Bias: {'Detected' if ling_detected else 'Not Detected'} (Score: {ling_score:.2f})"
        
        ax.text(0.02, 0.98, bias_summary, transform=ax.transAxes, fontsize=8, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        print(f"🔍 BIAS CHART: Created with {len(components)} components")
    else:
        print("🔍 BIAS CHART: No bias_breakdown data available")
        ax.text(0.5, 0.5, 'Bias Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Bias Components", fontsize=12, fontweight='bold')
    
    # === BOTTOM-LEFT: Risk Breakdown ===
    ax = axes[1, 0]
    if overall_risk:
        risk_level = overall_risk.get("risk_level", "N/A")
        risk_percentage = overall_risk.get("risk_percentage", 0)
        
        # Create gauge-like visualization using bar chart
        risk_color = '#10b981' if risk_percentage < 25 else '#f59e0b' if risk_percentage < 75 else '#ef4444'
        
        # Background bar
        ax.barh(0, 100, height=0.5, color='lightgray', alpha=0.3)
        
        # Risk bar
        ax.barh(0, risk_percentage, height=0.5, color=risk_color, alpha=0.8)
        
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel("Risk Percentage", fontsize=10)
        ax.set_yticks([])
        ax.set_title(f"Risk Level: {risk_level}", fontsize=12, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add percentage text
        ax.text(risk_percentage, 0, f'{risk_percentage}%', ha='center', va='center', 
                fontsize=12, fontweight='bold', color='white')
        
        # Add risk level zones
        ax.axvspan(0, 25, alpha=0.1, color='green', label='Low')
        ax.axvspan(25, 75, alpha=0.1, color='orange', label='Medium')
        ax.axvspan(75, 100, alpha=0.1, color='red', label='High')
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Risk Breakdown", fontsize=12, fontweight='bold')
    
    # === BOTTOM-RIGHT: Dataset Size Analysis ===
    ax = axes[1, 1]
    if dataset_overview:
        total_rows = dataset_overview.get("total_rows", 0)
        available_columns = dataset_overview.get("available_columns", [])
        num_columns = len(available_columns) if available_columns else 0
        
        # Create dual bar chart for rows and columns
        categories = ['Total Rows', 'Total Columns']
        values = [total_rows, num_columns]
        colors = ['#3498db', '#e74c3c']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        ax.set_title("Dataset Size Analysis", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                    f'{value:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Add dataset type info
        dataset_type = dataset_overview.get("dataset_type", "Unknown")
        ax.text(0.5, -0.3, f'Dataset Type: {dataset_type.title()}', 
                ha='center', va='center', fontsize=9, style='italic', transform=ax.transData)
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Dataset Size Analysis", fontsize=12, fontweight='bold')
    
    # === GLOBAL TITLE AND STYLING ===
    fig.suptitle(
        "Dataset Intelligence Dashboard",
        fontsize=16,
        fontweight="bold",
        y=0.98,
        color='#1f2937'
    )
    
    # Style all subplots
    for ax in axes.flat:
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
    
    # Prevent overlap
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    return fig
