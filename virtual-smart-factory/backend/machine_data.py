import pandas as pd

# Load dataset
file_path = "../../data/processed/final_factory_data.csv"
df = pd.read_csv(file_path)

# Get unique machines
machines = df["Machine_ID"].unique()

print("FACTORY MACHINES")
print("----------------")

for machine in machines:
    machine_data = df[df["Machine_ID"] == machine]

    print("\nMachine:", machine)
    print("Status:", machine_data["Machine_Status"].iloc[0])
    print("Temperature:", machine_data["Temperature"].iloc[0])
    print("Machine Load:", machine_data["Machine_Load"].iloc[0])
    print("Queue Length:", machine_data["Queue_Length"].iloc[0])
    print("Processing Time:", machine_data["Processing_Time"].iloc[0])