def generate_html(content):
    try:
        prompt = f"Convert to full HTML:\n{content}"

        response = client.chat.completions.create(
            model="llama3-70b-8192",  # 🔥 stable Groq model
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
