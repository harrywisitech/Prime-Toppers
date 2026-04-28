def safe_get(arr, index):
    return arr[index] if index >= 0 and index < len(arr) else ""

def generate_html(paragraphs):

    # CLEAN
    paragraphs = [p for p in paragraphs if p.strip() and "http" not in p.lower()]

    # SAFE FIND
    def find(keyword):
        for i, p in enumerate(paragraphs):
            if keyword.lower() in p.lower():
                return i
        return None

    intro_title = safe_get(paragraphs, 0)
    intro_body = safe_get(paragraphs, 1)

    features_idx = find("Why the Rectangle") or 2
    moments_idx = find("Events and Occasions") or 10
    steps_idx = find("Important Details") or 20

    # FEATURES (next 3 headings)
    features = []
    for i in range(features_idx+1, features_idx+7):
        if i < len(paragraphs) and len(paragraphs[i]) < 120:
            features.append(paragraphs[i])
        if len(features) == 3:
            break

    # STEPS
    steps = paragraphs[steps_idx:steps_idx+10]

    # HTML
    html = f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{intro_title}</div>
<div class="prd-intro-body">{intro_body}</div>
</div>

<div class="prd-section-h2">{safe_get(paragraphs, features_idx)}</div>

<div class="prd-three-cols">
"""

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
