"""
Column Detection Module
Auto-detects target and text columns for ML training.
"""

import pandas as pd
from typing import Tuple, Optional, Dict, Any


class ColumnDetector:
    """Detects target and text columns in datasets."""
    
    def __init__(self):
        self.high_priority_targets = ['income', 'salary', 'price']
        self.medium_priority_targets = ['target', 'label', 'outcome', 'result', 'score']
        
    def detect_columns(self, df: pd.DataFrame) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Detect text and target columns with priority-based logic.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (text_column, target_column, detection_info)
        """
        available_columns = list(df.columns)
        
        target_col = self._detect_target_column(df)
        text_col = self._detect_text_column(df, target_col)
        
        detection_info = {
            'available_columns': available_columns,
            'detected_target': target_col,
            'target_priority': self._get_target_priority(target_col) if target_col else None,
            'detected_text': text_col
        }
        
        print(f"*** AVAILABLE COLUMNS: {available_columns} ***")
        if target_col:
            priority = self._get_target_priority(target_col)
            if priority == 'high':
                print(f"*** DETECTED HIGH PRIORITY TARGET: {target_col} ***")
            elif priority == 'medium':
                print(f"*** DETECTED MEDIUM PRIORITY TARGET: {target_col} ***")
            else:
                print(f"*** DETECTED LOW PRIORITY TARGET: {target_col} ***")
        
        print(f"*** FINAL SELECTION - Text: {text_col}, Target: {target_col} ***")
        return text_col, target_col, detection_info
    
    def _detect_target_column(self, df: pd.DataFrame) -> Optional[str]:
        """Detect target column with priority-based logic."""
        
        # Check high priority targets first (exact match)
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in self.high_priority_targets:
                print(f"*** DETECTED HIGH PRIORITY TARGET: {col} ***")
                return col
        
        # Then check medium priority
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in self.medium_priority_targets:
                print(f"*** DETECTED MEDIUM PRIORITY TARGET: {col} ***")
                return col
        
        # Look for binary/ordinal columns
        for col in df.columns:
            if df[col].dtype in ['object', 'category']:
                unique_vals = df[col].nunique()
                if unique_vals == 2 or (unique_vals <= 10 and df[col].dtype == 'object'):
                    print(f"Inferred target column: {col} (unique values: {unique_vals})")
                    return col
        
        # Last resort: use last column
        target_col = df.columns[-1]
        print(f"Using fallback target column: {target_col}")
        return target_col
    
    def _detect_text_column(self, df: pd.DataFrame, target_col: Optional[str]) -> Optional[str]:
        """Detect text column with NLP-specific criteria."""
        
        remaining_cols = [col for col in df.columns if col != target_col]
        
        for col in remaining_cols:
            if df[col].dtype == 'object':
                avg_length = df[col].str.len().mean()
                unique_count = df[col].nunique()
                unique_ratio = unique_count / len(df)
                has_spaces = df[col].str.contains(' ').any()
                
                # NLP text criteria: 
                # - Long strings (sentences, not categories)
                # - High cardinality (many unique values)
                # - Contains spaces (multiple words)
                # - High uniqueness ratio (not repetitive categories)
                if (avg_length > 100 and 
                    unique_count > 1000 and 
                    unique_ratio > 0.3 and 
                    has_spaces):
                    text_col = col
                    print(f"*** DETECTED TEXT COLUMN: {col} (avg_length: {avg_length:.1f}, unique: {unique_count}, ratio: {unique_ratio:.2f}) ***")
                    return text_col
        
        # No suitable text column found
        return None
    
    def _get_target_priority(self, target_col: str) -> str:
        """Get the priority level of detected target column."""
        if not target_col:
            return None
        
        col_lower = target_col.lower()
        if col_lower in self.high_priority_targets:
            return 'high'
        elif col_lower in self.medium_priority_targets:
            return 'medium'
        else:
            return 'low'
    
    def classify_dataset_type(self, df: pd.DataFrame, text_col: Optional[str]) -> str:
        """
        Classify dataset as NLP or tabular.
        
        Args:
            df: Input DataFrame
            text_col: Detected text column
            
        Returns:
            'nlp' or 'tabular'
        """
        if text_col and text_col in df.columns and df[text_col].dtype == 'object':
            avg_length = df[text_col].str.len().mean()
            unique_ratio = df[text_col].nunique() / len(df)
            
            # Stricter NLP criteria: long text, high uniqueness, multiple words
            if avg_length > 100 and unique_ratio > 0.5 and len(df.columns) <= 10:
                return 'nlp'
        
        return 'tabular'
