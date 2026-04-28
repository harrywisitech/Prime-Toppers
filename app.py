import streamlit as st
import docx

st.set_page_config(page_title="DOC to HTML Converter", layout="wide")

st.title("🚀 DOC → HTML Converter")

# ✅ FILE UPLOADER (IMPORTANT)
uploaded_file = st.file_uploader("Upload DOCX file", type=["docx"])


# ✅ READ DOC FUNCTION
def read_doc(file):
    doc = docx.Document(file)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


# ✅ SAFE GET
def safe_get(arr, index):
    try:
        return arr[index]
    except:
        return ""


# ✅ MAIN HTML GENERATOR
def generate_html(paragraphs):

    paragraphs = [p.strip() for p in paragraphs if p.strip() and "http" not in p.lower()]

    if not paragraphs or len(paragraphs) < 2:
        return "<p>❌ Not enough content in DOC</p>"

    def find(keyword):
        for i, p in enumerate(paragraphs):
            if keyword.lower() in p.lower():
                return i
        return None

    intro_title = safe_get(paragraphs, 0)
    intro_body = safe_get(paragraphs, 1)

    features_idx = find("why")
    if features_idx is None:
        features_idx = min(2, len(paragraphs)-1)

    moments_idx = find("events")
    if moments_idx is None:
        moments_idx = min(6, len(paragraphs)-1)

    steps_idx = find("important")
    if steps_idx is None:
        steps_idx = min(10, len(paragraphs)-1)

    # FEATURES
    features = []
    for i in range(features_idx+1, len(paragraphs)):
        if len(paragraphs[i]) < 120:
            features.append(paragraphs[i])
        if len(features) == 3:
            break

    if not features:
        features = paragraphs[2:5]

    # STEPS
    steps = paragraphs[steps_idx:steps_idx+8]

    # BUILD HTML
    html = ""

    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{intro_title}</div>
<div class="prd-intro-body">{intro_body}</div>
</div>
"""

    html += f"""
<div class="prd-section-h2">{safe_get(paragraphs, features_idx)}</div>
"""

    html += '<div class="prd-three-cols">'
    for f in features:
        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{f}</div>
</div>
"""
    html += "</div>"

    html += f"""
<div class="prd-moments-section">
<div class="prd-section-h2">{safe_get(paragraphs, moments_idx)}</div>
</div>
"""

    html += '<div class="prd-steps-list">'
    for i, s in enumerate(steps, 1):
        html += f"""
<div class="prd-step-row">
<div class="prd-step-num">{str(i).zfill(2)}</div>
<div class="prd-step-body">{s}</div>
</div>
"""
    html += "</div>"

    return html


# ✅ BUTTON LOGIC (FINAL FIX)
if uploaded_file is not None:

    st.success("File uploaded ✅")

    if st.button("🔥 Convert to HTML"):

        try:
            paragraphs = read_doc(uploaded_file)
            html = generate_html(paragraphs)

            st.success("✅ HTML Generated")

            st.code(html, language="html")

            st.download_button(
                label="⬇ Download HTML",
                data=html,
                file_name="output.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
