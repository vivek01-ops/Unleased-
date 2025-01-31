import streamlit as st
import sqlite3  # Or use Django ORM for database

st.title("📢 Announcements Page")

conn = sqlite3.connect("announcements.db")
c = conn.cursor()

# Create announcements table (if not exists)
c.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Form to add new announcement
st.subheader("📝 Add a New Announcement")
with st.form("announcement_form"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    submit = st.form_submit_button("Post Announcement")

    if submit and title and content:
        c.execute("INSERT INTO announcements (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        st.success("✅ Announcement Posted!")

# Display announcements
st.subheader("📢 Recent Announcements")
c.execute("SELECT title, content, date FROM announcements ORDER BY date DESC")
announcements = c.fetchall()

if announcements:
    for title, content, date in announcements:
        with st.expander(f"📌 {title} ({date})"):
            st.write(content)
else:
    st.info("No announcements yet.")

conn.close()
