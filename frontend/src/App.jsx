import React, { useState, useCallback } from 'react'
import { Upload, Shield, CheckCircle, XCircle, Database, Brain, Users, MessageSquare, TrendingUp, Target, BarChart3, Download } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

function App() {
  const [report, setReport] = useState(null)
  const [phase5Report, setPhase5Report] = useState(null)
  const [phase6Report, setPhase6Report] = useState(null)
  const [phase7Report, setPhase7Report] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyzeReport = async (report) => {
    try {
      const response = await axios.post('http://localhost:8000/phase5/analyze', report)
      console.log('Phase 5 analysis received:', response.data)
      return response.data
    } catch (err) {
      console.error('Phase 5 analysis error:', err)
      return null
    }
  }

  const analyzePhase6 = async (report) => {
    try {
      const response = await axios.post('http://localhost:8000/phase6/analyze', report)
      console.log('Phase 6 analysis received:', response.data)
      return response.data
    } catch (err) {
      console.error('Phase 6 analysis error:', err)
      return null
    }
  }

  const analyzePhase7 = async (report) => {
    try {
      const response = await axios.post('http://localhost:8000/phase7/generate', report)
      console.log('Phase 7 analysis received:', response.data)
      return response.data
    } catch (err) {
      console.error('Phase 7 analysis error:', err)
      return null
    }
  }

  const onAnalyze = useCallback(async (file) => {
    setLoading(true)
    setError('')
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await axios.post('http://localhost:8000/report', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 300000  
      })
      
      console.log('Clean report received:', response.data)
      console.log('Component scores:', response.data.overall_risk?.component_scores)
      console.log('Individual components:')
      console.log('  Demographic:', response.data.overall_risk?.component_scores?.demographic)
      console.log('  Linguistic:', response.data.overall_risk?.component_scores?.linguistic)
      console.log('  Toxicity:', response.data.overall_risk?.component_scores?.toxicity)
      console.log('  Sentiment:', response.data.overall_risk?.component_scores?.sentiment)
      console.log('  Class Imbalance:', response.data.overall_risk?.component_scores?.class_imbalance)
      
      setReport(response.data)
      
      // Call Phase 5 analysis
      const phase5Data = await analyzeReport(response.data)
      setPhase5Report(phase5Data)
      
      // Call Phase 6 analysis
      const phase6Data = await analyzePhase6(response.data)
      setPhase6Report(phase6Data)
      
      // Call Phase 7 analysis
      const phase7Data = await analyzePhase7(response.data)
      setPhase7Report(phase7Data)
      
      setLoading(false)
    } catch (err) {
      console.error('Analysis error:', err)
      setError(err.response?.data?.detail || 'Analysis failed')
      setLoading(false)
    }
  }, [])

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0]
    if (file && file.name.endsWith('.csv')) {
      onAnalyze(file)
    } else {
      setError('Please upload a CSV file')
    }
  }, [onAnalyze])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    multiple: false
  })

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low': return 'risk-low'
      case 'Moderate': return 'risk-moderate'
      case 'High': return 'risk-high'
      default: return 'risk-low'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 0.7) return 'risk-score-high'
    if (score >= 0.4) return 'risk-score-moderate'
    return 'risk-score-low'
  }

  const getAssessmentColor = (assessment) => {
    if (assessment?.includes('HIGH SEVERITY')) return 'risk-score-high'
    if (assessment?.includes('ELEVATED SEVERITY')) return 'risk-score-moderate'
    return 'risk-score-low'
  }

  const getDecisionColor = (decision) => {
    if (decision?.includes('Comprehensive Mitigation Required')) return 'risk-score-high'
    if (decision?.includes('Performance Improvement Required')) return 'risk-score-high'
    if (decision?.includes('Conditional Approval')) return 'risk-score-moderate'
    return 'risk-score-low'
  }

  const getComplianceColor = (level) => {
    if (level === 'High') return 'risk-score-high'
    if (level === 'Medium') return 'risk-score-moderate'
    return 'risk-score-low'
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <div className="loading-text">Analyzing dataset for bias...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-card">
          <XCircle className="error-icon" />
          <h2 className="error-title">Analysis Failed</h2>
          <p className="error-message">{error}</p>
          <button 
            onClick={() => setError('')}
            className="btn btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (report) {
    return (
      <div className="app-container">
        {/* Report Header */}
        <div className="report-header">
          <div>
            <h1 className="report-title">Bias Analysis Report</h1>
            <p className="report-subtitle">Professional, production-ready bias assessment</p>
          </div>
          <div className={`risk-badge ${getRiskColor(report.overall_risk.risk_level)}`}>
            <span>{report.overall_risk.risk_level} Risk</span>
            <span>({report.overall_risk.risk_percentage}%)</span>
          </div>
        </div>

        {/* Overview Cards */}
        <div className="card-grid">
          {/* Dataset Overview */}
          <div className="card">
            <div className="card-header">
              <Database className="card-icon" />
              <h2 className="card-title">Dataset Overview</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Total Rows</span>
                <span className="metric-value">{report.dataset_overview.total_rows.toLocaleString()}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Total Columns</span>
                <span className="metric-value">{report.dataset_overview.total_columns}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Dataset Size</span>
                <span className="metric-value">{report.dataset_overview.dataset_size_mb} MB</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Dataset Type</span>
                <span className="metric-value">{report.dataset_overview.dataset_type}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Target Column</span>
                <span className="metric-value">{report.dataset_overview.target_column || 'N/A'}</span>
              </div>
              {report.dataset_overview.text_column && (
                <div className="metric-item">
                  <span className="metric-label">Text Column</span>
                  <span className="metric-value">{report.dataset_overview.text_column}</span>
                </div>
              )}
            </div>
          </div>

          {/* Data Quality */}
          <div className="card">
            <div className="card-header">
              <Shield className="card-icon" />
              <h2 className="card-title">Data Quality</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Missing Data</span>
                <span className={`metric-value ${getScoreColor(report.data_quality.missing_percentage / 100)}`}>
                  {report.data_quality.missing_percentage}%
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Duplicate Rows</span>
                <span className="metric-value">{report.data_quality.duplicate_rows}</span>
              </div>
              {report.data_quality.outlier_percentage !== null && (
                <div className="metric-item">
                  <span className="metric-label">Outliers</span>
                  <span className={`metric-value ${getScoreColor(report.data_quality.outlier_percentage / 100)}`}>
                    {report.data_quality.outlier_percentage}%
                  </span>
                </div>
              )}
              <div className="metric-item">
                <span className="metric-label">Completeness</span>
                <span className={`metric-value ${getScoreColor(report.data_quality.completeness_score / 100)}`}>
                  {report.data_quality.completeness_score}%
                </span>
              </div>
            </div>
          </div>

          {/* ML Training */}
          <div className="card">
            <div className="card-header">
              <Brain className="card-icon" />
              <h2 className="card-title">ML Training</h2>
            </div>
            {report.ml_training ? (
              <div className="metric-list">
                <div className="metric-item">
                  <span className="metric-label">Model</span>
                  <span className="metric-value">{report.ml_training.model_name}</span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Accuracy</span>
                  <span className={`metric-value ${getScoreColor(report.ml_training.accuracy / 100)}`}>
                    {report.ml_training.accuracy}%
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Precision</span>
                  <span className={`metric-value ${getScoreColor(report.ml_training.precision / 100)}`}>
                    {report.ml_training.precision}%
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Recall</span>
                  <span className={`metric-value ${getScoreColor(report.ml_training.recall / 100)}`}>
                    {report.ml_training.recall}%
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">F1 Score</span>
                  <span className={`metric-value ${getScoreColor(report.ml_training.f1_score)}`}>
                    {report.ml_training.f1_score}
                  </span>
                </div>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <Brain style={{ width: '48px', height: '48px', margin: '0 auto 1rem', opacity: 0.3 }} />
                <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>ML training not applicable</p>
              </div>
            )}
          </div>
        </div>

        {/* Bias Analysis */}
        <div className="card-grid">
          {/* Demographic Bias */}
          <div className="card">
            <div className="card-header">
              <Users className="card-icon" />
              <h2 className="card-title">Demographic Bias</h2>
              {report.bias_analysis.demographic_bias.detected && (
                <span className="status-badge status-detected">Detected</span>
              )}
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Detected</span>
                <span className={`metric-value ${report.bias_analysis.demographic_bias.detected ? 'risk-score-moderate' : 'risk-score-low'}`}>
                  {report.bias_analysis.demographic_bias.detected ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Score</span>
                <span className={`metric-value ${getScoreColor(report.bias_analysis.demographic_bias.score)}`}>
                  {report.bias_analysis.demographic_bias.score}
                </span>
              </div>
              {report.bias_analysis.demographic_bias.columns.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <span className="metric-label">Columns</span>
                  <div className="tag-cloud">
                    {report.bias_analysis.demographic_bias.columns.map((col, idx) => (
                      <span key={idx} className="tag">{col}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Linguistic Bias */}
          <div className="card">
            <div className="card-header">
              <MessageSquare className="card-icon" />
              <h2 className="card-title">Linguistic Bias</h2>
              {report.bias_analysis.linguistic_bias.detected && (
                <span className="status-badge status-detected">Detected</span>
              )}
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Detected</span>
                <span className={`metric-value ${report.bias_analysis.linguistic_bias.detected ? 'risk-score-moderate' : 'risk-score-low'}`}>
                  {report.bias_analysis.linguistic_bias.detected ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Score</span>
                <span className={`metric-value ${getScoreColor(report.bias_analysis.linguistic_bias.score)}`}>
                  {report.bias_analysis.linguistic_bias.score}
                </span>
              </div>
              {report.bias_analysis.linguistic_bias.detected && (
                <>
                  <div className="metric-item">
                    <span className="metric-label">Toxicity</span>
                    <span className={`metric-value ${getScoreColor(report.bias_analysis.linguistic_bias.toxicity_score)}`}>
                      {report.bias_analysis.linguistic_bias.toxicity_score}
                    </span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">Sentiment Gap</span>
                    <span className={`metric-value ${getScoreColor(report.bias_analysis.linguistic_bias.sentiment_gap)}`}>
                      {report.bias_analysis.linguistic_bias.sentiment_gap}
                    </span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">Gender Imbalance</span>
                    <span className={`metric-value ${getScoreColor(report.bias_analysis.linguistic_bias.gender_language_imbalance)}`}>
                      {report.bias_analysis.linguistic_bias.gender_language_imbalance}
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Risk Breakdown */}
        <div className="card">
          <div className="card-header">
            <TrendingUp className="card-icon" />
            <h2 className="card-title">Risk Breakdown</h2>
          </div>
          {report && (
        <>
          <div className="risk-grid">
            <div className="risk-component">
              <div className={`risk-score ${getScoreColor(report.overall_risk?.component_scores?.demographic || 0)}`}>
                {report.overall_risk?.component_scores?.demographic || 0}
              </div>
              <div className="risk-component-name">Demographic</div>
            </div>
            <div className="risk-component">
              <div className={`risk-score ${getScoreColor(report.overall_risk?.component_scores?.linguistic || 0)}`}>
                {report.overall_risk?.component_scores?.linguistic || 0}
              </div>
              <div className="risk-component-name">Linguistic</div>
            </div>
            <div className="risk-component">
              <div className={`risk-score ${getScoreColor(report.overall_risk?.component_scores?.toxicity || 0)}`}>
                {report.overall_risk?.component_scores?.toxicity || 0}
              </div>
              <div className="risk-component-name">Toxicity</div>
            </div>
            <div className="risk-component">
              <div className={`risk-score ${getScoreColor(report.overall_risk?.component_scores?.sentiment || 0)}`}>
                {report.overall_risk?.component_scores?.sentiment || 0}
              </div>
              <div className="risk-component-name">Sentiment</div>
            </div>
            <div className="risk-component">
              <div className={`risk-score ${getScoreColor(report.overall_risk?.component_scores?.class_imbalance || 0)}`}>
                {report.overall_risk?.component_scores?.class_imbalance || 0}
              </div>
              <div className="risk-component-name">Class Imbalance</div>
            </div>
          </div>
          
          {/* Class Imbalance Details */}
          {report.ml_training?.class_imbalance_details && (
            <div className="card">
              <div className="card-header">
                <BarChart3 className="card-icon" />
                <h2 className="card-title">Class Imbalance Details</h2>
              </div>
              <div className="metric-list">
                <div className="metric-item">
                  <span className="metric-label">Imbalance Ratio</span>
                  <span className="metric-value">
                    {report.ml_training.class_imbalance_details.ratio}:1
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Max Class %</span>
                  <span className="metric-value">
                    {report.ml_training.class_imbalance_details.max_class_percentage}%
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Min Class %</span>
                  <span className="metric-value">
                    {report.ml_training.class_imbalance_details.min_class_percentage}%
                  </span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Class Distribution</span>
                  <div className="class-distribution">
                    {Object.entries(report.ml_training.class_imbalance_details.class_distribution || {}).map(([className, count]) => (
                      <div key={className} className="class-item">
                        <span className="class-name">{className}:</span>
                        <span className="class-count">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
        </div>

        {/* Recommendations */}
        <div className="card">
          <div className="card-header">
            <Target className="card-icon" />
            <h2 className="card-title">Recommendations</h2>
          </div>
          <div className="recommendation-list">
            {report.recommendations.map((rec, idx) => (
              <div key={idx} className="recommendation-item">
                <CheckCircle className="recommendation-icon" />
                <span className="recommendation-text">{rec}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Phase 5 Risk Intelligence */}
        {phase5Report && (
        <div className="phase5-section">
          <h2 className="section-title">🧠 Risk Intelligence & Action Plan</h2>
          
          {/* Executive Summary */}
          <div className="card">
            <div className="card-header">
              <Target className="card-icon" />
              <h2 className="card-title">Executive Summary</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Overall Assessment</span>
                <span className={`metric-value ${getAssessmentColor(phase5Report.results?.executive_summary?.overall_assessment)}`}>
                  {phase5Report.results?.executive_summary?.overall_assessment}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Deployment Action</span>
                <span className="metric-value">
                  {phase5Report.results?.interpretation?.deployment_action}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Timeline</span>
                <span className="metric-value">
                  {phase5Report.results?.interpretation?.deployment_timeline}
                </span>
              </div>
            </div>
          </div>

          {/* Deployment Decision */}
          <div className="card">
            <div className="card-header">
              <Shield className="card-icon" />
              <h2 className="card-title">Deployment Decision</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Decision</span>
                <span className={`metric-value ${getDecisionColor(phase5Report.results?.deployment?.deployment_decision)}`}>
                  {phase5Report.results?.deployment?.deployment_decision}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Confidence</span>
                <span className="metric-value">
                  {Math.round((phase5Report.results?.deployment?.confidence_score || 0) * 100)}%
                </span>
              </div>
            </div>
          </div>

          {/* Mitigation Recommendations */}
          <div className="card">
            <div className="card-header">
              <Brain className="card-icon" />
              <h2 className="card-title">Mitigation Recommendations</h2>
            </div>
            <div className="mitigation-list">
              {phase5Report.results?.mitigation?.recommended_actions?.map((action, idx) => (
                <div key={idx} className="mitigation-item">
                  <span className="mitigation-bullet">•</span>
                  <span className="mitigation-text">{action}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Compliance Assessment */}
          <div className="card">
            <div className="card-header">
              <CheckCircle className="card-icon" />
              <h2 className="card-title">Compliance Assessment</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Regulatory Risk</span>
                <span className={`metric-value ${getComplianceColor(phase5Report.results?.compliance?.regulatory_risk?.level)}`}>
                  {phase5Report.results?.compliance?.regulatory_risk?.level}
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Review Required</span>
                <span className="metric-value">
                  {phase5Report.results?.compliance?.regulatory_risk?.review_required ? 'Yes' : 'No'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Phase 6 Dataset Intelligence */}
      {phase6Report && (
        <div className="phase5-section">
          <h2 className="section-title">📊 Dataset Intelligence & Ecosystem Analysis</h2>
          
          {/* Dataset Profile */}
          <div className="card">
            <div className="card-header">
              <Database className="card-icon" />
              <h2 className="card-title">Dataset Profile</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Fingerprint</span>
                <span className="metric-value">{phase6Report.results?.profile?.fingerprint}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Domain</span>
                <span className="metric-value">{phase6Report.results?.profile?.domain}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Task</span>
                <span className="metric-value">{phase6Report.results?.profile?.task}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Size</span>
                <span className="metric-value">{phase6Report.results?.profile?.size}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Balance</span>
                <span className="metric-value">{phase6Report.results?.profile?.balance}</span>
              </div>
            </div>
          </div>

          {/* Risk Percentile */}
          <div className="card">
            <div className="card-header">
              <BarChart3 className="card-icon" />
              <h2 className="card-title">Risk Percentile</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Percentile</span>
                <span className={`metric-value ${getScoreColor(phase6Report.results?.risk_percentile / 100)}`}>
                  {phase6Report.results?.risk_percentile}th
                </span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Market Position</span>
                <span className="metric-value">{phase6Report.results?.market_position}</span>
              </div>
            </div>
          </div>

          {/* Deployment Decision */}
          <div className="card">
            <div className="card-header">
              <Target className="card-icon" />
              <h2 className="card-title">Deployment Decision</h2>
            </div>
            <div className="metric-list">
              <div className="metric-item">
                <span className="metric-label">Decision</span>
                <span className={`metric-value ${getDecisionColor(phase6Report.results?.executive_summary?.deployment_decision)}`}>
                  {phase6Report.results?.executive_summary?.deployment_decision}
                </span>
              </div>
            </div>
          </div>

          {/* Similar Datasets */}
          {phase6Report.results?.similar_datasets && phase6Report.results.similar_datasets.length > 0 && (
            <div className="card">
              <div className="card-header">
                <Users className="card-icon" />
                <h2 className="card-title">Similar Datasets</h2>
              </div>
              <div className="mitigation-list">
                {phase6Report.results.similar_datasets.map((dataset, idx) => (
                  <div key={idx} className="mitigation-item">
                    <span className="mitigation-bullet">•</span>
                    <span className="mitigation-text">
                      <a 
                        href={dataset.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ color: '#3b82f6', textDecoration: 'none' }}
                      >
                        <strong>{dataset.name}</strong> - {dataset.domain}
                      </a>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Phase 7 Dataset Governance */}
      {phase7Report && (
        <div className="phase5-section">
          <h2 className="section-title">📋 Dataset Governance Report</h2>
          
          {/* Report Actions */}
          <div className="card">
            <div className="card-header">
              <Download className="card-icon" />
              <h2 className="card-title">Report Actions</h2>
            </div>
            <div className="mitigation-list">
              {/* Debug info */}
              <div style={{ fontSize: '12px', color: '#666', marginBottom: '10px' }}>
                Debug: PDF Path = {phase7Report.results?.pdf_path || 'NULL'}
              </div>
              <button 
                onClick={() => {
                  const pdfPath = phase7Report.results?.pdf_path;
                  if (pdfPath && pdfPath !== 'undefined' && pdfPath !== null) {
                    const filename = pdfPath.split('/').pop();
                    const downloadUrl = `http://localhost:8000/phase7/download/${filename}`;
                    console.log('Downloading PDF:', downloadUrl);
                    window.open(downloadUrl, '_blank');
                  } else {
                    alert('PDF report not available. Please run analysis first.');
                  }
                }}
                className="mitigation-item"
                style={{ cursor: 'pointer', padding: '10px', margin: '5px', border: '1px solid #ddd', borderRadius: '5px', background: '#f8f9fa' }}
              >
                <span className="mitigation-bullet">📄</span>
                <span className="mitigation-text">Download Full Report (PDF)</span>
              </button>
            </div>
          </div>
          
          {/* Visual Insights Summary */}
          {phase7Report.results?.visual_paths && phase7Report.results.visual_paths.length > 0 && (
            <div className="card">
              <div className="card-header">
                <BarChart3 className="card-icon" />
                <h2 className="card-title">Generated Visualizations</h2>
              </div>
              <div className="mitigation-list">
                {phase7Report.results.visual_paths.map((path, idx) => (
                  <div key={idx} className="mitigation-item">
                    <span className="mitigation-bullet">•</span>
                    <span className="mitigation-text">{path.split('/').pop()}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Action Button */}
      <div style={{ textAlign: 'center', marginTop: '3rem' }}>
        <button 
          onClick={() => setReport(null)}
          className="btn btn-primary"
          >
            Analyze Another Dataset
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-icon">
          <Shield />
        </div>
        <h1 className="hero-title">Bias Analyzer</h1>
        <p className="hero-subtitle">Professional-grade bias detection and analysis for machine learning datasets</p>
      </div>

      {/* Upload Section */}
      <div className="upload-section">
        <div 
          {...getRootProps()} 
          className={`upload-area ${isDragActive ? 'dragover' : ''}`}
        >
          <input {...getInputProps()} />
          <Upload className="upload-icon" />
          <div className="upload-text">Drop your CSV file here</div>
          <p className="upload-subtext">or click to browse</p>
        </div>
      </div>

      {/* Example Report Button */}
      <div style={{ textAlign: 'center' }}>
        <button 
          onClick={() => fetch('http://localhost:8000/report/example')
            .then(res => res.json())
            .then(data => setReport(data))
          }
          className="btn btn-secondary"
        >
          View Example Report
        </button>
      </div>
    </div>
  )
}

export default App
