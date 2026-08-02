import pandas as pd
import numpy as np
import os

def generate_custom_factory_dataset(num_rows=5000):
    print(f"Generating custom factory dataset for 4 specific machines with {num_rows} records...")
    np.random.seed(42)
    
    product_ids = [f"P{str(i).zfill(3)}" for i in np.random.randint(1, 300, size=num_rows)]
    
    # Exactly 4 named machines in the bearing factory
    machine_names = ['Lathe_M1', 'Grinding_M2', 'Polishing_M3', 'Assembly_M4']
    machine_ids = np.random.choice(machine_names, size=num_rows)
    
    machine_status = np.random.choice(['Idle', 'Busy', 'Overloaded'], size=num_rows, p=[0.2, 0.6, 0.2])
    queue_length = np.random.randint(0, 25, size=num_rows)
    processing_time = [f"{np.random.randint(3, 15)} min" for _ in range(num_rows)]
    worker_available = np.random.choice(['Yes', 'No'], size=num_rows, p=[0.85, 0.15])
    shift = np.random.choice(['Morning', 'Evening', 'Night'], size=num_rows)
    material_type = np.random.choice(['Bearing', 'Steel Ring', 'Alloy Housing'], size=num_rows)
    temperature = [f"{np.random.randint(28, 75)}°C" for _ in range(num_rows)]
    previous_wait_time = [f"{np.random.randint(1, 20)} min" for _ in range(num_rows)]
    current_wait_time = [f"{np.random.randint(2, 25)} min" for _ in range(num_rows)]
    next_machine = np.random.choice(machine_names, size=num_rows)
    
    df = pd.DataFrame({
        'Product_ID': product_ids,
        'Machine_ID': machine_ids,
        'Machine_Status': machine_status,
        'Queue_Length': queue_length,
        'Processing_Time': processing_time,
        'Worker_Available': worker_available,
        'Shift': shift,
        'Material_Type': material_type,
        'Temperature': temperature,
        'Previous_Wait_Time': previous_wait_time,
        'Current_Wait_Time': current_wait_time,
        'Next_Machine': next_machine
    })
    
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "factory_flow_data.csv")
    
    df.to_csv(file_path, index=False)
    print(f"Success! 4-machine dataset created and saved to: {file_path}")

if __name__ == "__main__":
    generate_custom_factory_dataset(5000)


