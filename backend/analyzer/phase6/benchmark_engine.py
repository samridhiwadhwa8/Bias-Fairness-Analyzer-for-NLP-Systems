"""
Benchmark Engine - Phase 6
Risk percentile calculation and ecosystem positioning.
"""

from typing import List


class BenchmarkEngine:
    """Risk benchmarking and percentile calculation engine."""
    
    BENCHMARKS = [22, 28, 35, 42, 50, 60, 72, 80]

    def calculate_percentile(self, risk: float) -> float:
        """
        Calculate percentile rank of risk score against benchmarks.
        
        Args:
            risk: Risk percentage from analysis
            
        Returns:
            Percentile rank (0-100)
        """
        if risk is None:
            raise ValueError("Phase6: risk is None")

        benchmarks = self.BENCHMARKS

        if not benchmarks:
            raise ValueError("Phase6: benchmark list empty")

        total_count = len(benchmarks)
        lower_count = sum(1 for r in benchmarks if r < risk)

        percentile = (lower_count / total_count) * 100
        return round(percentile, 1)

    def interpret(self, percentile: float) -> str:
        """
        Interpret percentile position in ecosystem.
        
        Args:
            percentile: Percentile rank
            
        Returns:
            Interpretation string
        """
        if percentile < 40:
            return "Among lowest risk datasets"
        elif percentile < 70:
            return "Average ecosystem risk"
        else:
            return "Among highest risk datasets"
