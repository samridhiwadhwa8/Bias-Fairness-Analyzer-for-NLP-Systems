"""
Bias Analysis Report Schema
Clean, startup-ready JSON schema for frontend display.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class BiasAnalysisReport:
    """Clean, production-safe bias analysis report schema."""
    
    # Dataset Overview
    dataset_overview: Dict[str, Any]
    
    # Data Quality
    data_quality: Dict[str, Any]
    
    # ML Training (nullable)
    ml_training: Optional[Dict[str, Any]]
    
    # Bias Analysis
    bias_analysis: Dict[str, Any]
    
    # Overall Risk
    overall_risk: Dict[str, Any]
    
    # Recommendations
    recommendations: List[str]
    
    @classmethod
    def from_analysis_results(cls, analysis_results: Dict[str, Any]) -> 'BiasAnalysisReport':
        """Create report from analysis results."""
        
        try:
            # Dataset Overview
            basic_info = analysis_results.get('basic_info', {})
            detected_columns = analysis_results.get('detected_columns', {})
            
            dataset_overview = {
                'total_rows': basic_info.get('total_rows', 0),
                'total_columns': basic_info.get('total_columns', 0),
                'dataset_size_mb': round(basic_info.get('memory_usage_mb', 0), 2),
                'dataset_type': analysis_results.get('dataset_type', 'unknown'),
                'target_column': detected_columns.get('target_column'),
                'text_column': detected_columns.get('text_column'),
                'available_columns': detected_columns.get('available_columns', []),
                'target_priority': detected_columns.get('target_priority'),
                'detection_info': detected_columns.get('detection_info', {})
            }
            
            # Data Quality
            data_quality_raw = analysis_results.get('data_quality', {})

            missing_val = data_quality_raw.get('total_missing_percentage', 0)
            outlier_val = data_quality_raw.get('outlier_percentage', 0)
            completeness_val = data_quality_raw.get('completeness_score', 0)
            
            data_quality = {
                'missing_percentage': round(float(missing_val), 1),
                'duplicate_rows': int(data_quality_raw.get('duplicate_rows', 0)),
                'outlier_percentage': (
                    round(float(outlier_val), 1)
                    if analysis_results.get('dataset_type') == 'tabular'
                    else None
                ),
                'completeness_score': round(float(completeness_val), 1)
            }
            
            # ML Training (nullable)
            ml_training_raw = analysis_results.get('ml_training', {})
            ml_training = None
            
            if ml_training_raw and ml_training_raw.get('success') and ml_training_raw.get('model_trained') is not False:
                # Handle accuracy/precision values that might be strings
                acc_val = ml_training_raw.get('accuracy_percentage', '0%')
                prec_val = ml_training_raw.get('precision_percentage', '0%')
                rec_val = ml_training_raw.get('recall_percentage', '0%')
                
                # Convert to float, handling both string and numeric types
                try:
                    accuracy = float(str(acc_val).replace('%', ''))
                except (ValueError, TypeError):
                    accuracy = 0.0
                    
                try:
                    precision = float(str(prec_val).replace('%', ''))
                except (ValueError, TypeError):
                    precision = 0.0
                    
                try:
                    recall = float(str(rec_val).replace('%', ''))
                except (ValueError, TypeError):
                    recall = 0.0
                
                # Get class imbalance details for display
                class_imbalance_info = analysis_results.get('class_imbalance', {})
                class_ratio = class_imbalance_info.get('imbalance_ratio', 0)
                max_class_pct = class_imbalance_info.get('max_class_percentage', 0)
                min_class_pct = class_imbalance_info.get('min_class_percentage', 0)
                class_distribution = class_imbalance_info.get('class_distribution', {})
                
                ml_training = {
                    'model_name': ml_training_raw.get('model', 'Unknown'),
                    'selection_reason': ml_training_raw.get('selection_reason', 'Not specified'),
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': round(ml_training_raw.get('f1_score', 0), 3),
                    'class_imbalance_ratio': class_ratio,
                    'class_imbalance_details': {
                        'ratio': class_ratio,
                        'max_class_percentage': max_class_pct,
                        'min_class_percentage': min_class_pct,
                        'class_distribution': class_distribution
                    }
                }
            
            # Bias Analysis
            bias_raw = analysis_results.get('bias_analysis', {})
            dataset_type = analysis_results.get('dataset_type', 'tabular')
            
            if dataset_type == 'nlp':
                # Safe conversions for NLP scores
                try:
                    linguistic_score = float(bias_raw.get('linguistic_score', 0))
                except (ValueError, TypeError):
                    linguistic_score = 0.0
                
                try:
                    toxicity_score = float(str(bias_raw.get('toxicity_score', 0)))
                except (ValueError, TypeError):
                    toxicity_score = 0.0
                    
                try:
                    sentiment_score = float(str(bias_raw.get('sentiment_score', 0)))
                except (ValueError, TypeError):
                    sentiment_score = 0.0
                    
                try:
                    gender_pronoun_score = float(str(bias_raw.get('gender_pronoun_score', 0)))
                except (ValueError, TypeError):
                    gender_pronoun_score = 0.0
                
                bias_analysis = {
                    'demographic_bias': {
                        'detected': False,
                        'score': 0.0,
                        'columns': []
                    },
                    'linguistic_bias': {
                        'detected': True,
                        'score': round(linguistic_score, 3),
                        'toxicity_score': round(toxicity_score, 3),
                        'sentiment_gap': round(sentiment_score, 3),
                        'gender_language_imbalance': round(gender_pronoun_score, 3)
                    }
                }
            else:
                demo_cols = analysis_results.get('detected_columns', {}).get('demographic_columns', [])
                
                # Safe conversion of demographic_score
                demo_score_raw = bias_raw.get('demographic_score', 0)
                try:
                    demo_score = float(str(demo_score_raw))
                except (ValueError, TypeError):
                    demo_score = 0.0
                    print(f"Warning: Could not convert demographic_score '{demo_score_raw}' to float, using 0.0")
                
                # Extract column names properly from demographic columns
                print(f"DEBUG: demo_cols type: {type(demo_cols)}")
                print(f"DEBUG: demo_cols content: {demo_cols}")
                
                if isinstance(demo_cols, list) and len(demo_cols) > 0:
                    if isinstance(demo_cols[0], dict):
                        # Already formatted as dictionaries
                        columns = [col['column'] for col in demo_cols]
                    elif isinstance(demo_cols[0], tuple):
                        # Need to extract column name from tuples
                        columns = [col[1] for col in demo_cols]  # (demo_type, col_name)
                        print(f"DEBUG: Extracted from tuples: {columns}")
                    elif isinstance(demo_cols[0], list):
                        # Double detection happened - extract unique column names
                        all_columns = []
                        for col_list in demo_cols:
                            if isinstance(col_list, list):
                                all_columns.extend(col_list)
                            else:
                                all_columns.append(col_list)
                        columns = list(set(all_columns))  # Remove duplicates
                        print(f"DEBUG: Double detection detected, unique columns: {columns}")
                    else:
                        # Already strings
                        columns = demo_cols
                        print(f"DEBUG: Already strings: {columns}")
                else:
                    columns = []
                
                print(f"DEBUG: extracted columns: {columns}")
                
                bias_analysis = {
                    'demographic_bias': {
                        'detected': demo_score > 0.1,  # Only flag as detected if score > threshold
                        'score': round(demo_score, 3),
                        'columns': columns
                    },
                    'linguistic_bias': {
                        'detected': False,
                        'score': 0.0,
                        'toxicity_score': 0.0,
                        'sentiment_gap': 0.0,
                        'gender_language_imbalance': 0.0
                    }
                }
            
            print("=== REPORT SCHEMA: BIAS ANALYSIS COMPLETED ===")
            
            # Overall Risk
            risk_raw = analysis_results.get('risk_assessment', {})
            component_scores = risk_raw.get('component_scores', {})
            
            overall_risk = {
                'risk_level': risk_raw.get('risk_level', 'Low'),
                'risk_percentage': round(risk_raw.get('risk_percentage', 0), 1),
                'component_scores': {
                    'demographic': round(component_scores.get('demographic', 0), 3),
                    'linguistic': round(component_scores.get('linguistic', 0), 3),
                    'toxicity': round(component_scores.get('toxicity', 0), 3),
                    'sentiment': round(component_scores.get('sentiment', 0), 3),
                    'class_imbalance': round(component_scores.get('class_imbalance', 0), 3)
                }
            }
            
            # Recommendations
            recommendations = analysis_results.get('risk_summary', {}).get('recommendations', [])
            
            return cls(
                dataset_overview=dataset_overview,
                data_quality=data_quality,
                ml_training=ml_training,
                bias_analysis=bias_analysis,
                overall_risk=overall_risk,
                recommendations=recommendations
            )
            
        except Exception as e:
            print(f"=== REPORT SCHEMA ERROR ===")
            print(f"Error: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            
            # Return a basic safe report if conversion fails
            return cls(
                dataset_overview={'total_rows': 0, 'total_columns': 0, 'dataset_size_mb': 0, 'dataset_type': 'unknown'},
                data_quality={'missing_percentage': 0, 'duplicate_rows': 0, 'outlier_percentage': None, 'completeness_score': 0},
                ml_training=None,
                bias_analysis={'demographic_bias': {'detected': False, 'score': 0.0, 'columns': []}, 'linguistic_bias': {'detected': False, 'score': 0.0}},
                overall_risk={'risk_level': 'Unknown', 'risk_percentage': 0, 'component_scores': {}},
                recommendations=[f'Error generating report: {str(e)}']
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'dataset_overview': self.dataset_overview,
            'data_quality': self.data_quality,
            'ml_training': self.ml_training,
            'bias_analysis': self.bias_analysis,
            'overall_risk': self.overall_risk,
            'recommendations': self.recommendations
        }


    def get_example_report() -> Dict[str, Any]:
     """Get example report for frontend development."""
    
     return {
        "dataset_overview": {
            "total_rows": 10000,
            "total_columns": 15,
            "dataset_size_mb": 2.5,
            "dataset_type": "tabular",
            "target_column": "income",
            "text_column": None
        },
        "data_quality": {
            "missing_percentage": 5.2,
            "duplicate_rows": 12,
            "outlier_percentage": 8.7,
            "completeness_score": 94.8
        },
        "ml_training": {
            "model_name": "Random Forest",
            "selection_reason": "Medium tabular dataset (10,000 rows) with 2 classes - robust for mixed feature types",
            "accuracy": 85.3,
            "precision": 84.7,
            "recall": 85.3,
            "f1_score": 0.847,
            "class_imbalance_ratio": 1.8
        },
        "bias_analysis": {
            "demographic_bias": {
                "detected": True,
                "score": 0.342,
                "columns": ["gender", "age", "education"]
            },
            "linguistic_bias": {
                "detected": False,
                "score": 0.0,
                "toxicity_score": 0.0,
                "sentiment_gap": 0.0,
                "gender_language_imbalance": 0.0
            }
        },
        "overall_risk": {
            "risk_level": "Moderate",
            "risk_percentage": 42.5,
            "component_scores": {
                "demographic": 0.342,
                "linguistic": 0.0,
                "toxicity": 0.0,
                "sentiment": 0.0,
                "class_imbalance": 0.180
            }
        },
        "recommendations": [
            "Consider bias mitigation techniques",
            "Review sensitive attribute handling",
            "Consider re-sampling techniques for class imbalance"
        ]
    }


def get_example_report() -> Dict[str, Any]:
    """Get example report for frontend development."""
    return {
        'dataset_overview': {
            'total_rows': 1000,
            'total_columns': 15,
            'dataset_size_mb': 2.5,
            'dataset_type': 'tabular',
            'target_column': 'income',
            'text_column': None,
            'available_columns': ['age', 'workclass', 'fnlwgt', 'education', 'educational-num', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'],
            'target_priority': 'high',
            'detection_info': {'detection_method': 'high_priority_match'}
        },
        'data_quality': {
            'missing_percentage': 5.2,
            'duplicate_rows': 12,
            'outlier_percentage': 8.1,
            'completeness_score': 94.8
        },
        'ml_training': {
            'model_name': 'RandomForestClassifier',
            'selection_reason': 'Best performance on validation data',
            'accuracy': 85.7,
            'precision': 84.2,
            'recall': 87.1,
            'f1_score': 0.856,
            'class_imbalance_ratio': 3.18
        },
        'bias_analysis': {
            'demographic_bias': {
                'detected': True,
                'score': 0.234,
                'columns': ['gender', 'age', 'race', 'education']
            },
            'linguistic_bias': {
                'detected': False,
                'score': 0.0,
                'toxicity_score': 0.0,
                'sentiment_gap': 0.0,
                'gender_language_imbalance': 0.0
            }
        },
        'overall_risk': {
            'risk_level': 'Medium',
            'risk_percentage': 23.4,
            'component_scores': {
                'demographic': 14.0,  # 0.234 * 0.60
                'linguistic': 0.0,
                'toxicity': 0.0,
                'sentiment': 0.0,
                'class_imbalance': 9.4    # 3.18 * 0.30 * 100
            }
        },
        'recommendations': [
            "Monitor demographic bias in model predictions",
            "Consider bias mitigation techniques",
            "Review sensitive attribute handling",
            "Consider re-sampling techniques for class imbalance"
        ]
    }
