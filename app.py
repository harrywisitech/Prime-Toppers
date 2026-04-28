def safe_get(arr, index):
    try:
        return arr[index]
    except:
        return ""

def generate_html(paragraphs):

    # 🔹 CLEAN DATA (remove empty + urls)
    paragraphs = [p.strip() for p in paragraphs if p.strip() and "http" not in p.lower()]

    # 🔹 SAFETY CHECK
    if not paragraphs or len(paragraphs) < 2:
        return "<p>❌ Not enough content in DOC</p>"

    # 🔹 SAFE FIND FUNCTION
    def find(keyword):
        for i, p in enumerate(paragraphs):
            if keyword.lower() in p.lower():
                return i
        return None

    # 🔹 BASIC CONTENT
    intro_title = safe_get(paragraphs, 0)
    intro_body = safe_get(paragraphs, 1)

    # 🔹 SAFE INDEX HANDLING (NO OR BUG)
    features_idx = find("why")
    if features_idx is None:
        features_idx = min(2, len(paragraphs)-1)

    moments_idx = find("events")
    if moments_idx is None:
        moments_idx = min(6, len(paragraphs)-1)

    steps_idx = find("important")
    if steps_idx is None:
        steps_idx = min(10, len(paragraphs)-1)

    # 🔹 FEATURES (3 SAFE ITEMS)
    features = []
    for i in range(features_idx+1, len(paragraphs)):
        if i >= len(paragraphs):
            break

        text = paragraphs[i]

        if len(text) < 120:
            features.append(text)

        if len(features) == 3:
            break

    # fallback if empty
    if not features:
        features = paragraphs[2:5]

    # 🔹 STEPS (SAFE SLICE)
    steps = []
    for i in range(steps_idx, min(steps_idx+8, len(paragraphs))):
        steps.append(paragraphs[i])

    # 🔹 BUILD HTML SAFELY
    html = ""

    # INTRO
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{intro_title}</div>
<div class="prd-intro-body">{intro_body}</div>
</div>
"""

    # HEADING
    html += f"""
<div class="prd-section-h2">{safe_get(paragraphs, features_idx)}</div>
"""

    # FEATURES
    html += '<div class="prd-three-cols">'
    for f in features:
        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{f}</div>
</div>
"""
    html += "</div>"

    # MOMENTS
    html += f"""
<div class="prd-moments-section">
<div class="prd-section-h2">{safe_get(paragraphs, moments_idx)}</div>
</div>
"""

    # STEPS
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
