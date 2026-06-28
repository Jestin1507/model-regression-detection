"""
HTML Report Generator
"""

from pathlib import Path
import json


class ReportGenerator:

    def __init__(self):

        self.history_file = Path(
            "reports/json/comparison_history.json"
        )

        self.output_file = Path(
            "reports/html/comparison_report.html"
        )

    def generate(self):

        if not self.history_file.exists():
            return

        with open(
            self.history_file,
            "r",
            encoding="utf-8",
        ) as f:

            history = json.load(f)

        rows = ""

        for record in history:

            accuracy = record["accuracy"] * 100

            if accuracy >= 95:
                color = "#d4edda"
                status = "✅ Excellent"

            elif accuracy >= 80:
                color = "#fff3cd"
                status = "🟡 Good"

            else:
                color = "#f8d7da"
                status = "🚨 Regression"

            rows += f"""
            <tr style="background:{color};">
                <td>{record['timestamp']}</td>
                <td>{record['provider']}</td>
                <td>{record['prompt']}</td>
                <td>{accuracy:.2f}%</td>
                <td>{status}</td>
            </tr>
            """

        html = f"""
<!DOCTYPE html>

<html>

<head>

<title>LLM Evaluation Report</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f7f7f7;
}}

table{{
width:100%;
border-collapse:collapse;
}}

th,td{{
padding:12px;
border:1px solid #ccc;
text-align:center;
}}

th{{
background:#222;
color:white;
}}

h1{{
text-align:center;
}}

</style>

</head>

<body>

<h1>Model Regression Detection Report</h1>

<table>

<tr>

<th>Timestamp</th>

<th>Provider</th>

<th>Prompt</th>

<th>Accuracy</th>

<th>Status</th>

</tr>

{rows}

</table>

</body>

</html>
"""

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.output_file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(html)

        print("\nHTML report generated successfully.")