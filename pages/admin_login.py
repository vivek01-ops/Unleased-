import streamlit as st
import sqlite3


# Database connection
conn = sqlite3.connect("admin.db", check_same_thread=False)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    phone_number TEXT,
    username TEXT UNIQUE
)
''')
conn.commit()

# Streamlit Page Configuration
st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.title("🔐 Admin Authentication")

# Navigation between Login and Register
choice = st.radio("Select an option:", ["Login", "Register"], horizontal=True)

if choice == "Register":
    st.subheader("Register")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    phone_number = st.text_input("Phone Number")
    username = st.text_input("Username")

    if st.button("Register", use_container_width=True):
        if password == confirm_password:
            try:
                cursor.execute("INSERT INTO users (full_name, email, password, phone_number, username) VALUES (?, ?, ?, ?, ?)",
                               (full_name, email, password, phone_number, username))
                conn.commit()
                st.success("User registered successfully! You can now log in.")
            except sqlite3.IntegrityError:
                st.error("Username or Email already exists.")
        else:
            st.error("Passwords do not match!")

elif choice == "Login":
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", use_container_width=True):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (login_username, login_password))
        user = cursor.fetchone()
        if user:
            st.success(f"Welcome, {user[1]}!")  # Display user's full name
            st.switch_page('pages/admin_dashboard.py')
        else:
            st.error("Invalid username or password.")

# Close the database connection
conn.close()
