import streamlit as st
import pandas as pd

# Load data (replace with actual data loading method)
data = pd.DataFrame([
    {"Team Name": "Test Team 1", "Hackathon": "test hackathon", "Description": "New test team for test purpose", "Members": 2, "Skills": ["UI/UX", "Figma", "Numpy", "Pandas", "SciPy"]},
    {"Team Name": "Test Team 2", "Hackathon": "test hackathon 2", "Description": "test team 2", "Members": 2, "Skills": ["HTML", "CSS", "JS", "Python", "C", "Java"]},
    {"Team Name": "New Team", "Hackathon": "new hackathon", "Description": "hackathon description", "Members": 1, "Skills": ["Figma", "UI/UX", "Docker", "AWS", "Pandas", "Numpy"]},
    {"Team Name": "New Team 2", "Hackathon": "new hackathon", "Description": "new team 2", "Members": 1, "Skills": ["html", "css", "js", "docker", "azure-aws", "mongodb"]}
])

# Streamlit UI
st.set_page_config(page_title="Hackathon Mates", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0e0e0e;
            color: #d8d8d8;
        }
        .stTextInput>div>div>input {
            background-color: #000;
            color: #fff;
            border: 1px solid #a855f7;
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
        .team-card {
            background-color: #1a1a1a;
            border: 1px solid #a855f7;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        .skill-badge {
            background-color: #a855f7;
            color: white;
            border-radius: 15px;
            padding: 5px 10px;
            margin-right: 5px;
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# <span style='color: #a855f7;'>HackathonMates</span>", unsafe_allow_html=True)
st.markdown("## <span style='color: white;'>Join new Teams</span>", unsafe_allow_html=True)

# Search bar
search_query = st.text_input("Search by skill...", "")

# Filter data based on skill search
if search_query:
    filtered_data = data[data["Skills"].apply(lambda skills: search_query.lower() in [s.lower() for s in skills])]
else:
    filtered_data = data

# Display teams in a grid format
cols = st.columns(2)
for index, row in filtered_data.iterrows():
    with cols[index % 2]:
        st.markdown(f"""
            <div class='team-card'>
                <h3 style='color: #a855f7;'>{row['Team Name']}</h3>
                <p><strong>For the Hackathon:</strong> {row['Hackathon']}</p>
                <p>{row['Description']}</p>
                <p>👥 <strong>Team Members:</strong> {row['Members']}</p>
                <p><strong>Skills:</strong> {' '.join([f"<span class='skill-badge'>{skill}</span>" for skill in row['Skills']])}</p>
            </div>
        """, unsafe_allow_html=True)