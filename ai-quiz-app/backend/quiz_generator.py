import json
import re
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_API_KEY"
)

def generate_question(topic):
    prompt = f"""
Generate a multiple-choice question on topic '{topic}' with exactly 4 options.
Include the correct option number (0-based index). Format it as JSON like:
{{
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "answer": 2
}}
"""
    completion = client.chat.completions.create(
        model="mistralai/devstral-small:free",
        messages=[{"role": "user", "content": prompt}]
    )
    content = completion.choices[0].message.content
    content_cleaned = re.sub(r"^```json|^```|```$", "", content, flags=re.MULTILINE).strip()
    return json.loads(content_cleaned)
