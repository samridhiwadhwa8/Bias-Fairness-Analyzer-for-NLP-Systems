"""
Utility Functions Module
Common utility functions for the bias analyzer.
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any, List, Optional, Union
from io import StringIO


class Utils:
    """Utility functions for data processing and analysis."""
    
    @staticmethod
    def safe_load_csv(file_content: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Safely load CSV with encoding fallback.
        
        Args:
            file_content: CSV file content as string
            encoding: Initial encoding to try
            
        Returns:
            Loaded DataFrame
        """
        encodings = [encoding, 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for enc in encodings:
            try:
                return pd.read_csv(StringIO(file_content), encoding=enc)
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error loading CSV with encoding {enc}: {e}")
                continue
        
        # Last resort: try with errors='ignore'
        try:
            return pd.read_csv(StringIO(file_content), encoding='utf-8', errors='ignore')
        except Exception as e:
            raise ValueError(f"Could not load CSV with any encoding: {e}")
    
    @staticmethod
    def convert_for_json(data: Union[np.ndarray, list, dict]) -> Union[list, dict]:
        """
        Convert data to JSON-serializable format.
        
        Args:
            data: Data to convert
            
        Returns:
            JSON-serializable data
        """
        if hasattr(data, 'toarray'):
            return data.toarray().tolist()
        elif hasattr(data, 'tolist'):
            return data.tolist()
        elif isinstance(data, dict):
            return {
                key: Utils.convert_for_json(value) 
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [Utils.convert_for_json(item) for item in data]
        elif isinstance(data, (np.integer, np.floating)):
            return data.item()
        elif isinstance(data, pd.Series):
            return data.tolist()
        elif pd.api.types.is_numeric_dtype(data) and not isinstance(data, str):
            return float(data)
        elif isinstance(data, str) and data in ['int64', 'float64', 'int32', 'float32', 'object', 'bool']:
            # Don't convert dtype strings to numbers, return as-is
            return data
        else:
            return data
    
    @staticmethod
    def calculate_health_score(data_quality: Dict[str, Any], 
                             sensitive_columns: Dict[str, Any],
                             feature_correlation: Dict[str, Any]) -> float:
        """
        Calculate overall dataset health score.
        
        Args:
            data_quality: Data quality metrics
            sensitive_columns: Sensitive columns analysis
            feature_correlation: Correlation analysis
            
        Returns:
            Health score (0-100)
        """
        scores = []
        
        # Data quality score (40% weight)
        quality_score = data_quality.get('completeness_score', 0)
        scores.append(quality_score * 0.4)
        
        # Sensitive columns score (30% weight)  
        sensitive_count = sensitive_columns.get('count', 0)
        sensitive_score = max(0, 100 - (sensitive_count * 10))
        scores.append(sensitive_score * 0.3)
        
        # Correlation score (20% weight)
        corr_score = 100 if not feature_correlation.get('correlation_warning', False) else 70
        scores.append(corr_score * 0.2)
        
        # Type balance score (10% weight)
        type_balance = data_quality.get('completeness_score', 50)
        scores.append(type_balance * 0.1)
        
        return round(sum(scores), 1)
    
    @staticmethod
    def get_proactive_risk_assessment(df: pd.DataFrame, 
                                     data_quality: Dict[str, Any],
                                     sensitive_columns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get proactive risk assessment.
        
        Args:
            df: Input DataFrame
            data_quality: Data quality metrics
            sensitive_columns: Sensitive columns analysis
            
        Returns:
            Risk assessment dictionary
        """
        risk_factors = []
        confidence = 0.85  # Base confidence
        
        # Adjust confidence based on data quality
        if data_quality.get('total_missing_percentage', 0) > 20:
            confidence -= 0.1
        if data_quality.get('duplicate_rows_percentage', 0) > 5:
            confidence -= 0.05
        if sensitive_columns.get('count', 0) == 0:
            confidence -= 0.1
        
        # Ensure confidence stays within bounds
        confidence = max(0.5, min(0.95, confidence))
        
        # Check for missing data risk
        if data_quality.get('total_missing_percentage', 0) > 20:
            risk_factors.append(f"High missing data rate: {data_quality['total_missing_percentage']:.1f}%")
        
        # Check for sensitive data risk
        if sensitive_columns.get('count', 0) > 0:
            risk_factors.append(f"Contains {sensitive_columns['count']} sensitive columns")
        
        # Check for dataset size risk
        if len(df) < 1000:
            risk_factors.append("Small dataset size may affect model reliability")
        
        # Check for outlier risk
        if data_quality.get('outlier_percentage', 0) > 15:
            risk_factors.append(f"High outlier rate: {data_quality['outlier_percentage']:.1f}%")
        
        # Determine risk potential
        risk_score = len(risk_factors)
        if risk_score >= 3:
            bias_risk_potential = 'High'
        elif risk_score >= 1:
            bias_risk_potential = 'Medium'
        else:
            bias_risk_potential = 'Low'
        
        return {
            'bias_risk_potential': bias_risk_potential,
            'confidence': confidence,
            'risk_factors': risk_factors
        }
    
    @staticmethod
    def detect_demographic_columns(df: pd.DataFrame) -> List[tuple]:
        """
        Detect protected demographic columns by name patterns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            List of (type, column_name) tuples for legally protected attributes
        """
        # Protected attributes (legally sensitive) - stricter definition
        demographic_patterns = {
            'gender': ['gender', 'sex', 'male', 'female', 'man', 'woman', 'men', 'women'],
            'race': ['race', 'ethnicity', 'nationality', 'country', 'native-country'],
            'age': ['age', 'age_group', 'years', 'experience', 'birth_date', 'dob']
            # Note: Excluding education, workclass, income as they are not legally protected
        }
        
        detected = []
        for col in df.columns:
            col_lower = col.lower()
            for demo_type, patterns in demographic_patterns.items():
                if any(pattern in col_lower for pattern in patterns):
                    detected.append((demo_type, col))
                    break
        
        return detected
    
    @staticmethod
    def has_meaningful_target(df: pd.DataFrame, target_col: str) -> bool:
        """
        Check if dataset has meaningful predictive target vs demographic comparison.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            
        Returns:
            True if meaningful target, False if demographic comparison
        """
        if not target_col or target_col not in df.columns:
            return False
        
        # Check for demographic comparison patterns
        target_lower = target_col.lower()
        
        # Patterns indicating demographic comparison, not prediction
        demographic_patterns = [
            'salary', 'income', 'wage', 'pay', 'earnings',
            'men', 'women', 'male', 'female', 'gender'
        ]
        
        # If target contains demographic terms and data looks like comparisons
        if any(pattern in target_lower for pattern in demographic_patterns):
            # Check if other columns suggest comparison structure
            comparison_cols = 0
            for col in df.columns:
                col_lower = col.lower()
                if any(pattern in col_lower for pattern in ['men', 'women', 'male', 'female', 'gender']):
                    comparison_cols += 1
            
            # If we have gender-specific columns, it's likely a comparison dataset
            if comparison_cols >= 2:
                return False
        
        # Default to meaningful target
        return True
    
    @staticmethod
    def load_metadata(metadata_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load dataset metadata for intelligent bias detection.
        
        Args:
            metadata_path: Path to metadata file
            
        Returns:
            Metadata dictionary
        """
        if not metadata_path:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            metadata_path = os.path.join(current_dir, '..', '..', 'datasets', 'meta.json')
        
        try:
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("Metadata file not found, using default detection")
                return {"auto_detection_rules": {
                    "gender_columns": ["gender", "sex", "male", "female", "man", "woman"],
                    "age_columns": ["age", "age_group", "age_of_user", "years", "experience"],
                    "socioeconomic_columns": ["income", "salary", "education", "workclass", "class", "occupation"],
                    "race_columns": ["race", "ethnicity", "nationality", "country"]
                }}
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return {"auto_detection_rules": {}}
    
    @staticmethod
    def get_dataset_info(metadata: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """
        Get metadata for a specific dataset with fuzzy matching.
        
        Args:
            metadata: Metadata dictionary
            filename: Dataset filename
            
        Returns:
            Dataset metadata
        """
        if not metadata:
            return {}
        
        # Try exact match first
        if filename in metadata:
            return metadata[filename]
        
        # Try fuzzy matching
        filename_lower = filename.lower()
        for meta_filename, meta_info in metadata.items():
            meta_lower = meta_filename.lower()
            if (meta_lower in filename_lower or 
                filename_lower in meta_lower or
                filename_lower.replace('.csv', '') == meta_lower.replace('.csv', '') or
                meta_lower.replace('.csv', '') in filename_lower.replace('.csv', '')):
                return meta_info
        
        # Return default metadata if no match found
        return {
            'domain': 'Unknown',
            'bias_risk_level': 'medium',
            'description': f'Analysis of {filename} dataset',
            'known_sensitive_attributes': [],
            'use_cases': ['General analysis', 'Bias detection', 'ML training']
        }
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame for analysis requirements.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Validation results
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check if DataFrame is empty
        if df.empty:
            validation_results['is_valid'] = False
            validation_results['errors'].append("DataFrame is empty")
            return validation_results
        
        # Check minimum rows
        if len(df) < 10:
            validation_results['warnings'].append("Dataset has fewer than 10 rows")
            validation_results['recommendations'].append("Consider collecting more data for reliable analysis")
        
        # Check for columns
        if len(df.columns) < 2:
            validation_results['warnings'].append("Dataset has fewer than 2 columns")
            validation_results['recommendations'].append("Dataset should have at least one feature and one target column")
        
        # Check for all-NaN columns
        nan_columns = df.columns[df.isnull().all()].tolist()
        if nan_columns:
            validation_results['warnings'].append(f"Columns with all NaN values: {nan_columns}")
            validation_results['recommendations'].append("Consider removing or imputing all-NaN columns")
        
        return validation_results
