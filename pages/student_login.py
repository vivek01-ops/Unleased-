import streamlit as st
import sqlite3

def create_database():
    conn = sqlite3.connect("student_db.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT,
                        email TEXT UNIQUE,
                        phone_number TEXT,
                        username TEXT UNIQUE,
                        password TEXT,
                        degree TEXT,
                        year_of_graduation TEXT,
                        college_name TEXT,
                        interest_area TEXT,
                        skills TEXT,
                        bio TEXT
                    )''')
    conn.commit()
    conn.close()

def register_user(full_name, email, phone_number, username, password, degree, year_of_graduation, college_name, interest_area, skills, bio):
    conn = sqlite3.connect("student_db.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (full_name, email, phone_number, username, password, degree, year_of_graduation, college_name, interest_area, skills, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (full_name, email, phone_number, username, password, degree, year_of_graduation, college_name, interest_area, skills, bio))
        conn.commit()
        st.success("User registered successfully! You can now log in.")
    except sqlite3.IntegrityError:
        st.error("Username or Email already exists!")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("student_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.title("Student Authontication")

create_database()

choice = st.radio("Select an option:", ["Login", "Register"], horizontal=True)

if choice == "Login":
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", use_container_width=True):
        user = login_user(login_username, login_password)
        if user:
            st.success(f"Welcome, {user[1]}!")
        else:
            st.error("Invalid username or password!")

elif choice == "Register":
    with st.expander("Formal Details", expanded=True):
        st.subheader("Register")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        phone_number = st.text_input("Phone Number")
        username = st.text_input("Username")
    
    with st.expander("Academic Details"):
        st.subheader("Academic Details")
        degree = st.text_input("Degree")
        year_of_graduation = st.selectbox("Year of Graduation", ("FY", "SY", "TY", "Final Year"), index=None)
        college_name = st.text_input("College Name")

    with st.expander("Interest Areas"):
        st.subheader("Interest Areas")
        interest_area = st.text_input("Interest Area")
        skills = st.text_input("Skills")
        bio = st.text_area("Bio")

    if st.button("Register", use_container_width=True):
        if password == confirm_password:
            register_user(full_name, email, phone_number, username, password, degree, year_of_graduation, college_name, interest_area, skills, bio)
        else:
            st.error("Passwords do not match!")
