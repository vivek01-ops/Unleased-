import streamlit as st
import pandas as pd
import yaml 
import emailfetch
import emailanalyzer
# Load the dataset
data = {
    "event_name": [
        "InnovateX Hackathon", 
        "TechFest 2025", 
        "Cultural Fiesta", 
        "Future Tech Summit", 
        "Vibrance 2025"
    ],
    "registration_date_from": [
        "2025-02-01", 
        "2025-03-10", 
        "2025-04-05", 
        "2025-06-01", 
        "2025-08-15"
    ],
    "registration_date_to": [
        "2025-02-07", 
        "2025-03-17", 
        "2025-04-12", 
        "2025-06-07", 
        "2025-08-20"
    ],
    "type": [
        "hackathon", 
        "tech event", 
        "cultural event", 
        "tech event", 
        "non-tech event"
    ],
    "fees_of_registration": [
        500, 
        1000, 
        300, 
        1500, 
        400
    ],
    "venue": [
        "Vishwakarma Institute of Technology, Pune", 
        "IIT Bombay Campus", 
        "Shivaji Park, Mumbai", 
        "Bangalore International Exhibition Centre", 
        "Juhu Beach, Mumbai"
    ],
    "time": [
        "10:00 AM - 5:00 PM", 
        "9:00 AM - 6:00 PM", 
        "6:00 PM - 10:00 PM", 
        "10:00 AM - 4:00 PM", 
        "9:00 AM - 2:00 PM"
    ],
    "prize": [
        "₹50,000", 
        "₹2,00,000", 
        "₹20,000", 
        "₹1,00,000", 
        "₹30,000"
    ]
}

df = pd.DataFrame(data)

# Streamlit Layout


st.set_page_config(page_title="Event Dashboard", layout="wide", initial_sidebar_state="collapsed")
st.title("🖥️ Event Dashboard")

# Add custom CSS for styling
st.markdown("""
    <style>
        .event-card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid gray;
        }
        .event-card h4 {
            color: #1f75fe;
        }
        .stMetric {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid gray;
            color: #1f75fe;
        }
    </style>
""", unsafe_allow_html=True)

# Section: Events for You
st.header("📌 Events for You - Know what clubs that you're interested in are coming up!")

# User Credentials Input
st.subheader("🔑 Provide Your Gmail Credentials to Fetch Registered and Ongoing Events")
username = st.text_input("Enter your Gmail ID", placeholder="your-email@gmail.com")
app_password = st.text_input("Enter your App Password", type="password")
accept = st.checkbox("I accept that I am sharing my app password and giving IMAP access.")

if st.button("Save Credentials"):
    if username and app_password and accept:
        credentials = {"username": username, "app_password": app_password}
        with open("credentials.yaml", "w") as file:
            yaml.dump(credentials, file,default_flow_style=False)
        st.success("✅ Credentials saved successfully!")
        emails = emailfetch.fetch_emails()
        if emails:
            emailanalyzer.email_summarizer(emails)
        else:
            st.write("No emails found to summarize.")
    else:
        st.error("⚠️ Please fill in all fields and accept the terms.")



# Filters for Venue and Event Type
st.header("Filter Events")
coli, colii = st.columns(2)
with coli:
    venues = df['venue'].unique()
    selected_venues = st.multiselect("Select Venue(s)", venues, default=[])
with colii:
    event_types = df['type'].unique()
    selected_types = st.multiselect("Select Event Type(s)", event_types, default=[])

# Logic to display filtered events
filtered_df = df
if selected_venues:
    filtered_df = filtered_df[filtered_df['venue'].isin(selected_venues)]
if selected_types:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]

st.metric(label="Total Events", value=str(len(filtered_df)))

# Function to display event card
def display_event_card(row):
    with st.container():
        st.markdown(f"""
            <div class="event-card">
                <h4>{row['event_name']}</h4>
                <p><strong>Venue:</strong> {row['venue']}</p>
                <p><strong>Prize:</strong> {row['prize']}</p>
                <details>
                    <summary><strong>Read More</strong></summary>
                    <p><strong>Event Type:</strong> {row['type']}</p>
                    <p><strong>Registration Dates:</strong> {row['registration_date_from']} to {row['registration_date_to']}</p>
                    <p><strong>Event Time:</strong> {row['time']}</p>
                    <p><strong>Registration Fees:</strong> ₹{row['fees_of_registration']}</p>
                </details>
            </div>
        """, unsafe_allow_html=True)

# Display events in a grid layout
num_columns = 3  # Number of event cards per row
cols = st.columns(num_columns)
for i, row in filtered_df.iterrows():
    col_index = i % num_columns
    with cols[col_index]:
        display_event_card(row)
