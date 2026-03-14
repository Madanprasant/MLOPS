import os
import pickle


from flask import Flask, jsonify, request, render_template
import numpy as np

# Load model path
MODEL_PATH = os.path.join(os.getcwd(), "model.pkl")


def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Run `train.py` first.")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model


app = Flask(__name__)

# Attempt to load the model at import/startup. If missing, `model` stays None and
# the `/predict` endpoint will return an informative error.
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    # Validate input
    required = ["cgpa", "internships", "projects", "communication"]
    if not all(k in data for k in required):
        return (
            jsonify({"error": f"Missing fields. Required: {required}"}),
            400,
        )

    try:
        features = [
            float(data["cgpa"]),
            int(data["internships"]),
            int(data["projects"]),
            float(data["communication"]),
        ]
    except Exception as e:
        return jsonify({"error": "Invalid input types", "details": str(e)}), 400

    if model is None:
        return jsonify({"error": "Model is not loaded on the server. Please check server logs."}), 500

    try:
        arr = np.array(features).reshape(1, -1)
        pred = int(model.predict(arr)[0])
        prob = None
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(arr)[0, 1])

        return jsonify({"prediction": pred, "probability": prob})
    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500


if __name__ == "__main__":
    # Ensure host/port are set for cloud deployment
    app.run(host="0.0.0.0", port=5000)
