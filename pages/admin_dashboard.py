import streamlit as st
import sqlite3

# page = st_navbar(["Make Announcement" ])
# st.write(page)
st.title("🛠️Admin Dashboard")   
st.sidebar.header("Navigation")

if st.button("📢 Manage Announcements"):
    st.switch_page("pages/admin_announcements.py")