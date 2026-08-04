import os
import random
import pandas as pd
import numpy as np


def generate_factory_data(num_rows=5000):
    print(f"Generating synthetic dataset with {num_rows} records including routing recommendations and expected wait times...")

    # Random seed
    np.random.seed(42)
    random.seed(42)

    # Master data
    product_ids = [f"P{str(i).zfill(4)}" for i in range(1, 501)]
    machine_ids = ["Lathe_M1", "Grinding_M2", "Polishing_M3", "Assembly_M4"]
    machine_statuses = ["Busy", "Idle", "Overloaded", "Maintenance"]
    shifts = ["Morning", "Evening", "Night"]
    material_types = [
        "Bearing_Steel_Chrome",
        "Bearing_Stainless",
        "Ceramic_Hybrid"
    ]
    next_machines = [
        "Grinding_M2",
        "Polishing_M3",
        "Assembly_M4",
        "Packaging_Line"
    ]

    data = []

    # Generate rows
    for _ in range(num_rows):

        prod_id = random.choice(product_ids)
        mach_id = random.choice(machine_ids)
        status = random.choice(machine_statuses)

        queue_len = np.random.randint(0, 25)
        proc_time = np.random.randint(5, 45)

        worker_avail = random.choice(["Yes", "No"])
        shift = random.choice(shifts)
        material = random.choice(material_types)

        temp = np.random.randint(25, 85)
        prev_wait = np.random.randint(2, 30)
        curr_wait = np.random.randint(5, 60)

        next_mach = random.choice(next_machines)

        recommended_machine = random.choice(machine_ids)
        expected_waiting_time = np.random.randint(1, 30)

        data.append({
            "Product_ID": prod_id,
            "Machine_ID": mach_id,
            "Machine_Status": status,
            "Queue_Length": queue_len,
            "Processing_Time": proc_time,
            "Worker_Available": worker_avail,
            "Shift": shift,
            "Material_Type": material,
            "Temperature": temp,
            "Previous_Wait_Time": prev_wait,
            "Current_Wait_Time": curr_wait,
            "Next_Machine": next_mach,
            "Recommended_Machine": recommended_machine,
            "Expected_Waiting_Time": expected_waiting_time
        })

    print("Length of data =", len(data))

    df = pd.DataFrame(data)

    # Create folder if it doesn't exist
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # Save dataset
    file_path = os.path.join(raw_dir, "factory_flow_data.csv")
    df.to_csv(file_path, index=False)

    print("Dataset Shape:", df.shape)
    print(f"Success! Dataset saved to: {file_path}")


# Main Function
if __name__ == "__main__":
    generate_factory_data(5000)