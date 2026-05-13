import streamlit as st
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai

# --- 1. Page Configuration --- test
st.set_page_config(page_title="PDF Chat AI", page_icon="📄")
load_dotenv() # hello again
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
#hello
# --- 2. Logic Functions ---
def extract_pdf_text(uploaded_file):
    """Processes the PDF file object directly from the web uploader."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    content = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text:
            content.append(f"[Page {page_num}]: {text}")
    return "\n".join(content)

# --- 3. Streamlit UI ---
st.title("📄 PDF AI Assistant")
st.markdown("Upload a document and ask Gemini questions about it.")

# File Uploader Widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the text in 'session_state' so it stays loaded while you chat
    if "pdf_context" not in st.session_state:
        with st.spinner("Extracting text..."):
            st.session_state.pdf_context = extract_pdf_text(uploaded_file)
            st.success("PDF ready!")

    # Question Input
    user_question = st.text_input("Ask a question about your PDF:")

    if user_question:
        with st.spinner("Gemini is thinking..."):
            prompt = f"Use this context to answer: {st.session_state.pdf_context}\n\nQuestion: {user_question}"
            try:
                # Using 2.5-flash for the best stability in 2026
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt
                )
                st.info("### Answer:")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")