import streamlit as st
import sqlite3
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define preprocess function
def preprocess(text):
    if pd.isna(text): 
        return ""
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(text.lower())
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    
    return " ".join(filtered_tokens)


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


def load_data():
    df = pd.read_csv(r"C:\Users\ASUS\Downloads\Unleashed\Unleashed\stud_recommendation_dataset1.csv")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()



    df['Interests'] = df['Interests'].apply(preprocess)
    df['Skills (Top 5)'] = df['Skills (Top 5)'].apply(preprocess)
    df['Latest Achievement'] = df['Latest Achievement'].apply(preprocess)
    df = df[df['Availability'] == 'Yes']

    df['combined'] = df['Skills (Top 5)'] + ' ' + df['Interests'] + ' ' + df['Latest Achievement']
    return df

def recommend_users(user_index, df, top_n=10):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    dissimilarity_matrix = 1 - cosine_sim

    dissimilarity_scores = dissimilarity_matrix[user_index]
    recommended_indices = np.argsort(dissimilarity_scores)[::-1]
    recommended_indices = [idx for idx in recommended_indices if idx != user_index]
    return df.iloc[recommended_indices[:top_n]]

st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.title("Student Authentication")

create_database()
choice = st.radio("Select an option:", ["Login", "Register"], horizontal=True)

df = load_data()
# Inject CSS at the start of the script
st.markdown("""
    <style>
        .profile-card {
            background-color: #1a1a1a;
            border: 1px solid #a855f7;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            text-align: center;
            width: 300px;
            display: inline-block;
        }
        .profile-card h3 {
            color: #a855f7;
            margin-bottom: 5px;
        }
        .profile-card p {
            margin: 5px 0;
        }
        .skill-badge {
            background-color: #a855f7;
            color: white;
            border-radius: 15px;
            padding: 5px 10px;
            margin: 3px;
            display: inline-block;
        }
        .github-btn, .invite-btn {
            background-color: #a855f7;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 12px;
            margin-top: 10px;
            display: inline-block;
            text-decoration: none;
            font-weight: bold;
        }
        .github-btn:hover, .invite-btn:hover {
            background-color: #9333ea;
        }
    </style>
""", unsafe_allow_html=True)



if choice == "Login":   
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", use_container_width=True):
        user = login_user(login_username, login_password)
        if user:
            st.success(f"Welcome, {user[1]}!")
            st.subheader("Recommended Hackathon Mates:")
            
            # Extract user details
            user_data = {
                "Name": user[1],
                "Skills (Top 5)": user[10],
                "Interests": user[9],
                "Latest Achievement": user[11] if len(user) > 11 else "",  # Check if the field exists
                "Availability": "Yes"  # Assuming they are available for hackathons
            }
            
            # Convert to DataFrame and preprocess
            user_df = pd.DataFrame([user_data])
            user_df["Interests"] = user_df["Interests"].apply(preprocess)
            user_df["Skills (Top 5)"] = user_df["Skills (Top 5)"].apply(preprocess)
            user_df["Latest Achievement"] = user_df["Latest Achievement"].apply(preprocess)
            user_df["combined"] = user_df["Skills (Top 5)"] + ' ' + user_df["Interests"] + ' ' + user_df["Latest Achievement"]
            
            # Append to main dataset
            df = pd.concat([df, user_df], ignore_index=True)
            user_index = df.index[-1]  # The last entry is the logged-in user

            # Get recommendations
            st.subheader("Recommended Hackathon Mates:")
            recommendations = recommend_users(user_index, df, top_n=5)
            
            
            # Create columns for responsive layout
            cols = st.columns(2)  # Adjust number of columns based on layout

            for idx, rec in recommendations.iterrows():
                with cols[idx % 2]:  # Arrange in two columns
                    st.markdown(f"""
                        <div class='profile-card'>
                            <h3>{rec['Name']}</h3>
                            <p><strong>Latest Achievement:</strong> {rec['Latest Achievement']}</p>
                            <p><strong>Skills:</strong></p>
                            <p>{" ".join([f"<span class='skill-badge'>{skill}</span>" for skill in rec['Skills (Top 5)'].split(", ")])}</p>
                            <a href="#" class="github-btn">GitHub</a>
                            <a href="#" class="invite-btn">Invite</a>
                        </div>
                    """, unsafe_allow_html=True)


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
