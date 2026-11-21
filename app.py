import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "name": "EAD AI CLIPPER",
        "status": "Backend is running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/generate-title", methods=["POST"])
def generate_title():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Topic required"}), 400

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return jsonify({"error": "API key not configured"}), 500

    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Create 5 catchy YouTube Shorts titles for: {topic}"
        )
        return jsonify({"titles": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
  
