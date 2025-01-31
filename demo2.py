import streamlit as st
import pandas as pd

# Load data (replace with actual data loading method)
data=pd.read_csv(r"C:\Users\ASUS\Downloads\Unleashed\Unleashed\stud_recommendation_dataset1.csv")


# Get recommendations
st.subheader("Recommended Hackathon Mates:")

# Streamlit UI Config
st.set_page_config(page_title="Hackathon Mates", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #0e0e0e;
            color: #d8d8d8;
        }
        .stTextInput>div>div>input {
            background-color: #000;
            color: white;
            border: 1px solid #a855f7;
            border-radius: 5px;
            padding: 8px;
        }
        .stButton>button {
            background-color: #a855f7;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #9333ea;
        }
        .profile-card {
            background-color: #1a1a1a;
            border: 1px solid #a855f7;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        }
        .avatar {
            width: 60px;
            height: 60px;
            background-color: #333;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            margin: 0 auto 10px;
        }
        .skill-badge {
            background-color: #a855f7;
            color: white;
            border-radius: 15px;
            padding: 5px 10px;
            margin: 5px;
            display: inline-block;
        }
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
        }
        .github-btn, .invite-btn {
            padding: 8px 12px;
            border-radius: 5px;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
        .github-btn {
            background-color: black;
            color: white;
        }
        .invite-btn {
            background-color: #a855f7;
            color: white;
        }
        .invite-btn:hover {
            background-color: #9333ea;
        }
    </style>
""", unsafe_allow_html=True)

# Page Header
st.markdown("# <span style='color: #a855f7;'>HackathonMates</span>", unsafe_allow_html=True)
st.markdown("## <span style='color: white;'>Connect with Teammates</span>", unsafe_allow_html=True)

# Search bar
search_query = st.text_input("Search by skill...", "")

# Filter data based on skill search
if search_query:
    filtered_data = data[data["Skills"].apply(lambda skills: search_query.lower() in [s.lower() for s in skills])]
else:
    filtered_data = data

# Display user profiles in a grid format
cols = st.columns(2)
for index, row in filtered_data.iterrows():
    with cols[index % 2]:
        st.markdown(f"""
            <div class='profile-card'>
                <div class='avatar'>{row['Name'][0]}</div>
                <h3 style='color: #a855f7;'>{row['Name']}</h3>
                <p>{row['Name']}</p>
                <p>{row['Department']}</p>
                <p>{row['Latest Achievement']}</p>
                <div class='action-buttons'>
                    <button class='github-btn'>GitHub</button>
                    <button class='invite-btn'>Invite</button>
                </div>
                <p><strong>Skills:</strong> {' '.join([f"<span class='skill-badge'>{skill}</span>" for skill in row['Skills (Top 5)']])}</p>
            </div>
        """, unsafe_allow_html=True)