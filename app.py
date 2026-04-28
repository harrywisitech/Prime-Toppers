import streamlit as st
import docx

st.set_page_config(page_title="DOC → HTML", layout="wide")

st.title("DOC to HTML Converter")

# FILE UPLOAD
uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])


# READ DOC - FIXED: Now reads ALL content including tables
def read_doc(file):
    doc = docx.Document(file)
    texts = []

    WORD_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    def extract_para_text(para_element):
        """Extract full text from a paragraph XML element."""
        parts = []
        for t in para_element.iter(f'{{{WORD_NS}}}t'):
            if t.text:
                parts.append(t.text)
        return ''.join(parts).strip()

    # Iterate body children IN ORDER so paragraphs and table content stay ordered
    for block in doc.element.body:
        tag = block.tag

        # ── Regular paragraph ──────────────────────────────────────────
        if tag == f'{{{WORD_NS}}}p':
            text = extract_para_text(block)
            if text:
                texts.append(text)

        # ── Table  ─────────────────────────────────────────────────────
        # BUG WAS HERE: doc.paragraphs skips table content entirely!
        elif tag == f'{{{WORD_NS}}}tbl':
            for row in block.iter(f'{{{WORD_NS}}}tr'):
                for cell in row.iter(f'{{{WORD_NS}}}tc'):
                    for para in cell.iter(f'{{{WORD_NS}}}p'):
                        text = extract_para_text(para)
                        if text:
                            texts.append(text)

        # ── Text boxes / drawing frames ────────────────────────────────
        elif tag == f'{{{WORD_NS}}}sdt':
            for para in block.iter(f'{{{WORD_NS}}}p'):
                text = extract_para_text(para)
                if text:
                    texts.append(text)

    return texts


# MAIN GENERATOR (FULL DOC → STRUCTURED HTML)
def generate_html(paragraphs):

    paragraphs = [p for p in paragraphs if p.strip()]

    if len(paragraphs) < 5:
        # Even if doc is short, still convert everything
        html = '<div class="prd-full-content">'
        for p in paragraphs:
            if len(p) < 80:
                html += f'<h3>{p}</h3>'
            else:
                html += f'<p>{p}</p>'
        html += '</div>'
        return html

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

    # FEATURES (3 blocks of 2 paragraphs each → indices 3-8)
    html += '<div class="prd-three-cols">'
    for i in range(3, min(9, len(paragraphs)), 2):
        title = paragraphs[i]
        body = paragraphs[i + 1] if i + 1 < len(paragraphs) else ""
        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{title}</div>
<div class="prd-feat-col-body">{body}</div>
</div>
"""
    html += "</div>"

    # REST CONTENT — everything from index 9 onwards (was already correct)
    html += '<div class="prd-full-content">'
    for i in range(9, len(paragraphs)):
        text = paragraphs[i]
        if len(text) < 80:
            html += f'<h3>{text}</h3>'
        else:
            html += f'<p>{text}</p>'
    html += "</div>"

    return html


# ── MAIN APP ────────────────────────────────────────────────────────────────
if uploaded_file is not None:

    st.success("✅ File uploaded successfully")

    if st.button("Convert to HTML"):

        try:
            paragraphs = read_doc(uploaded_file)

            if not paragraphs:
                st.warning("No text content found in the document.")
            else:
                html = generate_html(paragraphs)

                st.success(f"✅ HTML Generated — **{len(paragraphs)} paragraphs** processed")

                # FIXED: use text_area instead of st.code()
                # st.code() silently truncates large HTML in the browser!
                with st.expander("📄 View HTML Output", expanded=True):
                    st.text_area(
                        label="Full HTML (copy from here)",
                        value=html,
                        height=500,
                        key="html_output"
                    )

                st.download_button(
                    label="⬇️ Download HTML File",
                    data=html,
                    file_name="output.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)
