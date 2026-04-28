import streamlit as st
import docx

st.set_page_config(page_title="DOC → HTML", layout="wide")

st.title("DOC to HTML Converter")

# FILE UPLOAD
uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])


# READ DOC
def read_doc(file):
    doc = docx.Document(file)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


# MAIN GENERATOR (FULL DOC → STRUCTURED HTML)
def generate_html(paragraphs):

    paragraphs = [p for p in paragraphs if p.strip()]

    if len(paragraphs) < 5:
        return "<p>Not enough content</p>"

    html = ""

    # INTRO
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{paragraphs[0]}</div>
<div class="prd-intro-body">{paragraphs[1]}</div>
</div>
"""

    # MAIN HEADING
    html += f'<div class="prd-section-h2">{paragraphs[2]}</div>'

    # FEATURES (3 blocks)
    html += '<div class="prd-three-cols">'
    for i in range(3, min(9, len(paragraphs)), 2):
        title = paragraphs[i]
        body = paragraphs[i+1] if i+1 < len(paragraphs) else ""

        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{title}</div>
<div class="prd-feat-col-body">{body}</div>
</div>
"""
    html += "</div>"

    # REST CONTENT (FULL DOC)
    html += '<div class="prd-full-content">'
    for i in range(9, len(paragraphs)):
        text = paragraphs[i]

        if len(text) < 80:
            html += f'<h3>{text}</h3>'
        else:
            html += f'<p>{text}</p>'

    html += "</div>"

    return html


# BUTTON ACTION (MOST IMPORTANT PART)
if uploaded_file is not None:

    st.success("File uploaded")

    if st.button("Convert to HTML"):

        try:
            paragraphs = read_doc(uploaded_file)
            html = generate_html(paragraphs)

            st.success("HTML Generated")

            st.code(html, language="html")

            st.download_button(
                "Download HTML",
                html,
                "output.html"
            )

        except Exception as e:
            st.error(f"Error: {e}")
