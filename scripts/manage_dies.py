import csv
import os

DIE_FILE = "data/dies.csv"

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Check if file exists, create one if not
if not os.path.exists(DIE_FILE):
    with open(DIE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Die_ID", "Size", "Casing_Size", "Status"])

def add_die(die_id, size, casing_size):
    """Add a new die to the system."""
    with open(DIE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([die_id, size, casing_size, "Available"])
    print(f"Die {die_id} added successfully!")

def list_dies():
    """Display all dies."""
    with open(DIE_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

if __name__ == "__main__":
    while True:
        print("\n1. Add Die\n2. List Dies\n3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            die_id = input("Enter Die ID: ")
            size = input("Enter Size: ")
            casing_size = input("Enter Casing Size: ")
            add_die(die_id, size, casing_size)
        elif choice == "2":
            list_dies()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")
