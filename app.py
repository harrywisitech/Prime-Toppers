import streamlit as st
import docx
import traceback

# ---------------- UI ----------------
st.set_page_config(page_title="DOC → HTML Converter", layout="wide")
st.title("📄 DOC to HTML Converter")

uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])


# ---------------- READ DOC ----------------
def read_doc(file):
    doc = docx.Document(file)
    content = []

    # paragraphs
    for p in doc.paragraphs:
        if p.text.strip():
            content.append(p.text.strip())

    # tables
    for table in doc.tables:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                if cell.text.strip():
                    row_data.append(cell.text.strip())

            if row_data:
                content.append(" : ".join(row_data))

    return content


# ---------------- SMART HTML GENERATOR ----------------
def generate_html(paragraphs):

    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) < 3:
        return "<p>❌ Not enough content</p>"

    html = ""

    # INTRO
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{paragraphs[0]}</div>
<div class="prd-intro-body">{paragraphs[1] if len(paragraphs) > 1 else ""}</div>
</div>
"""

    i = 2

    while i < len(paragraphs):

        text = paragraphs[i]

        # 🔹 HEADING
        if len(text) < 80:
            html += f'<div class="prd-section-h2">{text}</div>'

            # FEATURES (safe)
            if i + 2 < len(paragraphs):
                html += '<div class="prd-three-cols">'

                count = 0
                j = i + 1

                while j < len(paragraphs) - 1 and count < 3:
                    title = paragraphs[j]
                    body = paragraphs[j + 1]

                    html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{title}</div>
<div class="prd-feat-col-body">{body}</div>
</div>
"""
                    j += 2
                    count += 1

                html += "</div>"
                i = j
                continue

        # 🔹 STEPS
        if text[:2].isdigit():

            html += '<div class="prd-steps-list">'
            step = 1

            while i < len(paragraphs):
                txt = paragraphs[i]

                if not txt[:2].isdigit():
                    break

                title = txt
                body = paragraphs[i+1] if i+1 < len(paragraphs) else ""

                html += f"""
<div class="prd-step-row">
<div class="prd-step-num">{str(step).zfill(2)}</div>
<div class="prd-step-content">
<div class="prd-step-title">{title}</div>
<div class="prd-step-body">{body}</div>
</div>
</div>
"""
                step += 1
                i += 2

            html += "</div>"
            continue

        # 🔹 TABLE
        if ":" in text:
            html += """
<div class="prd-snapshot-card">
<table class="prd-snapshot-table">
<tbody>
"""
            while i < len(paragraphs) and ":" in paragraphs[i]:
                parts = paragraphs[i].split(":", 1)
                key = parts[0]
                val = parts[1] if len(parts) > 1 else ""

                html += f"<tr><td>{key}</td><td>{val}</td></tr>"
                i += 1

            html += "</tbody></table></div>"
            continue

        # 🔹 NORMAL TEXT
        html += f"<p>{text}</p>"

        i += 1

    return html


# ---------------- MAIN ACTION ----------------
if uploaded_file is not None:

    st.success("✅ File uploaded")

    if st.button("Convert to HTML"):

        try:
            paragraphs = read_doc(uploaded_file)

            # DEBUG VIEW (optional)
            with st.expander("🔍 Raw extracted content"):
                st.write(paragraphs)

            html = generate_html(paragraphs)

            st.success("✅ HTML Generated")

            st.code(html, language="html")

            st.download_button(
                "⬇ Download HTML",
                html,
                file_name="output.html",
                mime="text/html"
            )

        except Exception as e:
            st.error("❌ Error occurred")
            st.text(str(e))
            st.text(traceback.format_exc())
