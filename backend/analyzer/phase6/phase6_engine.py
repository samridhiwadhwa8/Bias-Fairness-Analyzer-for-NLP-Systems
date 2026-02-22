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
        """
        Execute complete Phase 6 analysis with clean architecture.
        
        Args:
            report: Complete bias analysis report from Phase 4
            
        Returns:
            Comprehensive ecosystem intelligence and recommendations
        """
        print("=== PHASE 6: Dataset Intelligence & Ecosystem Analysis ===")
        
        # Step 1: Structural profiling (no hardcoding)
        print("Step 1: Creating structural profile...")
        profile = self.profiler.profile(report)
        print(f"DEBUG ENGINE: Profile type: {type(profile)}")
        print(f"DEBUG ENGINE: Profile value: {profile}")
        if isinstance(profile, dict):
            print(f"DEBUG ENGINE: Profile keys: {list(profile.keys())}")
        else:
            print(f"DEBUG ENGINE: ERROR: Profile is not a dict!")
        
        # Step 2: Risk benchmarking (correct percentile)
        print("Step 2: Benchmarking risk against ecosystem...")
        benchmark_comparison = self.benchmark.generate_benchmark_comparison(report)
        
        # Step 3: Kaggle suggestions (archetype-based)
        print("Step 3: Finding similar dataset archetypes...")
        similar_datasets = self.kaggle.suggest(profile)
        
        # Step 4: Recommendations (risk-based)
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
                    "no_hardcoding": True,
                    "correct_percentile": True,
                    "archetype_based": True
                }
            }
        }
        
        print("✅ Phase 6 Analysis Complete!")
        print(f"Profile: {profile['fingerprint']}")
        print(f"Risk Percentile: {benchmark_comparison['benchmark_comparison']['percentile']}%")
        print(f"Market Position: {benchmark_comparison['benchmark_comparison']['position']}")
        print(f"Similar Datasets: {len(similar_datasets)} found")
        
        return results
