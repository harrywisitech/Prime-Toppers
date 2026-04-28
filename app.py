def generate_html(paragraphs):

    # CLEAN unwanted lines
    clean = []
    for p in paragraphs:
        if "http" in p.lower():
            continue
        if "primetoppers.com" in p.lower():
            continue
        clean.append(p)

    paragraphs = clean

    # 🔥 DETECT SECTIONS
    intro_title = paragraphs[0]
    intro_body = paragraphs[1]

    # find sections by keywords
    def find_index(keyword):
        for i, p in enumerate(paragraphs):
            if keyword.lower() in p.lower():
                return i
        return -1

    features_start = find_index("Why the Rectangle")
    snapshot_start = find_index("Twenty-Four Fresh")
    moments_start = find_index("Events and Occasions")
    ingredients_start = find_index("What Goes into")
    steps_start = find_index("Important Details")
    cta_start = find_index("Your Brand")

    # FEATURES (next 3 blocks)
    features = paragraphs[features_start+1:features_start+4]

    # SNAPSHOT
    snapshot = paragraphs[snapshot_start: moments_start]

    # STEPS
    steps = paragraphs[steps_start+1:cta_start]

    # CTA
    cta = paragraphs[cta_start:]

    # HTML BUILD
    html = f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{intro_title}</div>
<div class="prd-intro-body">{intro_body}</div>
</div>

<div class="prd-section-h2">{paragraphs[features_start]}</div>

<div class="prd-three-cols">
"""

    for f in features:
        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{f}</div>
</div>
"""

    html += "</div>"

    # SNAPSHOT
    html += '<div class="prd-snapshot-layout"><div class="prd-snapshot-text">'
    for s in snapshot:
        html += f"<p>{s}</p>"
    html += "</div></div>"

    # MOMENTS
    html += f"""
<div class="prd-moments-section">
<div class="prd-section-h2">{paragraphs[moments_start]}</div>
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

    # CTA
    html += '<div class="prd-intro-box">'
    for c in cta:
        html += f"<p>{c}</p>"
    html += "</div>"

    return html
