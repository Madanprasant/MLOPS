import argparse
import os
import pickle

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_data(path: str):
    df = pd.read_csv(path)
    return df


def train(args):
    # Load dataset
    df = load_data(args.data_path)

    # Features and target
    X = df[["cgpa", "internships", "projects", "communication"]]
    y = df["placed"]

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # Create and train model with more regularization to avoid sharp probability jumps
    model = LogisticRegression(max_iter=args.max_iter, C=0.01)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    # MLflow tracking
    mlflow.set_experiment(args.experiment_name)
    with mlflow.start_run():
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("max_iter", args.max_iter)
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_metric("accuracy", float(accuracy))

        # Log the sklearn model artifact
        mlflow.sklearn.log_model(model, artifact_path="sklearn-model")

        # Also save a pickle for easy loading in the Flask app
        model_path = os.path.join(os.getcwd(), "model.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        mlflow.log_artifact(model_path)

    print(f"Training complete. Accuracy: {accuracy:.4f}")
    print(f"Model saved to {model_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Train placement prediction model")
    parser.add_argument("--data-path", type=str, default="placement.csv", help="Path to CSV dataset")
    parser.add_argument("--experiment-name", type=str, default="student-placement-experiment", help="MLflow experiment name")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set fraction")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument("--max-iter", type=int, default=1000, help="Max iterations for LogisticRegression")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args)
