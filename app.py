import streamlit as st
import docx
import os
from openai import OpenAI

# GROQ CLIENT
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="DOC to HTML Tool", layout="wide")

st.title("🚀 DOC → HTML Auto Converter (Groq Powered)")

uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])

def read_doc(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def generate_html(content):
    try:
        prompt = f"""
Convert the following content into structured HTML using EXACT format:

- prd-intro-box
- prd-three-cols
- prd-snapshot-layout
- prd-moments-section
- prd-steps-list
- CTA

STRICT RULES:
- No summarization
- No missing content
- Keep exact wording

CONTENT:
{content}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


if uploaded_file:
    if st.button("🔥 Convert to HTML"):
        text = read_doc(uploaded_file)
        html = generate_html(text)

        st.success("✅ HTML Generated")

        st.text_area("Output HTML", html, height=400)

        st.download_button(
            label="⬇ Download HTML",
            data=html,
            file_name="output.html",
            mime="text/html"
        )
