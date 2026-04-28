def generate_html(content):
    try:
        prompt = f"""
You are a strict HTML generator.

Convert the following DOC content into FULL structured HTML.

IMPORTANT RULES:
- Generate COMPLETE HTML (no missing sections)
- Do NOT stop early
- Do NOT summarize
- Include ALL content
- Maintain proper structure
- Return ONLY HTML (no explanation)

STRUCTURE MUST INCLUDE:
- prd-intro-box
- prd-section-h2
- prd-three-cols
- prd-snapshot-layout
- prd-moments-section
- prd-steps-list
- CTA

CONTENT:
{content}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=4000  # 🔥 IMPORTANT FIX
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"
