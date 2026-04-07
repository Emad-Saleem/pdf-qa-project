import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def extract_pdf_text(pdf_path):
    """Extracts text with Page and Line numbers for citations."""
    try:
        doc = fitz.open(pdf_path)
        content = []
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            line_num = 1
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        text = "".join([s["text"] for s in l["spans"]]).strip()
                        if text:
                            content.append(f"[Pg {page_num}, Ln {line_num}]: {text}")
                            line_num += 1
        return "\n".join(content)
    except Exception as e:
        return f"Error reading PDF: {e}"

def ask_gemini(question, context):
    """Sends the context and question to Gemini 3 Flash."""
    prompt = f"""
    Answer the question based ONLY on the text below. 
    You MUST cite the Page and Line numbers (e.g., [Pg 1, Ln 5]) for every fact you state.
    
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    """
    # Using the latest Gemini 3 Flash for speed
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    return response.text

# --- MAIN LOOP ---
if __name__ == "__main__":
    file_path = "data/document.pdf"
    
    if os.path.exists(file_path):
        print("--- 📄 Reading your PDF... ---")
        pdf_context = extract_pdf_text(file_path)
        print("--- ✅ System Ready! Type 'exit' to quit. ---")
        
        while True:
            query = input("\nWhat would you like to know? ")
            if query.lower() in ['exit', 'quit']:
                break
                
            print("Gemini is searching the document...")
            try:
                answer = ask_gemini(query, pdf_context)
                print(f"\nAI ANSWER:\n{answer}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print(f"Error: Could not find 'data/document.pdf'. Please add it!")