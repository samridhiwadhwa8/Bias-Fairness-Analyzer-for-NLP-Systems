"""
Benchmark Engine Module - Phase 6
Correct percentile calculation and risk interpretation.
"""

from typing import Dict, Any, List


class BenchmarkEngine:
    """Compares dataset risk against ecosystem benchmarks correctly."""
    
    def __init__(self):
        # Benchmark risk percentages from reference datasets
        self.benchmarks = [22, 28, 35, 42, 50, 60, 72, 80]
        
        # Domain-specific benchmarks (can be expanded)
        self.domain_benchmarks = {
            "finance": [35, 42, 55, 65, 75],
            "health": [25, 30, 40, 50, 60],
            "social_media": [45, 55, 65, 75, 85],
            "general": [30, 40, 50, 60, 70]
        }
    
    def calculate_percentile(self, risk_percentage: float, domain: str = "general") -> Dict[str, Any]:
        """
        Calculate correct percentile - higher percentile = higher relative risk.
        
        Args:
            risk_percentage: Dataset risk percentage
            domain: Dataset domain for domain-specific benchmarks
            
        Returns:
            Percentile calculation and interpretation
        """
        benchmarks = self.domain_benchmarks.get(domain, self.benchmarks)
        
        # Validation
        if not benchmarks:
            raise ValueError("Benchmark list cannot be empty")
        
        # Debug logs
        print(f"DEBUG BENCHMARK: Full benchmark list: {benchmarks}")
        
        # Calculate percentile with correct denominator (never mutate original list)
        total_count = len(benchmarks)
        lower_count = sum(1 for r in benchmarks if r < risk_percentage)
        percentile = (lower_count / total_count) * 100
        
        # Debug logs
        print(f"DEBUG BENCHMARK: Risk percentage: {risk_percentage}%")
        print(f"DEBUG BENCHMARK: Lower count (benchmarks < risk): {lower_count}")
        print(f"DEBUG BENCHMARK: Total count (full benchmark list): {total_count}")
        print(f"DEBUG BENCHMARK: Final percentile: {round(percentile, 1)}%")
        
        return {
            "percentile": round(percentile, 1),
            "datasets_lower_risk": lower_count,
            "datasets_higher_risk": total_count - lower_count,
            "total_datasets": total_count
        }
    
    def interpret_percentile(self, percentile: float) -> Dict[str, Any]:
        """
        Interpret percentile correctly - higher percentile = higher relative risk.
        """
        if percentile >= 80:
            return {
                "level": "very_high",
                "description": "Higher risk than 80% of similar datasets",
                "position": "Among highest risk datasets"
            }
        elif percentile >= 60:
            return {
                "level": "high", 
                "description": "Higher risk than 60% of similar datasets",
                "position": "Above average risk level"
            }
        elif percentile >= 40:
            return {
                "level": "average",
                "description": "Average risk level compared to similar datasets", 
                "position": "Typical risk profile"
            }
        elif percentile >= 20:
            return {
                "level": "low",
                "description": "Lower risk than 60% of similar datasets",
                "position": "Below average risk level"
            }
        else:
            return {
                "level": "very_low",
                "description": "Lower risk than 80% of similar datasets",
                "position": "Among lowest risk datasets"
            }
    
    def generate_benchmark_comparison(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete benchmark comparison.
        
        Args:
            report: Complete bias analysis report
            
        Returns:
            Benchmark analysis with correct interpretation
        """
        overall_risk = report.get("overall_risk", {})
        risk_percentage = overall_risk.get("risk_percentage", 0)
        risk_level = overall_risk.get("risk_level", "Low")
        
        # Calculate percentile
        domain = "general"  # Can be extracted from profiler later
        percentile_data = self.calculate_percentile(risk_percentage, domain)
        interpretation = self.interpret_percentile(percentile_data["percentile"])
        
        return {
            "dataset_risk": {
                "percentage": risk_percentage,
                "level": risk_level
            },
            "benchmark_comparison": {
                "percentile": percentile_data["percentile"],
                "interpretation": interpretation["description"],
                "position": interpretation["position"],
                "datasets_below": percentile_data["datasets_lower_risk"],
                "datasets_above": percentile_data["datasets_higher_risk"]
            },
            "risk_classification": interpretation["level"]
        }
