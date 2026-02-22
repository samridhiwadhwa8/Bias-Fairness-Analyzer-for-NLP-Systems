"""
Phase 6 Engine - Dataset Intelligence & Ecosystem Layer
Clean orchestration with structural profiling and correct risk interpretation.
"""

from typing import Dict, Any, List
from .profiler import DatasetProfiler
from .benchmark_engine import BenchmarkEngine  
from .recommendation_engine import RecommendationEngine
from .kaggle_suggester import KaggleSuggester


class Phase6Engine:
    """Phase 6: Dataset Intelligence & Ecosystem Awareness Engine."""
    
    def __init__(self):
        """Initialize Phase 6 components."""
        self.profiler = DatasetProfiler()
        self.benchmark = BenchmarkEngine()
        self.recommender = RecommendationEngine()
        self.kaggle = KaggleSuggester()
    
    def analyze(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Complete Phase 6 analysis with strict validation."""
        print("=== PHASE 6: Dataset Intelligence & Ecosystem Analysis ===")
        
        # Strict risk validation - NO silent fallbacks
        if "overall_risk" not in report:
            raise ValueError("Phase6: overall_risk missing from report")
        
        risk_data = report["overall_risk"]
        if not isinstance(risk_data, dict):
            raise ValueError("Phase6: overall_risk is not a dictionary")
        
        if "risk_percentage" not in risk_data:
            raise ValueError("Phase6: risk_percentage missing from overall_risk")
        
        if "risk_level" not in risk_data:
            raise ValueError("Phase6: risk_level missing from overall_risk")
        
        risk_percentage = risk_data["risk_percentage"]
        risk_level = risk_data["risk_level"]
        
        print(f"DEBUG ENGINE: Valid risk data - percentage: {risk_percentage}%, level: {risk_level}")
        
        # Step 1: Create structural profile
        print("Step 1: Creating structural profile...")
        profile = self.profiler.profile(report)
        
        print(f"DEBUG ENGINE: Profile type: {type(profile)}")
        print(f"DEBUG ENGINE: Profile value: {profile}")
        print(f"DEBUG ENGINE: Profile keys: {list(profile.keys()) if isinstance(profile, dict) else 'Not a dict'}")
        
        # Step 2: Benchmarking
        print("Step 2: Benchmarking risk against ecosystem...")
        benchmark_comparison = self.benchmark.generate_benchmark_comparison(report)
        
        # Step 3: Find similar datasets
        print("Step 3: Finding similar dataset archetypes...")
        similar_datasets = self.kaggle_suggester.suggest(profile)
        
        # Step 4: Generate recommendations
        print("Step 4: Generating risk-based recommendations...")
        recommendations = self.recommender.generate(report, profile)
        
        # Compile results
        results = {
            "profile": profile,
            "risk_percentile": benchmark_comparison["benchmark_comparison"]["percentile"],
            "market_position": benchmark_comparison["benchmark_comparison"]["position"],
            "similar_datasets": similar_datasets,
            "executive_summary": {
                "overall_assessment": recommendations["risk_assessment"],
                "deployment_decision": recommendations["deployment_decision"],
                "primary_recommendation": recommendations["recommendations"][0] if recommendations.get("recommendations") else "No recommendation",
                "next_steps": recommendations["next_steps"]
            },
            "benchmark_analysis": benchmark_comparison,
            "metadata": {
                "phase": "6",
                "analysis_type": "dataset_intelligence",
                "structural_only": True,
                "no_hardcoding": True,
                "features": {
                    "structural_profiling": True,
                    "ecosystem_benchmarking": True,
                    "domain_aware_suggestions": True,
                    "risk_validation": "strict"
                }
            }
        }
        
        print("✅ Phase 6 Analysis Complete!")
        print(f"Profile: {profile.get('fingerprint', 'Unknown')}")
        print(f"Risk Percentile: {results['risk_percentile']}%")
        print(f"Market Position: {results['market_position']}")
        print(f"Similar Datasets: {len(similar_datasets)} found")
        
        return results
