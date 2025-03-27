import streamlit as st
import pandas as pd
import csv
import os

DIE_FILE = "data/dies.csv"
ISSUE_FILE = "data/issued_dies.csv"

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Check if files exist, create if not
if not os.path.exists(DIE_FILE):
    with open(DIE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Die_ID", "Size", "Casing_Size", "Status"])

if not os.path.exists(ISSUE_FILE):
    with open(ISSUE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Die_ID", "Machine", "Customer", "Issue_Date", "Return_Date", "Wire_Drawn"])

# Load die data
def load_dies():
    return pd.read_csv(DIE_FILE)

# Load issued dies data
def load_issued_dies():
    return pd.read_csv(ISSUE_FILE)

# Streamlit App
st.title("🔧 Die Management System")

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Home", "Issue/Return Dies", "Reports"])

if menu == "Home":
    st.subheader("📋 All Dies")
    dies_df = load_dies()
    st.dataframe(dies_df)

elif menu == "Issue/Return Dies":
    st.subheader("🚀 Issue or Return Dies")

    choice = st.radio("Select Action", ["Issue Die", "Return Die"])

    if choice == "Issue Die":
        die_id = st.text_input("Enter Die ID:")
        machine = st.text_input("Enter Machine:")
        customer = st.text_input("Enter Customer:")

        if st.button("Issue Die"):
            dies_df = load_dies()
            if die_id in dies_df["Die_ID"].values:
                with open(ISSUE_FILE, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([die_id, machine, customer, pd.Timestamp.now(), "", "0"])
                dies_df.loc[dies_df["Die_ID"] == die_id, "Status"] = "Issued"
                dies_df.to_csv(DIE_FILE, index=False)
                st.success(f"✅ Die {die_id} issued successfully!")
            else:
                st.error("❌ Die ID not found!")

    elif choice == "Return Die":
        die_id = st.text_input("Enter Die ID to return:")
        wire_drawn = st.text_input("Enter Wire Drawn:")

        if st.button("Return Die"):
            issue_df = load_issued_dies()
            if die_id in issue_df["Die_ID"].values:
                issue_df.loc[issue_df["Die_ID"] == die_id, ["Return_Date", "Wire_Drawn"]] = [pd.Timestamp.now(), wire_drawn]
                issue_df.to_csv(ISSUE_FILE, index=False)

                dies_df = load_dies()
                dies_df.loc[dies_df["Die_ID"] == die_id, "Status"] = "Available"
                dies_df.to_csv(DIE_FILE, index=False)

                st.success(f"✅ Die {die_id} returned successfully!")
            else:
                st.error("❌ Die ID not found in issued records!")

elif menu == "Reports":
    st.subheader("📊 Die Usage Reports")
    issue_df = load_issued_dies()
    st.dataframe(issue_df)

