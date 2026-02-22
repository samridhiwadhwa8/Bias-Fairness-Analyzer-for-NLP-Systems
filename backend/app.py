"""
Bias Analyzer API
Clean, modular FastAPI backend for bias detection and analysis.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import pandas as pd
import json
import os
from typing import Dict, Any, Optional

# Import analyzer modules
from analyzer import (
    ColumnDetector,
    DatasetAnalyzer as DatasetAnalyzerModule,
    MLEngine,
    NLPBiasAnalyzer,
    TabularBiasAnalyzer,
    RiskEngine,
    utils
)
from analyzer.report_schema import BiasAnalysisReport

# Import Phase 5 API routes
from api.phase5_routes import router as phase5_router

# Import Phase 6 API routes  
from api.phase6_routes import router as phase6_router

# Initialize FastAPI app
app = FastAPI(
    title="Bias Analyzer API",
    description="Clean, modular bias detection and analysis system",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Phase 5 routes
app.include_router(phase5_router)
app.include_router(phase6_router)

# Initialize analyzer components
column_detector = ColumnDetector()
dataset_analyzer = DatasetAnalyzerModule()
ml_engine = MLEngine()
nlp_bias_analyzer = NLPBiasAnalyzer()
tabular_bias_analyzer = TabularBiasAnalyzer()
risk_engine = RiskEngine()

# Load metadata
metadata = utils.Utils.load_metadata()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Bias Analyzer API v2.0",
        "description": "Clean, modular bias detection and analysis system",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze (POST)",
            "upload": "/upload (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "components": {
            "column_detector": "active",
            "dataset_analyzer": "active",
            "ml_engine": "active",
            "nlp_bias_analyzer": "active",
            "tabular_bias_analyzer": "active",
            "risk_engine": "active"
        }
    }


@app.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    """
    Analyze uploaded dataset for bias.
    
    Args:
        file: CSV file to analyze
        
    Returns:
        Complete bias analysis results
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read file content
        file_content = await file.read()
        file_str = file_content.decode('utf-8')
        
        # Load CSV with encoding fallback
        df = utils.Utils.safe_load_csv(file_str)
        
        # Validate DataFrame
        validation = utils.Utils.validate_dataframe(df)
        if not validation['is_valid']:
            raise HTTPException(status_code=400, detail=validation['errors'])
        
        print(f"Starting analysis for {file.filename}")
        
        # Phase 1: Basic Dataset Analysis
        dataset_info = utils.Utils.get_dataset_info(metadata, file.filename)
        basic_info = dataset_analyzer.get_basic_info(df)
        data_quality = dataset_analyzer.analyze_data_quality(df)
        feature_correlation = dataset_analyzer.analyze_correlations(df)
        data_type_classification = dataset_analyzer.classify_data_types(df)
        column_analysis = dataset_analyzer.get_column_analysis(df)
        
        # Phase 2: Column Detection and ML Training
        text_col, target_col, column_detection_info = column_detector.detect_columns(df)
        dataset_type = column_detector.classify_dataset_type(df, text_col)
        
        # Detect demographic columns using tabular analyzer's method for consistency
        from analyzer.bias_tabular import TabularBiasAnalyzer
        tabular_analyzer = TabularBiasAnalyzer()
        demographic_cols = tabular_analyzer._detect_demographic_columns(df)
        
        # Check if meaningful target for ML
        has_meaningful_target = utils.Utils.has_meaningful_target(df, target_col)
        
        # ML Training (only if meaningful target)
        ml_results = None
        if has_meaningful_target:
            ml_results = ml_engine.train_and_evaluate(df, text_col, target_col, dataset_type)
        else:
            ml_results = {
                'success': True,
                'model_trained': False,
                'reason': 'Dataset appears to be demographic disparity analysis - ML modeling not appropriate',
                'dataset_type': 'Demographic Disparity Analysis'
            }
        
        # Phase 3: Bias Analysis (based on dataset type)
        bias_results = None
        if dataset_type == 'nlp':
            bias_results = nlp_bias_analyzer.analyze_bias(df, text_col, target_col, demographic_cols)
        else:
            # Get test predictions if available
            y_test = ml_results.get('y_test', []) if ml_results else []
            y_pred = ml_results.get('y_pred', []) if ml_results else []
            bias_results = tabular_bias_analyzer.analyze_bias(df, target_col, demographic_cols, y_test, y_pred)
        
        # Phase 4: Class Imbalance Analysis
        class_imbalance = dataset_analyzer.get_class_imbalance(df, target_col)
        
        # Phase 5: Risk Assessment
        # Initialize demo_score for both NLP and tabular cases
        demo_score = 0.0
        
        if dataset_type == 'nlp':
            risk_assessment = risk_engine.calculate_risk(
                linguistic_score=bias_results.get('linguistic_score', 0),
                toxicity_score=bias_results.get('toxicity_score', 0),
                sentiment_score=bias_results.get('sentiment_score', 0),
                class_imbalance_ratio=class_imbalance.get('imbalance_ratio', 0),
                dataset_type=dataset_type,
                has_demographic_columns=len(demographic_cols) > 0
            )
        else:
            # Ensure demographic_score is a float
            demo_score_raw = bias_results.get('demographic_score', 0)
            try:
                demo_score = float(str(demo_score_raw))
            except (ValueError, TypeError):
                demo_score = 0.0
                print(f"Warning: Could not convert demographic_score '{demo_score_raw}' to float, using 0.0")
            
            risk_assessment = risk_engine.calculate_risk(
                demographic_score=demo_score,
                class_imbalance_ratio=class_imbalance.get('imbalance_ratio', 0),
                dataset_type=dataset_type,
                has_demographic_columns=len(demographic_cols) > 0
            )
            
        # Debug: Print what we're sending to risk engine
        print(f"*** DEBUG: Risk Assessment Input ***")
        print(f"Dataset Type: {dataset_type}")
        print(f"Demographic Score: {demo_score}")
        print(f"Class Imbalance Ratio: {class_imbalance.get('imbalance_ratio', 0)}")
        print(f"Has Demographic Columns: {len(demographic_cols) > 0}")
        print(f"Risk Assessment Result: {risk_assessment}")
        
        # Get risk summary
        risk_summary = risk_engine.get_risk_summary(risk_assessment)
        
        # Phase 6: Health Score and Proactive Assessment
        health_score = utils.Utils.calculate_health_score(data_quality, {'count': len(demographic_cols)}, feature_correlation)
        proactive_risk = utils.Utils.get_proactive_risk_assessment(df, data_quality, {'count': len(demographic_cols)})
        
        # Compile full results
        full_results = {
            'success': True,
            'filename': file.filename,
            'dataset_type': dataset_type,
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            
            'basic_info': basic_info,
            'data_quality': data_quality,
            'feature_correlation': feature_correlation,
            'data_type_classification': data_type_classification,
            'column_analysis': column_analysis,
            'detected_columns': {
                'target_column': target_col,
                'text_column': text_col,
                'demographic_columns': demographic_cols,
                'available_columns': column_detection_info.get('available_columns', []),
                'target_priority': column_detection_info.get('target_priority'),
                'detection_info': column_detection_info
            },
            'ml_training': ml_results,
            'bias_analysis': bias_results,
            'class_imbalance': class_imbalance,
            'risk_assessment': risk_assessment,
            'risk_summary': risk_summary,
            
            # Overall Health
            'dataset_health_score': health_score,
            'proactive_risk_assessment': proactive_risk,
            
            # Metadata
            'dataset_metadata': dataset_info,
            
            # Validation
            'validation': validation
        }
        
        # Convert to JSON-serializable format
        full_results = utils.Utils.convert_for_json(full_results)
        
        return JSONResponse(content=full_results)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/report")
