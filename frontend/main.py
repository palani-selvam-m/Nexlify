import streamlit as st
import requests
import pandas as pd
import os

# Load backend API URL from environment variable
backend_api_url = os.getenv("BACKEND_API_URL", "http://backend:8000/users")

st.title("Nexlify User Management")

# Initialize session state for selected option and viewed user
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "viewed_user_id" not in st.session_state:
    st.session_state.viewed_user_id = None

# Top navigation: Create User and Get Users buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Create User", use_container_width=True):
        st.session_state.selected_option = "create"
        st.session_state.viewed_user_id = None
with col2:
    if st.button("Get Users", use_container_width=True):
        st.session_state.selected_option = "get"
        st.session_state.viewed_user_id = None

# Section 1: Create User Form (shown when "Create User" is selected)
if st.session_state.selected_option == "create":
    st.header("Create User")
    with st.form(key="create_user_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label="Create User")

        if submit_button:
            if name and email:
                try:
                    response = requests.post(
                        backend_api_url,
                        json={"name": name, "email": email}
                    )
                    response.raise_for_status()
                    st.success("User created successfully!")
                    # Clear form inputs
                    st.session_state["name"] = ""
                    st.session_state["email"] = ""
                except requests.exceptions.RequestException as e:
                    st.error(f"Error creating user: {e}")
            else:
                st.error("Please provide both name and email.")

# Section 2: Get Users List (shown when "Get Users" is selected)
if st.session_state.selected_option == "get":
    st.header("User List")
    try:
        response = requests.get(backend_api_url)
        response.raise_for_status()
        users = response.json()
        if users:
            # Create a DataFrame with only names and IDs
            df = pd.DataFrame(users)[["id", "name"]]
            # Display the list with a View button for each user
            for index, row in df.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(row["name"])
                with col2:
                    if st.button("View", key=f"view_{row['id']}"):
                        st.session_state.viewed_user_id = row["id"]
        else:
            st.write("No users found.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching users: {e}")

# Section 3: User Details (shown when a View button is clicked)
if st.session_state.viewed_user_id:
    user_id = st.session_state.viewed_user_id
    st.header(f"User Details (ID: {user_id})")
    try:
        response = requests.get(f"{backend_api_url}/{user_id}")
        response.raise_for_status()
        user = response.json()
        st.write(f"**Name**: {user['name']}")
        st.write(f"**Email**: {user['email']}")
        st.write(f"**Created At**: {user['created_at']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user details: {e}")