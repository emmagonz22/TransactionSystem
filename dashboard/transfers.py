import streamlit as st
import pandas as pd
import requests
from datetime import date

# API base URL
API_URL = "http://127.0.0.1:5000/transfers"  # Change this if your Flask API runs elsewhere

st.title("Transfer CRUD Operations")

# Operation selection
operation = st.sidebar.selectbox("Choose CRUD Operation", ["Create", "Get", "Update", "Delete"])

# --- Create Operation ---
if operation == "Create":
    st.header("Create a Transfer")

    # Input fields for transfer details
    sender_id = st.number_input("Sender ID", min_value=1, step=1)
    recipient_id = st.number_input("Recipient ID", min_value=1, step=1)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    transfer_date = st.date_input("Date", value=date.today())

    if st.button("Create Transfer"):
        # Create payload
        data = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "amount": amount,
            "date": str(transfer_date)
        }

        # Send POST request to create transfer
        response = requests.post(API_URL + "/", json=data)
        if response.status_code == 201:
            st.success("Transfer created successfully!")
            st.json(response.json())
        else:
            st.error("Failed to create transfer.")
            st.json(response.json())

# --- Get Operation ---
elif operation == "Get":
    st.header("Get a Transfer")

    # Input field for transfer ID
    trid = st.number_input("Transfer ID (trid)", min_value=1, step=1)

    if st.button("Get Transfer"):
        # Send GET request to retrieve transfer details
        response = requests.get(f"{API_URL}/{trid}")
        if response.status_code == 200:
            st.success("Transfer retrieved successfully!")
            st.json(response.json())
        else:
            st.error("Transfer not found.")
            st.json(response.json())

# --- Update Operation ---
elif operation == "Update":
    st.header("Update a Transfer")

    # Input fields for transfer ID and details to update
    trid = st.number_input("Transfer ID (trid) to Update", min_value=1, step=1)
    sender_id = st.number_input("Sender ID", min_value=1, step=1)
    recipient_id = st.number_input("Recipient ID", min_value=1, step=1)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    transfer_date = st.date_input("Date", value=date.today())

    if st.button("Update Transfer"):
        # Create payload
        data = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "amount": amount,
            "date": str(transfer_date)
        }

        # Send PUT request to update transfer
        response = requests.put(f"{API_URL}/{trid}", json=data)
        if response.status_code == 200:
            st.success("Transfer updated successfully!")
            st.json(response.json())
        else:
            st.error("Failed to update transfer.")
            st.json(response.json())

# --- Delete Operation ---
elif operation == "Delete":
    st.header("Delete a Transfer")

    # Input field for transfer ID to delete
    trid = st.number_input("Transfer ID (trid) to Delete", min_value=1, step=1)

    if st.button("Delete Transfer"):
        # Send DELETE request to delete transfer
        response = requests.delete(f"{API_URL}/{trid}")
        if response.status_code == 200:
            st.success("Transfer deleted successfully!")
            st.json(response.json())
        else:
            st.error("Failed to delete transfer.")
            st.json(response.json())
