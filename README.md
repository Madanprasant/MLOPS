# Student Placement Prediction System

## Project Overview

This project demonstrates an end-to-end MLOps workflow for a simple student placement prediction system. It trains a Logistic Regression model to predict whether a student will be placed (1) or not (0) based on the following features:

- `cgpa` (float)
- `internships` (int)
- `projects` (int)
- `communication` (float)

Files:

- `train.py` - training script with MLflow integration, saves `model.pkl`
- `app.py` - Flask API that loads `model.pkl` and exposes `/predict`
- `placement.csv` - sample dataset
- `requirements.txt` - Python dependencies
- `Dockerfile` - container specification

## Training and MLflow

1. Install dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

2. Start MLflow UI (optional) to view experiments:

```bash
mlflow ui --port 5001
```

3. Train the model and log to MLflow:

```bash
python train.py --data-path placement.csv
```

This will:

- Train a `LogisticRegression` model
- Log parameters and accuracy to MLflow under the experiment `student-placement-experiment`
- Save a `model.pkl` file and log it as an artifact

## Running the API locally

Start the Flask app (after training so `model.pkl` exists):

```bash
python app.py
```

The service will be available at `http://0.0.0.0:5000/` and the prediction endpoint is `POST /predict`.

Example request:

```bash
curl -X POST http://0.0.0.0:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"cgpa":8.1,"internships":1,"projects":4,"communication":8}'
```

Example response:

```json
{"prediction": 1, "probability": 0.87}
```

## Docker

Build and run with Docker:

```bash
docker build -t mlops-placement:latest .
docker run -p 5000:5000 mlops-placement:latest
```

The container runs the Flask app via `gunicorn` and listens on port `5000`.

## Railway Deployment (summary)

1. Create a new Railway project and link your GitHub repository.
2. Ensure `Dockerfile` is present (this project includes one). Railway can build using the Dockerfile.
3. Set any required environment variables (not required for this simple app).
4. Deploy; set the service port to `5000` if asked. Railway will map to an external URL.

Notes:

- For production deployments, ensure you store trained models in a persistent artifact store and use CI to retrain and promote models.
- Consider adding health checks, logging, and authentication for a real-world app.
