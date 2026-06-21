from http.server import BaseHTTPRequestHandler
import json
import numpy as np

with open("q-vercel-latency.json", "r") as f:
    data = json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))

        regions = body["regions"]
        threshold = body["threshold_ms"]

        result = {}

        for region in regions:
            rows = [r for r in data if r["region"] == region]

            latencies = [r["latency_ms"] for r in rows]
            uptimes = [r["uptime_pct"] for r in rows]

            result[region] = {
                "avg_latency": sum(latencies) / len(latencies),
                "p95_latency": float(np.percentile(latencies, 95)),
                "avg_uptime": sum(uptimes) / len(uptimes),
                "breaches": sum(1 for x in latencies if x > threshold)
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(result).encode())
