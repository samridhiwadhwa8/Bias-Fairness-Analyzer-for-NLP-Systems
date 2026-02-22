"""
Dataset Profiler Module - Phase 6
Clean structural profiling without hardcoding or dataset names.
"""

from typing import Dict, Any


class DatasetProfiler:
    """Analyzes dataset characteristics using structural evidence only."""
    
    def __init__(self):
        self.domain_keywords = {
            "finance": ["loan", "credit", "income", "bank", "transaction", "salary", "payment", "account", "balance", "debt"],
            "health": ["patient", "disease", "hospital", "medical", "diagnosis", "treatment", "clinical", "health"],
            "social_media": ["tweet", "post", "comment", "like", "share", "retweet", "message", "review", "rating"],
            "ecommerce": ["product", "price", "order", "purchase", "cart", "item", "inventory", "shipping", "sales"],
            "hr": ["employee", "hire", "salary", "performance", "work", "job", "department", "attrition", "promotion"],
            "education": ["student", "school", "grade", "education", "academic", "university", "course", "exam", "score"],
            "government": ["census", "public", "government", "administrative", "official", "policy", "citizen", "state"],
            "retail": ["customer", "store", "retail", "shopping", "brand", "merchandise", "checkout", "basket"]
        }
    
    def profile(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create structural dataset profile from Phase 4 analysis.
        
        Args:
            report: Complete bias analysis report from Phase 4
            
        Returns:
            Dataset fingerprint with characteristics
        """
        print(f"DEBUG PROFILER: Starting profile with report keys: {list(report.keys())}")
        
        overview = report.get("dataset_overview", {})
        ml = report.get("ml_training", {})
        bias = report.get("bias_analysis", {})
        
        print(f"DEBUG PROFILER: Overview: {overview}")
        print(f"DEBUG PROFILER: ML: {ml}")
        print(f"DEBUG PROFILER: Bias: {bias}")
        
        # Extract structural evidence with CORRECT keys
        row_count = overview.get("total_rows", 0)
        dataset_type = overview.get("dataset_type", "tabular")
        columns = overview.get("available_columns", [])
        target_col = overview.get("target_column", "")
        
        # CRITICAL FIX: Validate required fields
        if row_count == 0:
            raise ValueError("Phase6: total_rows is 0 - missing or incorrect key")
        if not columns:
            raise ValueError("Phase6: available_columns is empty - missing or incorrect key")
        if not target_col:
            raise ValueError("Phase6: target_column is empty - missing or incorrect key")
        
        print(f"DEBUG PROFILER: CORRECTLY Extracted - rows: {row_count}, type: {dataset_type}, columns: {len(columns)}, target: {target_col}")
        
        # Size detection (deterministic)
        size = self._detect_size(row_count)
        
        # Task detection using ML metadata only (NO unique count inference)
        task = "unknown"
        
        if ml:
            if "class_distribution" in ml and ml["class_distribution"]:
                task = "classification"
                print(f"DEBUG TASK: Found class_distribution, task = {task}")
            elif "f1_score" in ml:
                task = "classification"
                print(f"DEBUG TASK: Found f1_score, task = {task}")
            elif "accuracy" in ml:
                task = "classification"
                print(f"DEBUG TASK: Found accuracy, task = {task}")
            else:
                task = "regression"
                print(f"DEBUG TASK: No classification metrics found, task = {task}")
        else:
            print("DEBUG TASK: No ML data available, task = unknown")
        
        # Balance detection (from computed ratio) with VALIDATION
        if not ml:
            raise ValueError("Phase6: ml_training section missing")
        
        class_imbalance = ml.get("class_imbalance_details", {})
        ratio = class_imbalance.get("ratio", 1.0)
        
        print(f"DEBUG PROFILER: ML imbalance ratio: {ratio}")
        
        balance = ""
        if ratio <= 1.5:
            balance = "balanced"
        elif ratio <= 3.0:
            balance = "moderately_imbalanced"
        else:
            balance = "highly_imbalanced"
        
        # Domain detection using weighted scoring across ALL columns
        keywords = {
            "finance": ["loan", "credit", "bank"],  # Removed "income" to avoid false positives
            "health": ["patient", "medical", "disease"],
            "social_media": ["tweet", "post", "comment"],
            "ecommerce": ["product", "price", "order"],
            "demographic": ["age", "gender", "race", "country", "education", "marital", "workclass"]
        }
        
        score = {k: 0 for k in keywords}
        
        # Score across ALL available columns
        for col in columns:
            col_lower = col.lower()
            for domain, words in keywords.items():
                for w in words:
                    if w in col_lower:
                        score[domain] += 1
        
        print(f"DEBUG DOMAIN: Column scores: {score}")
        
        # Return "general" if highest score is less than 2 matches
        best = max(score, key=score.get)
        domain = best if score[best] >= 2 else "general"
        
        print(f"DEBUG DOMAIN: Best domain: {domain} (score: {score[best]})")
        
        print(f"DEBUG PROFILER: Detected - size: {size}, task: {task}, balance: {balance}, domain: {domain}")
        
        # Generate compact structural fingerprint
        domain_codes = {
            "demographic": "demo",
            "finance": "fin", 
            "health": "health",
            "social_media": "soc",
            "general": "gen"
        }
        
        task_codes = {
            "classification": "cls",
            "regression": "reg",
            "unknown": "unk"
        }
        
        size_codes = {
            "tiny": "T",
            "small": "S", 
            "medium": "M",
            "large": "L"
        }
        
        balance_codes = {
            "balanced": "B",
            "moderately_imbalanced": "MI",
            "highly_imbalanced": "HI"
        }
        
        domain_code = domain_codes.get(domain, "gen")
        task_code = task_codes.get(task, "unk")
        size_code = size_codes.get(size, "M")
        balance_code = balance_codes.get(balance, "B")
        
        structural_fingerprint = f"{domain_code}-{task_code}-{size_code}-{balance_code}"
        
        result = {
            "domain": domain,
            "task": task,
            "size": size,
            "balance": balance,
            "dataset_type": dataset_type,  # CRITICAL FIX: Add dataset_type
            "fingerprint": structural_fingerprint,
            "evidence": {
                "row_count": row_count,
                "column_count": len(columns),
                "dataset_type": dataset_type,
                "target_column": target_col
            }
        }
        
        print(f"DEBUG PROFILER: Final profile: {result}")
        return result
    
    def _detect_size(self, row_count: int) -> str:
        """Detect size category using deterministic thresholds."""
        if row_count < 1000:
            return "tiny"
        elif row_count < 10000:
            return "small"
        elif row_count < 100000:
            return "medium"
        else:
            return "large"
    
    def _detect_task(self, ml: Dict[str, Any], target_col: str, dataset_info: Dict[str, Any]) -> str:
        """Detect task type from ML training, target column, and actual data."""
        evidence = []
        
        # CRITICAL FIX: Read actual task_type from ML training if available
        if ml and ml.get("model_trained"):
            task_type = ml.get("task_type")
            if task_type:
                print(f"DEBUG PHASE6: Found task_type from ML: {task_type}")
                return task_type
            
            # Fallback: Evidence from ML metrics
            metrics = ml.get("metrics", {})
            if "accuracy" in metrics or "f1_score" in metrics:
                evidence.append("classification")
            if "mse" in metrics or "mae" in metrics or "r2_score" in metrics:
                evidence.append("regression")
        
        # Evidence from target column
        target_lower = target_col.lower()
        if any(word in target_lower for word in ["approved", "default", "fraud", "churn", "admission", "attrition"]):
            evidence.append("binary_classification")
        elif any(word in target_lower for word in ["category", "type", "grade", "level", "class"]):
            evidence.append("multi_classification")
        elif any(word in target_lower for word in ["income", "salary", "price", "score", "age"]):
            evidence.append("regression")
        
        # CRITICAL FIX: Check actual target unique values from dataset
        if dataset_info and "target_column" in dataset_info:
            try:
                # This should be passed from the actual dataset analysis
                target_unique_count = dataset_info.get("target_unique_count", 0)
                print(f"DEBUG PHASE6: Target unique count: {target_unique_count}")
                if target_unique_count > 0:
                    if target_unique_count <= 20:
                        evidence.append("classification")
                        # Remove regression evidence if it's actually classification
                        evidence = [e for e in evidence if e != "regression"]
                    else:
                        evidence.append("regression")
            except Exception:
                pass
        
        # Determine primary task
        if "binary_classification" in evidence:
            return "binary_classification"
        elif "multi_classification" in evidence:
            return "multi_classification"
        elif "regression" in evidence:
            return "regression"
        elif "classification" in evidence:
            return "classification"
        else:
            return "unknown"
    
    def _detect_balance(self, bias: Dict[str, Any]) -> str:
        """Detect balance category from computed ratio."""
        class_imbalance = bias.get("class_imbalance_details", {})
        ratio = class_imbalance.get("ratio", 1.0)
        
        if ratio <= 1.5:
            return "balanced"
        elif ratio <= 3.0:
            return "moderately_imbalanced"
        else:
            return "highly_imbalanced"
    
    def _detect_domain(self, columns: list, target_col: str, bias: Dict[str, Any]) -> str:
        """Detect domain from ALL column names, not just target."""
        evidence = {}
        
        # CRITICAL FIX: Scan ALL column names, not just target
        all_columns = ' '.join(columns + [target_col]).lower()
        
        # Score each domain based on keyword presence across ALL columns
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_columns)
            evidence[domain] = score
        
        # Additional scoring for target column (higher weight)
        target_lower = target_col.lower()
        if any(word in target_lower for word in ["income", "salary", "credit", "loan", "payment"]):
            evidence["finance"] = evidence.get("finance", 0) + 2
        elif any(word in target_lower for word in ["disease", "medical", "patient", "health"]):
            evidence["health"] = evidence.get("health", 0) + 2
        elif any(word in target_lower for word in ["tweet", "comment", "post", "sentiment"]):
            evidence["social_media"] = evidence.get("social_media", 0) + 2
        elif any(word in target_lower for word in ["employee", "attrition", "promotion", "hire"]):
            evidence["hr"] = evidence.get("hr", 0) + 2
        elif any(word in target_lower for word in ["student", "grade", "education", "admission"]):
            evidence["education"] = evidence.get("education", 0) + 2
        
        # Find best domain
        if evidence:
            best_domain = max(evidence, key=evidence.get)
            best_score = evidence[best_domain]
            
            # CRITICAL FIX: Return "general" if confidence is low (score < 2)
            if best_score >= 2:
                return best_domain
            else:
                print(f"DEBUG: Low domain confidence ({best_score}), returning 'general'")
                return "general"
        else:
            return "general"
