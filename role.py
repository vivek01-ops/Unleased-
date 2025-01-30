import streamlit as st
import sqlite3

st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.title("👥 What's your role?")

col1, col2 = st.columns(2)

with col1:
    if st.button("Admin", use_container_width=True):
        st.switch_page("pages/admin_login.py")

with col2:
    if st.button("User", use_container_width=True):
        st.switch_page("pages/student_login.py")