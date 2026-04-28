def generate_html(paragraphs):

    # CLEAN DATA
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return "<p>No content found</p>"

    html = ""

    # INTRO (first 2 lines)
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{paragraphs[0]}</div>
<div class="prd-intro-body">{paragraphs[1] if len(paragraphs) > 1 else ""}</div>
</div>
"""

    # REST CONTENT LOOP (FULL DOC)
    html += '<div class="prd-full-content">'

    for i in range(2, len(paragraphs)):

        text = paragraphs[i]

        # 🔹 Detect heading
        if len(text) < 80:
            html += f'<div class="prd-section-h2">{text}</div>'

        # 🔹 Detect normal paragraph
        else:
            html += f'<p>{text}</p>'

    html += '</div>'

    return html
