import csv
import os
from datetime import datetime

DIE_FILE = "data/dies.csv"
ISSUE_FILE = "data/issued_dies.csv"

# Ensure the data folder and files exist
os.makedirs("data", exist_ok=True)

if not os.path.exists(ISSUE_FILE):
    with open(ISSUE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Die_ID", "Machine", "Customer", "Issue_Date", "Return_Date", "Wire_Drawn"])

def issue_die(die_id, machine, customer):
    """Issue a die to a machine and customer."""
    dies = []
    with open(DIE_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == die_id and row[3] == "Available":
                row[3] = "Issued"
            dies.append(row)

    with open(DIE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(dies)

    with open(ISSUE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([die_id, machine, customer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "", "0"])
    
    print(f"Die {die_id} issued to {machine} for {customer}.")

def return_die(die_id, wire_drawn):
    """Mark a die as returned and update wire drawn."""
    issues = []
    with open(ISSUE_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == die_id and row[4] == "":
                row[4] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row[5] = wire_drawn
            issues.append(row)

    with open(ISSUE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(issues)

    dies = []
    with open(DIE_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == die_id:
                row[3] = "Available"
            dies.append(row)

    with open(DIE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(dies)

    print(f"Die {die_id} returned. Wire drawn: {wire_drawn}")

if __name__ == "__main__":
    while True:
        print("\n1. Issue Die\n2. Return Die\n3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            die_id = input("Enter Die ID: ")
            machine = input("Enter Machine: ")
            customer = input("Enter Customer: ")
            issue_die(die_id, machine, customer)
        elif choice == "2":
            die_id = input("Enter Die ID: ")
            wire_drawn = input("Enter Wire Drawn: ")
            return_die(die_id, wire_drawn)
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")
