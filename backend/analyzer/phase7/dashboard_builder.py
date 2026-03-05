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
    """Generate a comprehensive dashboard figure."""
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    
    # Create figure with 3 charts layout (2x2 grid, but we'll use only 3)
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))  # Safe size for PDF
    fig.patch.set_facecolor('white')
    
    # Remove the top-right subplot (ML Algorithm Performance)
    fig.delaxes(axes[0, 1])
    
    # Debug: Check if axes are created properly
    print(f" DASHBOARD DEBUG: axes shape = {axes.shape}")
    print(f" DASHBOARD DEBUG: axes type = {type(axes)}")
    
    # Get the remaining 3 axes in correct order
    ax1 = axes[0, 0]  # Top-left (Class Distribution)
    ax2 = axes[1, 0]  # Bottom-left (Risk Breakdown)
    ax3 = axes[1, 1]  # Bottom-right (Dataset Size)
    
    # Create a list of the 3 axes
    axes = [ax1, ax2, ax3]
    
    # Extract data using safe_get
    class_dist = safe_get(report, "ml_training", "class_imbalance_details", "class_distribution", default={})
    bias_breakdown = safe_get(report, "overall_risk", "breakdown", default={})
    overall_risk = safe_get(report, "overall_risk", default={})
    dataset_overview = safe_get(report, "dataset_overview", default={})
    
    # Debug output for bias_breakdown
    print(f" BIAS DEBUG: bias_breakdown = {bias_breakdown}")
    print(f" BIAS DEBUG: overall_risk = {overall_risk}")
    
    # Additional debug for overall_risk structure
    if overall_risk:
        print(f" BIAS DEBUG: overall_risk keys = {list(overall_risk.keys())}")
        if 'breakdown' in overall_risk:
            print(f" BIAS DEBUG: breakdown keys = {list(overall_risk['breakdown'].keys())}")
    else:
        print(" BIAS DEBUG: No 'breakdown' key in overall_risk")
    
    # === TOP-LEFT: Class Distribution ===
    ax = axes[0]
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
        print(f" CLASS CHART: Created with {len(classes)} classes")
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Class Distribution", fontsize=12, fontweight='bold')
    
    # === BOTTOM-LEFT: Risk Breakdown ===
    ax = axes[1]
    if overall_risk:
        risk_level = overall_risk.get("risk_level", "N/A")
        risk_percentage = overall_risk.get("risk_percentage", 0)
        
        # Create gauge-like visualization using bar chart
        risk_color = '#10b981' if risk_percentage < 25 else '#f59e0b' if risk_percentage < 75 else '#ef4444'
        
        # Background bar
        ax.barh(0, 100, height=0.3, color='lightgray', alpha=0.3)
        
        # Risk percentage bar
        ax.barh(0, risk_percentage, height=0.3, color=risk_color, alpha=0.8)
        
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel("Risk Percentage", fontsize=10)
        ax.set_yticks([])
        ax.set_title("Risk Breakdown", fontsize=12, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add risk level text
        ax.text(risk_percentage, 0, f'{risk_percentage}th', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
        
        # Add risk level zones
        ax.axvspan(0, 25, alpha=0.1, color='green', label='Low')
        ax.axvspan(25, 75, alpha=0.1, color='orange', label='Medium')
        ax.axvspan(75, 100, alpha=0.1, color='red', label='High')
        print(f" RISK CHART: Created with {risk_percentage}% risk level")
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Risk Breakdown", fontsize=12, fontweight='bold')
    
    # === BOTTOM-RIGHT: Dataset Size Analysis ===
    ax = axes[2]
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
        print(f" DATASET CHART: Created with {total_rows} rows, {num_columns} columns")
    else:
        ax.text(0.5, 0.5, 'Data Not Available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Dataset Size Analysis", fontsize=12, fontweight='bold')
    
    # === GLOBAL STYLING ===
    # Removed global title as requested
    
    # Style all subplots
    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
    
    # Use regular tight_layout instead of with rect to avoid margin issues
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Adjust top margin for title
    
    print(f" DASHBOARD DEBUG: Final figure created successfully")
    return fig
