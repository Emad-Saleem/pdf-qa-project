import streamlit as st
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai

# --- 1. Page Configuration ---
st.set_page_config(page_title="PDF Chat AI", page_icon="📄")
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- 2. Initialize Persistent Session States ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize a temporary user database in session memory if it doesn't exist
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "admin": "password123",
        "student": "jee2026"
    }

# --- 3. Logic Functions --
def extract_pdf_text(uploaded_file):
    """Processes the PDF file object directly from the web uploader."""
    l = []
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page_num, page in enumerate(doc, start=1):
        y = []
        page_text = page.get_text("text")
        texts = page_text.split("\n")
        for tno, text in enumerate(texts, start=1):
            text = text.strip()
            if text:
                y.append({tno: text})
        l.append({page_num: y})
    return l

# --- 4. Authentication System UI ---
def auth_page():
    st.title("🔒 PDF AI Assistant Portal")
    
    # Toggle between Login and Sign Up modes
    mode = st.radio("Select an option:", ["Log In", "Sign Up"], horizontal=True)
    
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password")
    
    if mode == "Log In":
        if st.button("Log In"):
            if username in st.session_state.user_db and st.session_state.user_db[username] == password:
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                
    elif mode == "Sign Up":
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if not username or not password:
                st.error("Username and password cannot be empty.")
            elif username in st.session_state.user_db:
                st.error("Username already exists! Choose another one.")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            else:
                # 1. Save the new credentials
                st.session_state.user_db[username] = password
                
                # 2. Instantly log them in!
                st.session_state.logged_in = True
                st.success("Account created! Logging you in...")
                st.rerun()  # Instantly skips to the PDF page

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- 5. Application Routing ---
if not st.session_state.logged_in:
    auth_page()
else:
    # --- Sidebar with Logout Button ---
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in!")
    if st.sidebar.button("Log Out"):
        logout()

    # --- Main Application UI ---
    st.title("📄 PDF AI Assistant")
    st.markdown("Upload a document and ask Gemini questions about it.")

    # File Uploader Widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if "pdf_context" not in st.session_state:
            with st.spinner("Extracting text..."):
                st.session_state.pdf_context = extract_pdf_text(uploaded_file)
                st.success("PDF ready!")

        # Question Input
        user_question = st.text_input("Ask a question about your PDF:")

        if user_question:
            with st.spinner("Gemini is thinking..."):
                prompt = f"Use this context to answer while also providing page and line numbers: {st.session_state.pdf_context}\n\nQuestion: {user_question}"
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt
                    )
                    st.info("### Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")