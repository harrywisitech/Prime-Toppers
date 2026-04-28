def read_doc(file):
    doc = docx.Document(file)

    content = []

    # 🔹 PARAGRAPHS
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            content.append(text)

    # 🔹 TABLES (IMPORTANT FIX)
    for table in doc.tables:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                txt = cell.text.strip()
                if txt:
                    row_data.append(txt)

            if row_data:
                content.append(" : ".join(row_data))

    return content
