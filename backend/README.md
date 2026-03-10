# Bias Analyzer Backend - Modular Architecture

## 🚀 Module Responsibilities

### **app.py** - Main Application
- FastAPI server setup and configuration
- API route definitions (`/`, `/api/health`, `/api/analyze`)
- Request/response handling
- Error handling and logging
- **Orchestrates all engines**

### Bias Analysis (Phase 4)
- **Demographic bias detection** (gender, race, age, socioeconomic)
- **Linguistic bias detection**:
  - 🧪 Toxicity score
  - 📊 Word frequency bias
  - ⚖️ Positive vs Negative probability gap
  - 👫 Gendered word analysis (he vs she ratio)
- Overall risk assessment
- Mitigation recommendations

### Recommendations (Phase 2)
- Dataset use case recommendations
- Proactive risk assessment
- Data quality insights
- Improvement suggestions
- Risk factor analysis

### Common Utilities
- File loading and validation
- Multiple encoding support
- Data type conversion for JSON
- Standardized response formatting
- Error handling helpers



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