async def generate_clean_report(file: UploadFile = File(...)):
    """
    Generate clean bias analysis report for frontend.
    
    Args:
        file: CSV file to analyze
        
    Returns:
        Clean, production-ready bias analysis report
    """
    try:
        # Run full analysis
        full_results = await analyze_dataset(file)
        
        # Extract the actual results from the response
        if isinstance(full_results, JSONResponse):
            analysis_data = full_results.body.decode('utf-8')
            import json
            full_results = json.loads(analysis_data)
        
        # Generate clean report
        clean_report = BiasAnalysisReport.from_analysis_results(full_results)
        
        return JSONResponse(content=clean_report.to_dict())
        
    except ValueError as e:
        print(f"ValueError in report generation: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in report generation: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/report/example")
async def get_example_report():
    """Get example report for frontend development."""
    from analyzer.report_schema import get_example_report
    return JSONResponse(content=get_example_report())


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Simple file upload endpoint for testing.
    
    Args:
        file: File to upload
        
    Returns:
        Upload confirmation
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        try:
            # Read file content
            file_str = await file.read()
            file_str = file_str.decode('utf-8')
            
            # Load CSV safely
            df = utils.Utils.safe_load_csv(file_str)
            
            # Basic validation
            validation = utils.Utils.validate_dataframe(df)
            if not validation['is_valid']:
                raise HTTPException(status_code=400, detail=validation['errors'])
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
        
        return {
            'success': True,
            'filename': file.filename,
            'message': 'File uploaded successfully',
            'dataset_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist()
            },
            'validation': validation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/components")
async def get_components():
    """Get information about analyzer components."""
    return {
        'components': {
            'column_detector': {
                'description': 'Auto-detects target and text columns',
                'methods': ['detect_columns', 'classify_dataset_type']
            },
            'dataset_analyzer': {
                'description': 'Performs basic dataset analysis',
                'methods': ['get_basic_info', 'analyze_data_quality', 'analyze_correlations']
            },
            'ml_engine': {
                'description': 'Handles ML model training and evaluation',
                'methods': ['train_and_evaluate', 'select_model', 'prepare_data']
            },
            'nlp_bias_analyzer': {
                'description': 'Analyzes bias in NLP/text datasets',
                'methods': ['analyze_bias', '_detect_toxicity', '_analyze_sentiment']
            },
            'tabular_bias_analyzer': {
                'description': 'Analyzes bias in tabular datasets',
                'methods': ['analyze_bias', '_analyze_demographic_bias', '_calculate_fairness_metrics']
            },
            'risk_engine': {
                'description': 'Calculates weighted risk scores',
                'methods': ['calculate_risk', 'get_risk_summary']
            },
            'utils': {
                'description': 'Utility functions for data processing',
                'methods': ['safe_load_csv', 'convert_for_json', 'validate_dataframe']
            }
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
