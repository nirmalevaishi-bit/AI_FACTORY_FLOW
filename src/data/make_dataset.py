
import pandas as pd
import os

def load_and_process_data():
    raw_data_path = os.path.join("data", "raw", "factory_flow_data.csv")
    processed_data_path = os.path.join("data", "processed", "cleaned_factory_data.csv")
    
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_path}. Run generate_large_dataset.py first!")
    
    print("Loading raw factory data...")
    df = pd.read_csv(raw_data_path)
    
    # 1. Clean columns containing text units and convert to numeric values
    if 'Processing_Time' in df.columns:
        df['Processing_Time'] = df['Processing_Time'].astype(str).str.replace(' min', '').astype(float)
    if 'Temperature' in df.columns:
        df['Temperature'] = df['Temperature'].astype(str).str.replace('°C', '').astype(float)
    if 'Previous_Wait_Time' in df.columns:
        df['Previous_Wait_Time'] = df['Previous_Wait_Time'].astype(str).str.replace(' min', '').astype(float)
    if 'Current_Wait_Time' in df.columns:
        df['Current_Wait_Time'] = df['Current_Wait_Time'].astype(str).str.replace(' min', '').astype(float)
        
    # 2. Drop unique IDs that shouldn't affect predictions
    if 'Product_ID' in df.columns:
        df = df.drop(columns=['Product_ID'])
        
    # 3. Encode categorical text columns into numbers
    categorical_cols = ['Machine_ID', 'Machine_Status', 'Worker_Available', 'Shift', 'Material_Type', 'Next_Machine']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes
            
    # 4. Save processed data
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)
    print(f"Cleaned data successfully saved to {processed_data_path}")
    return df

if __name__ == "__main__":
    load_and_process_data()