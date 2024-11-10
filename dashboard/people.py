import streamlit as st
import pandas as pd
import requests

# API URL
API_URL = "http://127.0.0.1:5000/people" 

st.title("People CRUD Operations")

# Operation selector
operation = st.sidebar.selectbox("Choose CRUD Operation", ["Create", "Get", "Update", "Delete"])

#Create 
if operation == "Create":
   with st.form("create_person_form"):
      st.header("Create a Person")

      # form for the people 
      first_name = st.text_input("First Name")
      last_name = st.text_input("Last Name")
      telephone = st.text_input("Telephone")
      email = st.text_input("Email")
      city = st.text_input("City")
      country = st.text_input("Country")
      android = st.checkbox("Android User")
      ios = st.checkbox("iOS User")
      desktop = st.checkbox("Desktop User")
      
      submit_button = st.form_submit_button("Create Person")
      
      if submit_button:
         # Create payload
         data = {
            "first_name": first_name,
            "last_name": last_name,
            "telephone": telephone,
            "email": email,
            "city": city,
            "country": country,
            "android": android,
            "ios": ios,
            "desktop": desktop
         }
         
         if not first_name or not last_name or not email or not city or not country:
            st.error("First name, last name, city, country and email are required fields.")
         else:
            #post request to the backend 
            response = requests.post(API_URL + "/", json=data)
            
            if response.status_code == 201:
               st.success("Person created successfully!")
               st.json(response.json())
            else:
               st.error("Failed to create person.")
               st.json(response.json())

# Get 
elif operation == "Get":
   with st.form("get_person_form"):
      st.header("Get a Person")

      # Input field for person ID
      pid = st.number_input("Person ID (pid)", min_value=1)
      submit_button = st.form_submit_button("Get Person")
      if submit_button:
         response = requests.get(f"{API_URL}/{pid}")
         if response.status_code == 200:
            st.success("Person retrieved successfully!")
            st.json(response.json())
         else:
            st.error("Person not found.")
            st.json(response.json())

# Update
elif operation == "Update":
   with st.form("update_person_form"):
      st.header("Update a Person")

      # Input fields for person ID and details to update
      pid = st.number_input("Person ID (pid) to Update", min_value=1)
      first_name = st.text_input("First Name")
      last_name = st.text_input("Last Name")
      telephone = st.text_input("Telephone")
      email = st.text_input("Email")
      city = st.text_input("City")
      country = st.text_input("Country")
      android = st.checkbox("Android User")
      ios = st.checkbox("iOS User")
      desktop = st.checkbox("Desktop User")
      submit_button = st.form_submit_button("Update Person")
      if submit_button:
         # Create payload
         data = {
            "first_name": first_name,
            "last_name": last_name,
            "telephone": telephone,
            "email": email,
            "city": city,
            "country": country,
            "android": android,
            "ios": ios,
            "desktop": desktop
         }

         if not first_name or not last_name or not email or not city or not country:
            st.error("First name, last name, city, country and email are required fields.")
         else:
            # Send PUT request to update person
            response = requests.put(f"{API_URL}/{pid}", json=data)
            if response.status_code == 200:
               st.success("Person updated successfully!")
               st.json(response.json())
            else:
               st.error("Failed to update person.")
               st.json(response.json())

# Delete
elif operation == "Delete":
   with st.form("delete_person_form"):
      st.header("Delete a Person")

      # Input field for person ID to remove
      pid = st.number_input("Person ID (pid) to Delete", min_value=1, step=1)

      submit_button = st.form_submit_button("Delete Person")
      if submit_button:
         # Remove element from the db
         response = requests.delete(f"{API_URL}/{pid}")
         if response.status_code == 200:
            st.success("Person deleted successfully!")
            st.json(response.json())
         else:
            st.error("Failed to delete person.")
            st.json(response.json())
