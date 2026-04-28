def safe_get(arr, index):
    try:
        return arr[index]
    except:
        return ""

def generate_html(paragraphs):

    paragraphs = [p.strip() for p in paragraphs if p.strip() and "http" not in p.lower()]

    if len(paragraphs) < 3:
        return "<p>Not enough content</p>"

    def find(keyword):
        for i, p in enumerate(paragraphs):
            if keyword.lower() in p.lower():
                return i
        return None

    intro_title = safe_get(paragraphs, 0)
    intro_body = safe_get(paragraphs, 1)

    features_idx = find("Why")
    if features_idx is None:
        features_idx = 2

    moments_idx = find("Events")
    if moments_idx is None:
        moments_idx = min(8, len(paragraphs)-1)

    steps_idx = find("Important")
    if steps_idx is None:
        steps_idx = min(12, len(paragraphs)-1)

    features = []
    for i in range(features_idx+1, min(features_idx+10, len(paragraphs))):
        if len(paragraphs[i]) < 120:
            features.append(paragraphs[i])
        if len(features) == 3:
            break

    steps = paragraphs[steps_idx:steps_idx+8]

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
