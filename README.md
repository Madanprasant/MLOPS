# Student Placement Prediction System

## Project Overview
This project is an end-to-end MLOps machine learning application designed to predict student placements based on relevant academic and extracurricular features. The system is built using Python, trained via scikit-learn (Logistic Regression), tracked with MLflow, and served as a RESTful web API using Flask. 

### Features Used:
- **cgpa**: Cumulative Grade Point Average (e.g. 8.5)
- **internships**: Number of internships completed (e.g. 2)
- **projects**: Number of projects completed (e.g. 3)
- **communication**: Communication skills rating or binary flag (e.g. 1)

**Target**: `placed` (1 for Yes, 0 for No)

## Run Locally
1. Clone the repository and navigate to the project directory:
   ```bash
   cd mlops-placement
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the training script to generate `model.pkl`:
   ```bash
   python train.py
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Test the prediction endpoint (`POST /predict`):
   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"cgpa": 8.5, "internships": 2, "projects": 3, "communication": 1}'
   ```

## MLflow Usage
This project integrates MLflow for experiment tracking and metric logging.
When you run `python train.py`, it automatically logs the model type, accuracy parameters, and the model artifact in the `mlruns/` directory.

To view the MLflow UI:
```bash
mlflow ui
```
Then open `http://127.0.0.1:5000` (or whatever port MLflow binds to, usually 5000) in your browser to analyze your experiment runs. Note: if Flask is also on 5000, you can run MLflow on another port:
```bash
mlflow ui --port 5001
```

## Docker Build and Run Commands
We have provided a `Dockerfile` to containerize the API.

1. First build the model locally so `model.pkl` is available to copy:
   ```bash
   python train.py
   ```
2. Build the Docker image:
   ```bash
   docker build -t placement-app .
   ```
3. Run the Docker container on port 5000:
   ```bash
   docker run -d -p 5000:5000 placement-app
   ```
4. Your API is now running isolated inside the container and mapped to your host's 5000 port!

## Railway Deployment Steps
To easily deploy this container to the cloud using Railway.app:

1. Create a GitHub repository and commit your code, making sure to include `model.pkl` (You can ignore `mlruns/` via `.gitignore`).
2. Log into [Railway](https://railway.app/).
3. Click **New Project** -> **Deploy from GitHub repo**.
4. Select your newly created repository.
5. Railway will automatically detect the `Dockerfile` and build it.
6. Once deployed, Railway provides a public URL (e.g., `https://your-app.up.railway.app`).
7. You can now send `POST /predict` requests to the secure Railway endpoint.
