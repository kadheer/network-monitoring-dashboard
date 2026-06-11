import subprocess
import re
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

TARGETS = ["8.8.8.8", "1.1.1.1", "github.com"]

def ping(host):
    """Run ping and return (latency_ms, packet_loss_percent)"""
    try:
        # it runs ping and returns the latency per milli second and packet percent loss
        output = subprocess.check_output(
            ["ping", "-c", "4", "-W", "2", host],        # its sends 4 pings in 2 secs
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        # loss been extracted
        loss_match = re.search(r"(\d+)% packet loss", output)
        loss = int(loss_match.group(1)) if loss_match else 100
        # rtt avg
        rtt_match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/", output)
        avg_latency = float(rtt_match.group(1)) if rtt_match else None
        return avg_latency, loss
    except subprocess.CalledProcessError:
        return None, 100

def traceroute(host):
    """Run traceroute and return first few hops as list"""
    try:
        output = subprocess.check_output(
            ["traceroute", "-n", "-m", "5", "-w", "1", host],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        hops = []
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit():
                hop_num = parts[0]
                # IP address is usually the second field after hop number
                ip = parts[1] if parts[1] != "*" else "*"
                hops.append({"hop": hop_num, "ip": ip})
        return hops
    except Exception:
        return []

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/metrics")
def get_metrics():
    results = []
    for target in TARGETS:
        latency, loss = ping(target)
        # Only do traceroute if loss is not 100% to save time
        route = traceroute(target) if loss < 100 else []
        results.append({
            "target": target,
            "latency_ms": latency,
            "packet_loss_percent": loss,
            "route": route
        })
    return jsonify(results)

if __name__ == "__main__":
    # all interfaces on port 5000
    app.run(host="0.0.0.0", port=5000, debug=False)
  
