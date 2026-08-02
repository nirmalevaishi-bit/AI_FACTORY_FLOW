import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def train_factory_models():
    processed_data_path = os.path.join("data", "processed", "cleaned_factory_data.csv")
    if not os.path.exists(processed_data_path):
        raise FileNotFoundError("Cleaned data not found. Run make_dataset.py first!")
        
    df = pd.read_csv(processed_data_path)
    print("Preparing features and targets for training...")
    
    # Define features input list matching your custom schema
    feature_columns = [
        'Machine_ID', 'Machine_Status', 'Queue_Length', 'Processing_Time', 
        'Worker_Available', 'Shift', 'Material_Type', 'Temperature', 'Previous_Wait_Time'
    ]
    
    X = df[feature_columns]
    y_wait_time = df['Current_Wait_Time']
    y_next_machine = df['Next_Machine']
    
    # Split data (80% training, 20% testing)
    X_train, X_test, y_wait_train, y_wait_test = train_test_split(X, y_wait_time, test_size=0.2, random_state=42)
    _, _, y_machine_train, y_machine_test = train_test_split(X, y_next_machine, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor (for Current Wait Time)...")
    wait_model = RandomForestRegressor(n_estimators=100, random_state=42)
    wait_model.fit(X_train, y_wait_train)
    
    print("Training Random Forest Classifier (for Next Machine Routing)...")
    machine_model = RandomForestClassifier(n_estimators=100, random_state=42)
    machine_model.fit(X_train, y_machine_train)
    
    # Package models into an artifact dictionary
    bundle = {
        "wait_time_model": wait_model,
        "machine_routing_model": machine_model,
        "features": feature_columns
    }
    
    os.makedirs("artifacts", exist_ok=True)
    artifact_path = os.path.join("artifacts", "model.pkl")
    
    joblib.dump(bundle, artifact_path)
    print(f"Backend AI models successfully trained and saved to {artifact_path}!")

if __name__ == "__main__":
    train_factory_models()