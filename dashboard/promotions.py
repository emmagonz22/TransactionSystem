import streamlit as st
import requests

# API URL
API_URL = "http://127.0.0.1:5000/promotions"

st.title("Promotions CRUD Operations")

# Operation selector
operation = st.sidebar.selectbox("Choose CRUD Operation", ["Create", "Get", "Update", "Delete"])

# Create
if operation == "Create":
   with st.form("create_promotion_form"):
      st.header("Create a Promotion")

      # Form for the promotion
      client_email = st.text_input("Client Email")
      telephone = st.text_input("Telephone")
      promotion = st.text_input("Promotion Description")
      responded = st.checkbox("Responded")

      submit_button = st.form_submit_button("Create Promotion")

      if submit_button:
         # Create payload
         data = {
            "client_email": client_email,
            "telephone": telephone,
            "promotion": promotion,
            "responded": responded
         }
         
         if not client_email or not promotion or not telephone or not responded:
            st.error("Client email, telephone, responded and promotion description are required fields.")
         else:
            # POST request to the backend
            response = requests.post(API_URL + "/", json=data)
            
            if response.status_code == 201:
               st.success("Promotion created successfully!")
               st.json(response.json())
            else:
               st.error("Failed to create promotion.")
               st.json(response.json())

# Get
elif operation == "Get":
   with st.form("get_promotion_form"):
      st.header("Get a Promotion")

      # Input field for promotion ID
      prid = st.number_input("Promotion ID (prid)", min_value=1)
      submit_button = st.form_submit_button("Get Promotion")
      
      if submit_button:
         response = requests.get(f"{API_URL}/{prid}")
         if response.status_code == 200:
            st.success("Promotion retrieved successfully!")
            st.json(response.json())
         else:
            st.error("Promotion not found.")
            st.json(response.json())

# Update
elif operation == "Update":
   with st.form("update_promotion_form"):
      st.header("Update a Promotion")

      # Input fields for promotion ID and details to update
      prid = st.number_input("Promotion ID (prid) to Update", min_value=1)
      client_email = st.text_input("Client Email")
      telephone = st.text_input("Telephone")
      promotion = st.text_input("Promotion Description")
      responded = st.checkbox("Responded")
      
      submit_button = st.form_submit_button("Update Promotion")
      
      if submit_button:
         # Create payload
         data = {
            "client_email": client_email,
            "telephone": telephone,
            "promotion": promotion,
            "responded": responded
         }

         if not client_email or not promotion:
            st.error("Client email and promotion description are required fields.")
         else:
            # Send PUT request to update promotion
            response = requests.put(f"{API_URL}/{prid}", json=data)
            if response.status_code == 200:
               st.success("Promotion updated successfully!")
               st.json(response.json())
            else:
               st.error("Failed to update promotion.")
               st.json(response.json())

# Delete
elif operation == "Delete":
   with st.form("delete_promotion_form"):
      st.header("Delete a Promotion")

      # Input field for promotion ID to delete
      prid = st.number_input("Promotion ID (prid) to Delete", min_value=1, step=1)

      submit_button = st.form_submit_button("Delete Promotion")
      
      if submit_button:
         # DELETE request to remove the promotion
         response = requests.delete(f"{API_URL}/{prid}")
         if response.status_code == 200:
            st.success("Promotion deleted successfully!")
            st.json(response.json())
         else:
            st.error("Failed to delete promotion.")
            st.json(response.json())
