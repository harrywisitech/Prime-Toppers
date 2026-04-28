import streamlit as st
import docx

st.set_page_config(page_title="DOC to HTML Tool", layout="wide")

st.title("🚀 DOC → HTML Auto Converter (Perfect Version)")

uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])


# 📄 DOC READ
def read_doc(file):
    doc = docx.Document(file)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


# 🔥 FIXED TEMPLATE ENGINE (NO AI BREAK)
def generate_html(paragraphs):
    
    html = f"""
<!-- INTRO -->
<div class="prd-intro-box">
<div class="prd-intro-title">{paragraphs[0] if len(paragraphs)>0 else ''}</div>
<div class="prd-intro-body">{paragraphs[1] if len(paragraphs)>1 else ''}</div>
</div>

<div class="prd-section-h2">{paragraphs[2] if len(paragraphs)>2 else ''}</div>

<!-- FEATURES -->
<div class="prd-three-cols">
"""

    # 3 columns auto fill
    for i in range(3, 6):
        if i < len(paragraphs):
            html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{paragraphs[i]}</div>
</div>
"""

    html += "</div>"

    # SNAPSHOT
    html += """
<div class="prd-snapshot-layout">
<div class="prd-snapshot-text">
"""

    for i in range(6, min(len(paragraphs), 15)):
        html += f"<p>{paragraphs[i]}</p>"

    html += "</div></div>"

    # MOMENTS (dummy safe)
    html += """
<div class="prd-moments-section">
<div class="prd-section-h2">Events & Occasions</div>
</div>
"""

    # STEPS
    html += '<div class="prd-steps-list">'

    step_num = 1
    for i in range(15, len(paragraphs)):
        html += f"""
<div class="prd-step-row">
<div class="prd-step-num">{str(step_num).zfill(2)}</div>
<div class="prd-step-content">
<div class="prd-step-body">{paragraphs[i]}</div>
</div>
</div>
"""
        step_num += 1

    html += "</div>"

    # CTA
    html += """
<div class="prd-intro-box">
<div class="prd-intro-title">Customize Now</div>
<div class="prd-intro-body">Click Customize Now to start your order</div>
</div>
"""

    return html


# 🚀 RUN
if uploaded_file:
    if st.button("🔥 Convert to HTML"):
        paragraphs = read_doc(uploaded_file)
        html = generate_html(paragraphs)

        st.success("✅ Perfect HTML Generated")

        st.code(html, language="html")

        st.download_button(
            label="⬇ Download HTML",
            data=html,
            file_name="output.html",
            mime="text/html"
        )
