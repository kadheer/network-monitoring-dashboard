# network-monitoring-dashboard
There is this repo where i want to highlight the live latency, packet loss and simple trace route. Firstly I have divided the project into three parts being python script file which is my main file for operations, the second the html file where I want to reflect the backend operations in this html file and lastly the css style file to create db.

# Networking Monitoring Dashboard

Simple dashboard to monitor latency, packet loss, and routing status for a few endpoints. Uses Flask + system ping/traceroute.

## Why I built this
I needed a quick way to see if our office network drops packets to Google DNS or Cloudflare. The auto-refresh every 30 seconds helps spot intermittent issues.

## wie kann man es ausfuhren?
pip install -r requirements.txt
python app.py
