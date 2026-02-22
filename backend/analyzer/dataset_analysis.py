"""
Dataset Analysis Module
Performs basic dataset analysis and quality assessment.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class DatasetAnalyzer:
    """Analyzes dataset structure and quality."""
    
    def __init__(self):
        pass
    
    def get_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get basic dataset information.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with basic dataset info
        """
        data_types = {}
        for col, dtype in df.dtypes.items():
            data_types[col] = str(dtype)
        
        return {
            'total_rows': int(len(df)),
            'total_columns': int(len(df.columns)),
            'memory_usage_mb': float(df.memory_usage(deep=True).sum() / (1024**2)),
            'dataset_size_bytes': int(len(df.to_csv(index=False).encode('utf-8'))),
            'columns': df.columns.tolist(),
            'data_types': data_types
        }
    
    def analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze data quality metrics.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with data quality metrics
        """
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        missing_percentage = (missing_cells / total_cells) * 100
        
        # Outlier detection
        outlier_count = 0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].notna().sum() > 0:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_count += len(outliers)
        
        outlier_percentage = (outlier_count / total_cells) * 100 if total_cells > 0 else 0
        
        return {
            'total_missing_percentage': missing_percentage,
            'outlier_percentage': outlier_percentage,
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_rows_percentage': (df.duplicated().sum() / len(df)) * 100 if len(df) > 0 else 0,
            'completeness_score': max(0, 100 - missing_percentage)
        }
    
    def analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze feature correlations.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with correlation analysis
        """
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) < 2:
            return {'correlation_warning': False, 'high_correlations': []}
        
        correlation_matrix = numeric_df.corr()
        high_corr_pairs = []
        
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = abs(correlation_matrix.iloc[i, j])
                if corr_value > 0.8:  # High correlation threshold
                    high_corr_pairs.append({
                        'feature1': correlation_matrix.columns[i],
                        'feature2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        return {
            'correlation_warning': len(high_corr_pairs) > 0,
            'high_correlations': high_corr_pairs[:5]  # Top 5 correlations
        }
    
    def classify_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Classify data types in the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with data type classification
        """
        type_counts = {'numeric': 0, 'categorical': 0, 'datetime': 0, 'boolean': 0, 'text': 0}
        text_columns = []
        numeric_columns = []
        
        for col in df.columns:
            if df[col].dtype in [np.int64, np.float64, np.int32, np.float32]:
                type_counts['numeric'] += 1
                numeric_columns.append(col)
            elif df[col].dtype == 'bool':
                type_counts['boolean'] += 1
            elif 'datetime' in str(df[col].dtype):
                type_counts['datetime'] += 1
            elif df[col].dtype == 'object':
                # Check if it's ACTUAL NLP text or just categorical strings
                avg_length = df[col].str.len().mean()
                unique_ratio = df[col].nunique() / len(df)
                has_spaces = df[col].str.contains(' ').any()
                
                # NLP text criteria: long strings, high uniqueness, contains spaces
                if avg_length > 30 and unique_ratio > 0.1 and has_spaces:
                    type_counts['text'] += 1
                    text_columns.append(col)
                else:
                    type_counts['categorical'] += 1
        
        # Determine primary type
        if type_counts['text'] > 0:
            primary_type = 'TEXT'
            classification = 'NLP Text Classification'
        elif type_counts['numeric'] > 0 and type_counts['categorical'] > 0:
            primary_type = 'Structured Tabular (Numeric + Categorical)'
            classification = 'Mixed'
        elif type_counts['numeric'] > 0:
            primary_type = 'Numeric'
            classification = 'Numeric'
        else:
            primary_type = 'Categorical'
            classification = 'Categorical'
        
        return {
            'type_counts': type_counts,
            'text_columns': len(text_columns),
            'numeric_columns': len(numeric_columns),
            'primary_type': primary_type,
            'classification': classification
        }
    
    def get_class_imbalance(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """
        Analyze class distribution in target column.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            
        Returns:
            Dictionary with class imbalance metrics
        """
        if target_col not in df.columns:
            return {'imbalance_ratio': 0.0, 'max_class_percentage': 0.0, 'min_class_percentage': 0.0}
        
        class_counts = df[target_col].value_counts()
        
        if len(class_counts) <= 1:
            return {'imbalance_ratio': 0.0, 'max_class_percentage': 100.0, 'min_class_percentage': 100.0}
        
        # Calculate imbalance ratio
        max_count = class_counts.max()
        min_count = class_counts.min()
        imbalance_ratio = max_count / min_count
        
        # Cap at reasonable maximum
        imbalance_ratio = min(imbalance_ratio, 5.0)
        
        # Calculate percentages
        total_samples = len(df)
        max_class_percentage = (max_count / total_samples) * 100
        min_class_percentage = (min_count / total_samples) * 100
        
        # Get class names
        max_class_name = class_counts.idxmax()
        min_class_name = class_counts.idxmin()
        
        return {
            'imbalance_ratio': round(imbalance_ratio, 2),
            'max_class_percentage': round(max_class_percentage, 1),
            'min_class_percentage': round(min_class_percentage, 1),
            'class_distribution': class_counts.to_dict(),
            'max_class_name': max_class_name,
            'min_class_name': min_class_name,
            'max_class_count': int(max_count),
            'min_class_count': int(min_count)
        }
    
    def get_column_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get detailed column analysis.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with column analysis
        """
        column_analysis = {}
        
        for col in df.columns:
            col_info = {
                'type': 'text' if df[col].dtype == 'object' else 'number',
                'unique_values': int(df[col].nunique()),
                'missing_percentage': float(df[col].isnull().sum() / len(df) * 100) if len(df) > 0 else 0,
                'sample_values': df[col].dropna().head(5).tolist()
            }
            
            if df[col].dtype in [np.int64, np.float64, np.int32, np.float32]:
                col_info.update({
                    'min': float(df[col].min()) if df[col].notna().any() else 0,
                    'max': float(df[col].max()) if df[col].notna().any() else 0,
                    'mean': float(df[col].mean()) if df[col].notna().any() else 0,
                    'std': float(df[col].std()) if df[col].notna().any() else 0
                })
            elif df[col].dtype == 'object':
                col_info.update({
                    'avg_length': float(df[col].astype(str).str.len().mean()) if df[col].notna().any() else 0,
                    'max_length': int(df[col].astype(str).str.len().max()) if df[col].notna().any() else 0
                })
            
            column_analysis[col] = col_info
        
        return column_analysis
