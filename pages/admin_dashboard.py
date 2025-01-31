import streamlit as st
from streamlit_navigation_bar import st_navbar
import sqlite3

# page = st_navbar(["Make Announcement" ])
# st.write(page)
st.title("🛠️Admin Dashboard")   
st.sidebar.header("Navigation")

if st.button("📢 Manage Announcements"):
    st.switch_page("pages/admin_announcements.py")