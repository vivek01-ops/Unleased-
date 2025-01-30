import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import emailfetch  # Import the email fetching script

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=gemini_api_key)

def email_summarizer(email_data):
    # Dictionary to store summarized emails
    outputs = {}

    for email in email_data:
        subject = email["subject"]
        body = email["body"]
        
        # Define prompt for summarization
        prompt = f"Summarize the following email:\n\nSubject: {subject}\n\nBody: {body}\n\nSummary:"
        
        try:
            model = genai.GenerativeModel("gemini-pro")  # Load the Gemini model
            response = model.generate_content(prompt)
            output = response.text
        except Exception as e:
            output = f"Error generating summary: {e}"
        
        outputs[f"{email['from']} - {subject}"] = output

    # Display results in Streamlit
    with st.expander("Email Summaries", expanded=True):
        for key, output in outputs.items():
            st.subheader(f"Email from: {key}")
            st.write(output, end="\n\n")

def main():
    st.title("AI Email Summarization Tool")
    st.header("Powered by Gemini AI, Streamlit")

    deploy_tab, code_tab = st.tabs(["Deployment", "Code"])

    with deploy_tab:
        # Fetch emails
        emails = emailfetch.fetch_emails()  # Assuming fetch_emails() returns a list of emails

        if emails:
            email_summarizer(emails)
        else:
            st.write("No emails found to summarize.")
    
    with code_tab:
        st.header("Source Code")
        st.code(open(__file__).read())  # Display the script itself

if __name__ == "__main__":
    main()
