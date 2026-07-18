import os
import csv
import json
from typing import List, Dict, Any
from monitoring import metrics_engine

class ComplianceReportCompiler:
    @staticmethod
    def output_security_matrices(findings_log: List[Dict[str, Any]], target_dir: str) -> None:
        os.makedirs(target_dir, exist_ok=True)
        stats = metrics_engine.compile_metrics_snapshot()
        
        # 1. JSON Export
        with open(os.path.join(target_dir, "security_report.json"), "w", encoding="utf-8") as f:
            json.dump({"summary": stats, "events": findings_log}, f, indent=2)

        # 2. CSV Export
        fields = ["timestamp", "event_type", "resource", "description"]
        with open(os.path.join(target_dir, "security_report.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in findings_log:
                writer.writerow({k: row.get(k, "N/A") for k in fields})

        # 3. Premium Dark Mode Dashboard Presentation Layout
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Secure GenAI Gateway Compliance Matrix</title>
            <style>
                body {{ font-family: 'Inter', sans-serif; background-color: #121212; color: #FFFFFF; padding: 40px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #00E676; border-bottom: 1px solid #1E1E1E; padding-bottom: 12px; font-weight: 700; }}
                .summary-card {{ background-color: #1E1E1E; padding: 20px; border-radius: 8px; margin-bottom: 24px; border: 1px solid #00E676; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #1E1E1E; }}
                th, td {{ padding: 14px 20px; text-align: left; border-bottom: 1px solid #121212; }}
                th {{ color: #8E8E93; background-color: #252525; font-size: 13px; text-transform: uppercase; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Secure GenAI Gateway - Compliance Log Summary</h1>
                <div class="summary-card">
                    <h3>Operational Performance Telemetry Metrics</h3>
                    <p>Total Processed Requests: {stats['total_processed_requests']}</p>
                    <p>Security Interceptions Counter: {stats['total_security_interceptions']}</p>
                    <p>Average Processing Speed: {stats['average_latency_seconds']} seconds</p>
                </div>
            </div>
        </body>
        </html>
        """
        with open(os.path.join(target_dir, "security_report.html"), "w", encoding="utf-8") as f:
            f.write(html_content)