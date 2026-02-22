"""
Tabular Bias Analysis Module
Detects demographic and class imbalance bias in tabular datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict

# Try to import Fairlearn, but don't fail if not available
try:
    from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference
    from sklearn.metrics import accuracy_score
    FAIRLEARN_AVAILABLE = True
except ImportError:
    FAIRLEARN_AVAILABLE = False


class TabularBiasAnalyzer:
    """Analyzes bias in tabular datasets."""
    
    def __init__(self):
        # Protected attributes (legally sensitive) - stricter definition
        self.demographic_patterns = {
            'gender': ['gender', 'sex', 'male', 'female', 'man', 'woman', 'men', 'women'],
            'race': ['race', 'ethnicity', 'nationality', 'country', 'native-country'],
            'age': ['age', 'age_group', 'years', 'experience', 'birth_date', 'dob']
            # Note: Excluding education, workclass, income as they are not legally protected
        }
    
    def analyze_bias(self, df: pd.DataFrame, target_col: str, 
                    demographic_cols: List[tuple], y_test: List, y_pred: List) -> Dict[str, Any]:
        """
        Perform comprehensive tabular bias analysis.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            demographic_cols: List of demographic column tuples
            y_test: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary with bias analysis results
        """
        print(f"Performing tabular bias analysis with {len(demographic_cols)} demographic columns")
        
        # Detect demographic columns if not provided
        if not demographic_cols:
            demographic_cols = self._detect_demographic_columns(df)
        
        # Calculate individual bias components
        demographic_score = self._analyze_demographic_bias(df, target_col, demographic_cols)
        class_imbalance_score = self._analyze_class_imbalance(df, target_col)
        
        # Calculate fairness metrics if Fairlearn is available
        fairness_metrics = self._calculate_fairness_metrics(df, target_col, demographic_cols, y_test, y_pred)
        
        # Overall demographic bias score
        overall_demographic_score = (demographic_score + class_imbalance_score) / 2
        
        return {
            'bias_type': 'Tabular Demographic Bias',
            'demographic_score': round(demographic_score, 3),
            'class_imbalance_score': round(class_imbalance_score, 3),
            'overall_demographic_score': round(overall_demographic_score, 3),
            'demographic_columns_found': len(demographic_cols),
            'demographic_columns': self._format_demographic_columns(demographic_cols),
            'fairness_metrics': fairness_metrics,
            'analysis_details': {
                'demographic_distributions': self._get_demographic_distributions(df, demographic_cols),
                'class_distribution': self._get_class_distribution(df, target_col),
                'bias_indicators': self._identify_bias_indicators(df, demographic_cols, target_col)
            }
        }
    
    def _detect_demographic_columns(self, df: pd.DataFrame) -> List[Tuple[str, str]]:
        """Detect demographic columns by name patterns."""
        detected = []
        
        for col in df.columns:
            col_lower = col.lower()
            for demo_type, patterns in self.demographic_patterns.items():
                if any(pattern in col_lower for pattern in patterns):
                    detected.append((demo_type, col))
                    break
        
        return detected
    
    def _analyze_demographic_bias(self, df: pd.DataFrame, target_col: str, 
                                 demographic_cols: List[Tuple[str, str]]) -> float:
        """Analyze demographic bias in the dataset."""
        if not demographic_cols:
            return 0.0
        
        bias_scores = []
        
        for demo_type, col_name in demographic_cols:
            if col_name not in df.columns:
                continue
            
            # Calculate representation bias
            col_data = df[col_name].dropna()
            if len(col_data) == 0:
                continue
            
            # For categorical columns
            if df[col_name].dtype == 'object':
                value_counts = col_data.value_counts()
                if len(value_counts) > 1:
                    # Calculate imbalance ratio
                    majority = value_counts.max()
                    minority = value_counts.min()
                    imbalance = (majority - minority) / len(col_data)
                    bias_scores.append(min(imbalance, 1.0))
            
            # For numeric columns (like age, income)
            elif df[col_name].dtype in [np.int64, np.float64, np.int32, np.float32]:
                # Check for skewed distribution
                q25 = col_data.quantile(0.25)
                q75 = col_data.quantile(0.75)
                median = col_data.median()
                
                # Calculate skewness indicator
                if median < q25 or median > q75:
                    skewness = abs(median - col_data.mean()) / col_data.std()
                    bias_scores.append(min(skewness / 3, 1.0))  # Normalize and cap
            
            # For boolean columns
            elif df[col_name].dtype == 'bool':
                # Treat boolean as categorical
                value_counts = col_data.value_counts()
                if len(value_counts) > 1:
                    majority = value_counts.max()
                    minority = value_counts.min()
                    imbalance = (majority - minority) / len(col_data)
                    bias_scores.append(min(imbalance, 1.0))
            
            # Skip other types (datetime, etc.)
            else:
                continue
        
        return np.mean(bias_scores) if bias_scores else 0.0
    
    def _analyze_class_imbalance(self, df: pd.DataFrame, target_col: str) -> float:
        """Analyze class imbalance in target variable."""
        if target_col not in df.columns:
            return 0.0
        
        class_counts = df[target_col].value_counts()
        if len(class_counts) <= 1:
            return 0.0
        
        # Calculate imbalance ratio
        majority = class_counts.max()
        minority = class_counts.min()
        total = len(df)
        
        # Imbalance score: 0 = balanced, 1 = completely imbalanced
        imbalance_score = (majority - minority) / total
        
        return min(imbalance_score, 1.0)
    
    def _calculate_fairness_metrics(self, df: pd.DataFrame, target_col: str,
                                   demographic_cols: List[Tuple[str, str]], 
                                   y_test: List, y_pred: List) -> Dict[str, Any]:
        """Calculate fairness metrics using Fairlearn if available."""
        if not FAIRLEARN_AVAILABLE or not demographic_cols or not y_test or not y_pred:
            return {
                'fairlearn_available': False,
                'demographic_parity': None,
                'equalized_odds': None,
                'message': 'Fairlearn not available or insufficient data for fairness metrics'
            }
        
        try:
            fairness_results = {}
            
            for demo_type, col_name in demographic_cols[:2]:  # Limit to first 2 demographic columns
                if col_name not in df.columns:
                    continue
                
                # Get demographic attribute for test set
                # Note: This assumes the test set is a subset of the original df
                # In practice, you'd need to track which rows were in the test set
                demo_attr = df[col_name].dropna().head(len(y_test))
                
                if len(demo_attr) != len(y_test):
                    continue
                
                # Calculate demographic parity difference
                dp_diff = demographic_parity_difference(
                    y_test, y_pred, sensitive_features=demo_attr
                )
                
                # Calculate equalized odds difference
                eo_diff = equalized_odds_difference(
                    y_test, y_pred, sensitive_features=demo_attr
                )
                
                fairness_results[f'{demo_type}_{col_name}'] = {
                    'demographic_parity_difference': round(dp_diff, 4),
                    'equalized_odds_difference': round(eo_diff, 4)
                }
            
            return {
                'fairlearn_available': True,
                'metrics': fairness_results
            }
            
        except Exception as e:
            return {
                'fairlearn_available': True,
                'error': f'Fairness metrics calculation failed: {str(e)}',
                'metrics': {}
            }
    
    def _format_demographic_columns(self, demographic_cols: List[Tuple[str, str]]) -> List[Dict[str, str]]:
        """Format demographic columns for output."""
        return [
            {'type': demo_type, 'column': col_name}
            for demo_type, col_name in demographic_cols
        ]
    
    def _get_demographic_distributions(self, df: pd.DataFrame, 
                                      demographic_cols: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Get distribution statistics for demographic columns."""
        distributions = {}
        
        for demo_type, col_name in demographic_cols:
            if col_name not in df.columns:
                continue
            
            col_data = df[col_name].dropna()
            
            if df[col_name].dtype == 'object':
                # Categorical distribution
                value_counts = col_data.value_counts()
                distributions[f'{demo_type}_{col_name}'] = {
                    'type': 'categorical',
                    'distribution': value_counts.to_dict(),
                    'unique_values': len(value_counts),
                    'most_common': value_counts.index[0] if len(value_counts) > 0 else None
                }
            else:
                # Numeric distribution
                distributions[f'{demo_type}_{col_name}'] = {
                    'type': 'numeric',
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'mean': float(col_data.mean()),
                    'median': float(col_data.median()),
                    'std': float(col_data.std()),
                    'quartiles': {
                        'q25': float(col_data.quantile(0.25)),
                        'q50': float(col_data.quantile(0.50)),
                        'q75': float(col_data.quantile(0.75))
                    }
                }
        
        return distributions
    
    def _get_class_distribution(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """Get class distribution for target variable."""
        if target_col not in df.columns:
            return {}
        
        class_counts = df[target_col].value_counts()
        total = len(df)
        
        return {
            'distribution': class_counts.to_dict(),
            'total_samples': total,
            'class_percentages': {
                str(cls): round(count / total * 100, 2) 
                for cls, count in class_counts.items()
            },
            'imbalance_ratio': round(class_counts.max() / class_counts.min(), 2) if class_counts.min() > 0 else float('inf')
        }
    
    def _identify_bias_indicators(self, df: pd.DataFrame, demographic_cols: List[Tuple[str, str]], 
                                 target_col: str) -> List[str]:
        """Identify potential bias indicators in the dataset."""
        indicators = []
        
        # Check for missing demographic data
        for demo_type, col_name in demographic_cols:
            if col_name in df.columns:
                missing_pct = (df[col_name].isnull().sum() / len(df)) * 100
                if missing_pct > 20:
                    indicators.append(f"High missing data in {col_name}: {missing_pct:.1f}%")
        
        # Check for class imbalance
        if target_col in df.columns:
            class_counts = df[target_col].value_counts()
            if len(class_counts) > 1:
                imbalance = (class_counts.max() - class_counts.min()) / len(df)
                if imbalance > 0.3:
                    indicators.append(f"High class imbalance in {target_col}: {imbalance:.2f}")
        
        # Check for demographic skew
        for demo_type, col_name in demographic_cols:
            if col_name in df.columns and df[col_name].dtype == 'object':
                value_counts = df[col_name].value_counts()
                if len(value_counts) > 1:
                    skew = (value_counts.max() - value_counts.min()) / len(df)
                    if skew > 0.4:
                        indicators.append(f"Demographic skew in {col_name}: {skew:.2f}")
        
        return indicators
