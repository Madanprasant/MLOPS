import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import pickle
import os

def train_model():
    """Trains a Logistic Regression model on the placement dataset and logs to MLflow."""
    # 1. Load dataset using pandas
    print("Loading dataset...")
    df = pd.read_csv('placement.csv')
    
    # Feature columns and target
    X = df[['cgpa', 'internships', 'projects', 'communication']]
    y = df['placed']
    
    # 2. Perform train test split (80% training, 20% testing)
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Integrate MLflow experiment tracking
    mlflow.set_experiment("Student_Placement_Prediction")
    
    with mlflow.start_run():
        print("Training model...")
        # Train Logistic Regression model
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        # Predict on test set
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained. Accuracy: {accuracy:.4f}")
        
        # 4. Log parameters, metrics and model
        mlflow.log_param("model_type", "Logistic Regression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        
        mlflow.log_metric("accuracy", accuracy)
        
        mlflow.sklearn.log_model(model, "logistic_regression_model")
        print("Metrics and parameters logged to MLflow.")
        
        # 5. Save trained model as model.pkl using pickle
        model_path = 'model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model saved successfully to {model_path}")

if __name__ == '__main__':
    train_model()
