def generate_html(paragraphs):

    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) < 5:
        return "<p>Not enough content</p>"

    html = ""

    # 🔹 INTRO
    html += f"""
<div class="prd-intro-box">
<div class="prd-intro-title">{paragraphs[0]}</div>
<div class="prd-intro-body">{paragraphs[1]}</div>
</div>
"""

    i = 2

    # 🔹 SECTION DETECTION LOOP
    while i < len(paragraphs):

        text = paragraphs[i]

        # 🟣 HEADING DETECTION
        if len(text) < 80:
            html += f'<div class="prd-section-h2">{text}</div>'

            # 🔹 FEATURES BLOCK (next 3 pairs)
            if i + 6 < len(paragraphs):
                html += '<div class="prd-three-cols">'

                for j in range(1, 7, 2):
                    title = paragraphs[i + j]
                    body = paragraphs[i + j + 1]

                    html += f"""
<div class="prd-feat-col">
<div class="prd-feat-col-title">{title}</div>
<div class="prd-feat-col-body">{body}</div>
</div>
"""

                html += "</div>"
                i += 7
                continue

        # 🟢 STEP DETECTION (01, 02, etc.)
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

        # 🟡 TABLE DETECTION
        if ":" in text:
            html += """
<div class="prd-snapshot-card">
<table class="prd-snapshot-table">
<tbody>
"""
            while i < len(paragraphs) and ":" in paragraphs[i]:
                key, val = paragraphs[i].split(":", 1)
                html += f"<tr><td>{key}</td><td>{val}</td></tr>"
                i += 1

            html += "</tbody></table></div>"
            continue

        # 🔵 NORMAL PARAGRAPH
        html += f"<p>{text}</p>"

        i += 1

    return html

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
