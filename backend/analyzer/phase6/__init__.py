"""
Phase 6 Module Initialization
Clean architecture with structural profiling.
"""

from .profiler import DatasetProfiler
from .benchmark_engine import BenchmarkEngine
from .recommendation_engine import RecommendationEngine
from .kaggle_suggester import KaggleSuggester
from .phase6_engine import Phase6Engine

__all__ = [
    'DatasetProfiler',
    'BenchmarkEngine', 
    'RecommendationEngine',
    'KaggleSuggester',
    'Phase6Engine'
]
