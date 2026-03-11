from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load saved model.pkl at startup
model = None
MODEL_PATH = 'model.pkl'

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
else:
    print("Warning: model.pkl not found. Please run train.py first to generate the model.")

@app.route('/', methods=['GET'])
def home():
    """Home route - Health check endpoint."""
    return jsonify({
        "message": "Welcome to the Student Placement Prediction System API.",
        "status": "Healthy",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict endpoint - Accepts JSON input and returns prediction."""
    if model is None:
        return jsonify({"error": "Model object is not loaded. Please train the model first."}), 500
        
    try:
        # Accept JSON input for cgpa, internships, projects, communication
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided."}), 400
            
        cgpa = float(data.get('cgpa', 0.0))
        internships = int(data.get('internships', 0))
        projects = int(data.get('projects', 0))
        communication = int(data.get('communication', 0)) # binary or rating 1-5 depending on scale
        
        # Format for sklearn prediction
        input_features = [[cgpa, internships, projects, communication]]
        
        # Return prediction as JSON response
        prediction = model.predict(input_features)[0]
        
        return jsonify({
            "input": {
                "cgpa": cgpa,
                "internships": internships,
                "projects": projects,
                "communication": communication
            },
            "prediction": int(prediction),
            "result": "Placed" if int(prediction) == 1 else "Not Placed"
        })
        
    except ValueError as ve:
        return jsonify({"error": f"Invalid data format: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Ensure application runs on host 0.0.0.0 and port 5000 for cloud deployment
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
