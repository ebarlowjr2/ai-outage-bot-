from flask import Flask, send_file, jsonify
import os
import logging

app = Flask(__name__)

@app.route("/")
def serve_overlay():
    """Serve the overlay HTML file"""
    try:
        overlay_path = os.path.join(os.path.dirname(__file__), "overlay", "overlay.html")
        return send_file(overlay_path)
    except FileNotFoundError:
        logging.error("overlay.html not found")
        return "Overlay file not found", 404

@app.route("/data")
def serve_data():
    """Serve the current outage summary data"""
    try:
        output_path = os.path.join(os.path.dirname(__file__), "overlay", "output.txt")
        if os.path.exists(output_path):
            return send_file(output_path)
        else:
            return "No outage data available", 200
    except Exception as e:
        logging.error(f"Error serving data: {e}")
        return "Error loading data", 500

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "AI Outage Bot Overlay Server"})

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting overlay server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
