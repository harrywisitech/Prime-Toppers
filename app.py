def generate_html(paragraphs):

    # CLEAN
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) < 10:
        return "<p>Not enough structured content</p>"

    # SAFE GET
    def g(i):
        return paragraphs[i] if i < len(paragraphs) else ""

    # ---------------- INTRO ----------------
    html = f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{g(0)}</div>
<div class="prd-intro-body">{g(1)}</div>
</div>
"""

    # ---------------- MAIN HEADING ----------------
    html += f"""
<div class="prd-section-h2">{g(2)}</div>
"""

    # ---------------- FEATURES ----------------
    html += '<div class="prd-three-cols">'

    for i in range(3, 9, 2):
        html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{g(i)}</div>
<div class="prd-feat-col-body">{g(i+1)}</div>
</div>
"""

    html += "</div>"

    # ---------------- SNAPSHOT ----------------
    html += """
<div class="prd-snapshot-layout">
<div class="prd-snapshot-text">
"""

    for i in range(9, 15):
        html += f"<p>{g(i)}</p>"

    html += """
</div>

<div>
<div class="prd-snapshot-card">
<div class="prd-snapshot-header">Product Snapshot</div>
<table class="prd-snapshot-table">
<tbody>
"""

    # TABLE AUTO BUILD
    for i in range(15, 25):
        if ":" in g(i):
            key, val = g(i).split(":", 1)
            html += f"<tr><td>{key}</td><td>{val}</td></tr>"

    html += """
</tbody>
</table>
</div>
</div>
</div>
"""

    # ---------------- MOMENTS ----------------
    html += """
<div class="prd-moments-section">
<div class="prd-section-h2">Every Occasion Where This Cookie Makes Its Mark</div>
<div class="prd-moments-grid">
"""

    moments = ["Corporate Events","Weddings","Birthdays","Product Launches","Branded Gifting","Baby Showers"]

    for m in moments:
        html += f"""
<div class="prd-moment-item">
<span class="prd-moment-icon">📌</span>
<div class="prd-moment-label">{m}</div>
</div>
"""

    html += "</div></div>"

    # ---------------- INGREDIENTS ----------------
    html += f"""
<div class="prd-moments-section">
<div class="prd-section-h2">{g(25)}</div>
<p>{g(26)}</p>

<div class="prd-steps-list">
"""

    step = 1
    for i in range(27, 35, 2):
        html += f"""
<div class="prd-step-row">
<div class="prd-step-num">{str(step).zfill(2)}</div>
<div class="prd-step-content">
<div class="prd-step-title">{g(i)}</div>
<div class="prd-step-body">{g(i+1)}</div>
</div>
</div>
"""
        step += 1

    html += "</div></div>"

    # ---------------- ORDER INFO ----------------
    html += f"""
<div class="prd-moments-section">
<div class="prd-section-h2">{g(35)}</div>
<p>{g(36)}</p>

<div class="prd-steps-list">
"""

    step = 1
    for i in range(37, len(paragraphs), 2):
        html += f"""
<div class="prd-step-row">
<div class="prd-step-num">{str(step).zfill(2)}</div>
<div class="prd-step-content">
<div class="prd-step-title">{g(i)}</div>
<div class="prd-step-body">{g(i+1)}</div>
</div>
</div>
"""
        step += 1

    html += "</div></div>"

    # ---------------- CTA ----------------
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{g(-3)}</div>
<div class="prd-intro-body">{g(-2)}</div>
<div class="prd-intro-body" style="padding-top:15px;color:#d63f70;font-weight:bold;">
{g(-1)}
</div>
</div>
"""

    return html
