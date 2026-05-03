import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Text Summarizer", layout="wide")

st.title("Text Summarizer")

if "text" not in st.session_state:
    st.session_state.text = ""

length_option = st.selectbox(
    "Summary Length",
    ["Short", "Medium", "Detailed"]
)

format_option = st.selectbox(
    "Format",
    ["Paragraph", "Bullet Points"]
)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text()

    st.session_state.text = extracted_text

text_input = st.text_area("Enter text", value=st.session_state.text, height=300)

def build_prompt(text, length, fmt):
    length_map = {
        "Short": "in 3-4 lines",
        "Medium": "in 6-8 lines",
        "Detailed": "in detail covering all key points"
    }

    format_map = {
        "Paragraph": "in paragraph form",
        "Bullet Points": "in bullet points"
    }

    prompt = f"Summarize the following text {length_map[length]} {format_map[fmt]}:\n\n{text}"
    return prompt

if st.button("Summarize"):
    if text_input.strip() == "":
        st.warning("Please enter text or upload a PDF")
    else:
        prompt = build_prompt(text_input, length_option, format_option)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        summary = response.choices[0].message.content

        st.subheader("Summary")
        st.write(summary)