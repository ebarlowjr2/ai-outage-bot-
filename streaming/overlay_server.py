from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def serve_overlay():
    return send_file("streaming/overlay/overlay.html")

@app.route("/data")
def serve_data():
    return send_file("streaming/overlay/output.txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
