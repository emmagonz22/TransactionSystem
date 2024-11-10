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
    st.header("Create a Person")

    # Input fields for person details
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    telephone = st.text_input("Telephone")
    email = st.text_input("Email")
    city = st.text_input("City")
    country = st.text_input("Country")

    if st.button("Create Person"):
        # Create payload
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "telephone": telephone,
            "email": email,
            "city": city,
            "country": country
        }

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
    st.header("Get a Person")

    # Input field for person ID
    pid = st.number_input("Person ID (pid)", min_value=1)

    if st.button("Get Person"):
        response = requests.get(f"{API_URL}/{pid}")
        if response.status_code == 200:
            st.success("Person retrieved successfully!")
            st.json(response.json())
        else:
            st.error("Person not found.")
            st.json(response.json())

# Update
elif operation == "Update":
    st.header("Update a Person")

    # Input fields for person ID and details to update
    pid = st.number_input("Person ID (pid) to Update", min_value=1)
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    telephone = st.text_input("Telephone")
    email = st.text_input("Email")
    city = st.text_input("City")
    country = st.text_input("Country")

    if st.button("Update Person"):
        # Create payload
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "telephone": telephone,
            "email": email,
            "city": city,
            "country": country
        }

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
    st.header("Delete a Person")

    # Input field for person ID to remove
    pid = st.number_input("Person ID (pid) to Delete", min_value=1, step=1)

    if st.button("Delete Person"):
        # Remove element from the db
        response = requests.delete(f"{API_URL}/{pid}")
        if response.status_code == 200:
            st.success("Person deleted successfully!")
            st.json(response.json())
        else:
            st.error("Failed to delete person.")
            st.json(response.json())
