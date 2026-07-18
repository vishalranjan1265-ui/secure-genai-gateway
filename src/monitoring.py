import time
from typing import List, Dict, Any

class OperationalMetricsTracker:
    def __init__(self) -> None:
        self.total_transactions = 0
        self.total_violations_intercepted = 0
        self.latency_accumulator = 0.0

    def record_transaction(self, latency: float, violations_count: int) -> None:
        self.total_transactions += 1
        self.total_violations_intercepted += violations_count
        self.latency_accumulator += latency

    def compile_metrics_snapshot(self) -> Dict[str, Any]:
        avg_latency = self.latency_accumulator / self.total_transactions if self.total_transactions > 0 else 0.0
        return {
            "total_processed_requests": self.total_transactions,
            "total_security_interceptions": self.total_violations_intercepted,
            "average_latency_seconds": round(avg_latency, 4)
        }

metrics_engine = OperationalMetricsTracker()