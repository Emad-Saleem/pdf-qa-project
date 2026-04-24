# PDF Research Assistant 📄

A Python-based web application that allows users to upload PDF documents and ask questions about their content using **Gemini 2.5 Flash**.

## Features
- **PDF Text Extraction:** Uses PyMuPDF (fitz) to read document text.
- **AI-Powered Answers:** Uses Google Gemini API to process queries.
- **Interactive UI:** Built with Streamlit for a clean browser experience.

## How to Run
1. Clone this repository. # test
2. Create a `.env` file and add your `GOOGLE_API_KEY` from gemini.
3. Create a virtual environment: `python -m venv venv`.
4. Install requirements: `pip install -r requirements.txt`.
5. Run the app: `streamlit run app.py`.