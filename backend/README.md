# Bias Analyzer Backend - Modular Architecture

## 📁 Project Structure

```
backend/
├── app.py              # Main FastAPI application and routes
├── dataset_engine.py    # Dataset analysis and profiling
├── model_engine.py     # ML model training and evaluation  
├── bias_engine.py      # Bias and fairness detection
├── recommender_engine.py # Dataset recommendations and risk assessment
├── utils.py            # Common utility functions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Module Responsibilities

### **app.py** - Main Application
- FastAPI server setup and configuration
- API route definitions (`/`, `/api/health`, `/api/analyze`)
- Request/response handling
- Error handling and logging
- **Orchestrates all engines**

### **dataset_engine.py** - Dataset Analysis (Phase 1)
- Data loading and validation
- Basic statistics and profiling
- Data quality assessment
- Sensitive column detection
- Feature correlation analysis
- Data type classification
- Metadata extraction and caching

### **model_engine.py** - ML Training (Phase 3)
- Intelligent column detection (text vs categorical)
- Dataset type classification
- Model selection logic (text → Naive Bayes, categorical → Random Forest)
- Feature engineering (TF-IDF, One-Hot Encoding)
- Model training and evaluation
- Performance metrics calculation

### **bias_engine.py** - Bias Analysis (Phase 4)
- **Demographic bias detection** (gender, race, age, socioeconomic)
- **Linguistic bias detection**:
  - 🧪 Toxicity score
  - 📊 Word frequency bias
  - ⚖️ Positive vs Negative probability gap
  - 👫 Gendered word analysis (he vs she ratio)
- Overall risk assessment
- Mitigation recommendations

### **recommender_engine.py** - Recommendations (Phase 2)
- Dataset use case recommendations
- Proactive risk assessment
- Data quality insights
- Improvement suggestions
- Risk factor analysis

### **utils.py** - Common Utilities
- File loading and validation
- Multiple encoding support
- Data type conversion for JSON
- Standardized response formatting
- Error handling helpers

## 🔄 Data Flow

```
Upload → app.py → dataset_engine.py → model_engine.py → bias_engine.py → recommender_engine.py → Response
```

## 🎯 Key Benefits

✅ **Modular Architecture**: Each engine has single responsibility
✅ **Maintainable**: Easy to debug and modify individual components
✅ **Testable**: Each module can be tested independently
✅ **Scalable**: Easy to add new features or engines
✅ **No Corruption**: Modular structure prevents file corruption issues
✅ **Clear Imports**: No circular dependencies, clean module structure

## 🚀 Running the Application

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server will run on `http://0.0.0.0:8001` with all existing functionality preserved.

## 📝 Notes

- All existing functionality has been preserved and organized
- No breaking changes to API endpoints
- Frontend integration remains unchanged
- Enhanced error handling and logging throughout
