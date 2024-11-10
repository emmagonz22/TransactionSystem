import streamlit as st
import requests

# API URL
API_URL = "http://127.0.0.1:5000/transaction"

st.title("Transaction CRUD Operations")

# Operation selector
operation = st.sidebar.selectbox("Choose CRUD Operation", ["Create", "Get", "Update", "Delete"])

# Create
if operation == "Create":
   with st.form("create_transaction_form"):
      st.header("Create a Transaction Entry")

      # Form for the transaction entry
      tid = st.number_input("Transaction ID (tid)", min_value=1, step=1)
      item_name = st.text_input("Item Name")
      price = st.number_input("Price", min_value=0.0, step=0.01)
      price_per_item = st.number_input("Price Per Item", min_value=0.0, step=0.01)
      quantity = st.number_input("Quantity", min_value=1, step=1)
      phone = st.text_input("Phone")
      store = st.text_input("Store")
      
      submit_button = st.form_submit_button("Create Transaction Entry")

      if submit_button:
         # Create payload
         data = {
            "tid": tid,
            "item_name": item_name,
            "price": price,
            "price_per_item": price_per_item,
            "quantity": quantity,
            "phone": phone,
            "store": store
         }

         if not item_name or price == 0.0 or quantity <= 0:
            st.error("Item name, price, and quantity are required fields.")
         else:
            # POST request to the backend
            response = requests.post(API_URL + "/", json=data)

            if response.status_code == 201:
               st.success("Transaction entry created successfully!")
               st.json(response.json())
            else:
               st.error("Failed to create transaction entry.")
               st.json(response.json())

# Get
elif operation == "Get":
   with st.form("get_transaction_form"):
      st.header("Get a Transaction Entry")

      # Input field for transaction ID
      tid = st.number_input("Transaction ID (tid)", min_value=1)
      submit_button = st.form_submit_button("Get Transaction Entry")

      if submit_button:
         response = requests.get(f"{API_URL}/{tid}")
         if response.status_code == 200:
            st.success("Transaction entry retrieved successfully!")
            st.json(response.json())
         else:
            st.error("Transaction entry not found.")
            st.json(response.json())

# Update
elif operation == "Update":
   with st.form("update_transaction_form"):
      st.header("Update a Transaction Entry")

      # Input fields for transaction ID and details to update
      # If entry does not exist is going to create a new entry, this should be rewritten
      eid = st.number_input("Entry ID (eid)", min_value=1, step=1)
      tid = st.number_input("Transaction ID (tid) to Update", min_value=1)
      item_name = st.text_input("Item Name")
      price = st.number_input("Price", min_value=0.0, step=0.01)
      price_per_item = st.number_input("Price Per Item", min_value=0.0, step=0.01)
      quantity = st.number_input("Quantity", min_value=1, step=1)
      phone = st.text_input("Phone")
      store = st.text_input("Store")

      submit_button = st.form_submit_button("Update Transaction Entry")

      if submit_button:
         # Create payload
         data = {
            "eid": eid,
            "tid": tid,
            "item_name": item_name,
            "price": price,
            "price_per_item": price_per_item,
            "quantity": quantity,
            "phone": phone,
            "store": store
         }

         if not item_name or price == 0.0 or quantity <= 0:
            st.error("Item name, price, and quantity are required fields.")
         else:
            # PUT request to update transaction
            response = requests.put(f"{API_URL}/entry/{eid}", json=data)
            if response.status_code == 200:
               st.success("Transaction entry updated successfully!")
               st.json(response.json())
            else:
               st.error("Failed to update transaction entry.")
               st.json(response.json())

# Delete
elif operation == "Delete":
   with st.form("delete_transaction_form"):
      st.header("Delete a Transaction Entry")

      # Input field for transaction ID to delete
      tid = st.number_input("Transaction ID (tid) to Delete", min_value=1, step=1)

      submit_button = st.form_submit_button("Delete Transaction Entry")

      if submit_button:
         # DELETE request to remove the transaction entry
         response = requests.delete(f"{API_URL}/{tid}")
         if response.status_code == 200:
            st.success("Transaction entry deleted successfully!")
            st.json(response.json())
         else:
            st.error("Failed to delete transaction entry.")
            st.json(response.json())
