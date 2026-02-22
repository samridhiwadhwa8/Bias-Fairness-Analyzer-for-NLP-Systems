"""
Dataset Profiler - Phase 6
Structural profiling and fingerprinting without ML training.
"""

from typing import Dict, Any, List


class DatasetProfiler:
    """Dataset profiling and fingerprinting engine."""
    
    def profile(self, report: dict) -> dict:
        """
        Profile dataset and generate compact fingerprint.
        
        Args:
            report: Complete bias analysis report
            
        Returns:
            Dictionary with profile information and fingerprint
        """
        # Validate required keys
        if "dataset_overview" not in report:
            raise ValueError("Phase6: dataset_overview missing")

        overview = report["dataset_overview"]
        ml = report.get("ml_training")

        required_keys = ["total_rows", "dataset_type"]
        for key in required_keys:
            if key not in overview:
                raise ValueError(f"Phase6: {key} missing in dataset_overview")

        row_count = overview["total_rows"]
        dataset_type = overview["dataset_type"]
        columns = overview.get("available_columns", [])
        target_column = overview.get("target_column")

        # Size classification
        if row_count < 1000:
            size = "T"
        elif row_count < 10000:
            size = "S"
        elif row_count < 100000:
            size = "M"
        else:
            size = "L"

        # Task detection (classification-only project)
        task = "unk"
        if ml:
            if "class_distribution" in ml:
                task = "cls"
            elif "class_imbalance_details" in ml and \
                 "class_distribution" in ml["class_imbalance_details"]:
                task = "cls"
            else:
                task = "unk"

        # Imbalance detection
        imbalance_ratio = None
        if ml and "class_imbalance_ratio" in ml:
            imbalance_ratio = ml["class_imbalance_ratio"]

        if imbalance_ratio is None:
            balance_code = "UNK"
        elif imbalance_ratio <= 1.5:
            balance_code = "B"
        elif imbalance_ratio <= 3:
            balance_code = "MI"
        else:
            balance_code = "HI"

        # Domain detection
        domain = self._detect_domain(dataset_type, columns)

        # Compact fingerprint
        fingerprint = f"{domain}-{task}-{size}-{balance_code}"

        return {
            "domain": domain,
            "task": task,
            "size": size,
            "balance": balance_code,
            "dataset_type": dataset_type,
            "fingerprint": fingerprint
        }

    def _detect_domain(self, dataset_type: str, columns: List[str]) -> str:
        """
        Detect dataset domain based on column names and type.
        
        Args:
            dataset_type: Type of dataset (tabular/nlp)
            columns: List of column names
            
        Returns:
            Domain identifier string
        """
        columns_lower = [c.lower() for c in columns]

        if dataset_type == "nlp":
            # Default NLP to social media unless strong signal otherwise
            return "soc"

        # Medical/Healthcare domain detection
        if any(word in columns_lower for word in ["glucose", "insulin", "bmi", "blood", "pressure", "diabetes", "medical", "health", "patient", "treatment", "disease"]):
            return "med"

        if any(word in columns_lower for word in ["age", "gender", "race", "education"]):
            return "demo"

        if any(word in columns_lower for word in ["loan", "credit", "bank"]):
            return "fin"

        return "gen"
