"""
ML Engine Module
Handles model training and evaluation with auto-selection.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from typing import Dict, Any, Tuple, Optional, Union
import pickle


class MLEngine:
    """Machine Learning engine for model training and evaluation."""
    
    def __init__(self):
        self.vectorizer = None
        self.preprocessor = None
        self.label_encoder = None
    
    def select_model(self, dataset_type: str, n_classes: int, dataset_size: int) -> Dict[str, Any]:
        """
        Select appropriate model based on dataset characteristics.
        
        Args:
            dataset_type: 'nlp' or 'tabular'
            n_classes: Number of target classes
            dataset_size: Number of samples
            
        Returns:
            Dictionary with model selection info
        """
        if dataset_type == 'nlp':
            if n_classes == 2:
                return {
                    'model': LogisticRegression,
                    'name': 'Logistic Regression',
                    'reason': f'NLP binary classification with {n_classes} classes - optimal for balanced sentiment tasks'
                }
            else:
                return {
                    'model': MultinomialNB,
                    'name': 'Multinomial Naive Bayes',
                    'reason': f'NLP multi-class classification with {n_classes} classes - stable baseline for TF-IDF features'
                }
        else:  # tabular
            if dataset_size > 10000:
                return {
                    'model': GradientBoostingClassifier,
                    'name': 'Gradient Boosting',
                    'reason': f'Large tabular dataset ({dataset_size:,} rows) with {n_classes} classes - gradient boosting for complex patterns'
                }
            else:
                return {
                    'model': RandomForestClassifier,
                    'name': 'Random Forest',
                    'reason': f'Medium tabular dataset ({dataset_size:,} rows) with {n_classes} classes - robust for mixed feature types'
                }
    
    def prepare_data(self, df: pd.DataFrame, text_col: Optional[str], target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for ML training.
        
        Args:
            df: Input DataFrame
            text_col: Text column name (if any)
            target_col: Target column name
            
        Returns:
            Tuple of (X, y) prepared for training
        """
        if text_col:
            # Text dataset: Use text column as DataFrame
            X = df[[text_col]].fillna('')
            print(f"Using text column: {text_col}")
        else:
            # Categorical + numeric: Use all columns except target
            feature_cols = [col for col in df.columns if col != target_col]
            X = df[feature_cols].fillna('Unknown')
            print(f"Using feature columns: {feature_cols}")
        
        y = df[target_col].fillna('Unknown')
        
        # Handle missing values in target
        mask = y != 'Unknown'
        X = X[mask]
        y = y[mask]
        
        return X, y
    
    def engineer_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame, 
                         text_col: Optional[str], model_class) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform feature engineering.
        
        Args:
            X_train: Training features
            X_test: Test features
            text_col: Text column name (if any)
            model_class: Model class for feature selection
            
        Returns:
            Tuple of (X_train_vec, X_test_vec) transformed features
        """
        if text_col and text_col in X_train.columns:
            # Text features
            if model_class == MultinomialNB:
                self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
            else:
                self.vectorizer = TfidfVectorizer(max_features=300, stop_words='english')
            
            X_train_vec = self.vectorizer.fit_transform(X_train[text_col])
            X_test_vec = self.vectorizer.transform(X_test[text_col])
        else:
            # Tabular features
            categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
            
            transformers = []
            if numeric_cols:
                transformers.append(('num', StandardScaler(), numeric_cols))
            if categorical_cols:
                transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols))
            
            if transformers:
                self.preprocessor = ColumnTransformer(transformers=transformers)
                X_train_vec = self.preprocessor.fit_transform(X_train)
                X_test_vec = self.preprocessor.transform(X_test)
            else:
                X_train_vec = X_train.values
                X_test_vec = X_test.values
        
        return X_train_vec, X_test_vec
    
    def encode_labels(self, y_train: pd.Series, y_test: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encode target labels.
        
        Args:
            y_train: Training labels
            y_test: Test labels
            
        Returns:
            Tuple of encoded labels
        """
        self.label_encoder = LabelEncoder()
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        y_test_encoded = self.label_encoder.transform(y_test)
        
        return y_train_encoded, y_test_encoded
    
    def train_model(self, model_class, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """
        Train ML model.
        
        Args:
            model_class: Model class to instantiate
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Trained model
        """
        # MultinomialNB doesn't accept random_state parameter
        if model_class == MultinomialNB:
            model = model_class()
        else:
            model = model_class(random_state=42)
        model.fit(X_train, y_train)
        return model
    
    def evaluate_model(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Evaluate trained model.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Tuple of (predictions, metrics)
        """
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Get class names for classification report
        if self.label_encoder:
            target_names = [str(name) for name in self.label_encoder.classes_]
        else:
            target_names = None
        
        # Generate classification report
        class_report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True, zero_division=0)
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        cm_labels = target_names if target_names else list(range(len(np.unique(y_test))))
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'classification_report': class_report,
            'confusion_matrix': {
                'matrix': cm.tolist(),
                'labels': cm_labels
            }
        }
        
        return y_pred, metrics
    
    def train_and_evaluate(self, df: pd.DataFrame, text_col: Optional[str], 
                          target_col: str, dataset_type: str) -> Dict[str, Any]:
        """
        Complete ML training and evaluation pipeline.
        
        Args:
            df: Input DataFrame
            text_col: Text column name (if any)
            target_col: Target column name
            dataset_type: 'nlp' or 'tabular'
            
        Returns:
            Dictionary with training results
        """
        try:
            # Prepare data
            X, y = self.prepare_data(df, text_col, target_col)
            
            if len(X) < 10:
                return {
                    'success': False,
                    'error': 'Insufficient data after cleaning',
                    'dataset_ml_ready': False
                }
            
            # Split data
            if len(X) < 20:
                return {
                    'success': False,
                    'error': 'Insufficient data for train-test split',
                    'dataset_ml_ready': False
                }
            
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
                print(f"Stratified split: {len(X_train)} training, {len(X_test)} testing samples")
            except ValueError:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                print(f"Regular split: {len(X_train)} training, {len(X_test)} testing samples")
            
            # Encode labels
            y_train_encoded, y_test_encoded = self.encode_labels(y_train, y_test)
            
            # Select model
            n_classes = len(df[target_col].unique())
            dataset_size = len(df)
            model_selection = self.select_model(dataset_type, n_classes, dataset_size)
            
            print(f"*** SELECTED MODEL: {model_selection['name']} ***")
            print(f"*** SELECTION REASON: {model_selection['reason']} ***")
            
            # Feature engineering
            X_train_vec, X_test_vec = self.engineer_features(X_train, X_test, text_col, model_selection['model'])
            
            # Train model
            model = self.train_model(model_selection['model'], X_train_vec, y_train_encoded)
            
            # Evaluate
            y_pred, metrics = self.evaluate_model(model, X_test_vec, y_test_encoded)
            
            # Convert predictions back to original labels
            if self.label_encoder:
                y_pred_original = self.label_encoder.inverse_transform(y_pred)
                y_test_original = self.label_encoder.inverse_transform(y_test_encoded)
            else:
                y_pred_original = y_pred
                y_test_original = y_test_encoded
            
            return {
                'success': True,
                'model': model_selection['name'],
                'model_type': model_selection['name'],
                'selection_reason': model_selection['reason'],
                'text_column': text_col,
                'target_column': target_col,
                'X_test': self._convert_for_json(X_test_vec),
                'y_test': y_test_original.tolist(),
                'y_pred': y_pred_original.tolist(),
                'accuracy_percentage': f"{metrics['accuracy'] * 100:.1f}%",
                'precision_percentage': f"{metrics['precision'] * 100:.1f}%",
                'recall_percentage': f"{metrics['recall'] * 100:.1f}%",
                'f1_score': metrics['f1_score'],
                'confusion_matrix': metrics['confusion_matrix'],
                'classification_report': metrics['classification_report']
            }
            
        except Exception as e:
            print(f"ML Training Error: {e}")
            return {
                'success': False,
                'error': f'ML training failed: {str(e)}',
                'dataset_ml_ready': False,
                'y_pred': [],
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'confusion_matrix': {'matrix': [], 'labels': []},
                'classification_report': {}
            }
    
    def _convert_for_json(self, data: np.ndarray) -> list:
        """Convert numpy array to JSON-serializable format."""
        if hasattr(data, 'toarray'):
            # Sparse matrix
            return data.toarray().tolist()
        else:
            # Dense array
            return data.tolist()
