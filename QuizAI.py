import json
from openai import OpenAI
import re
import os

# Environment setup
os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '50000'

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def callAIModel(topic):
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

    try:
        data = json.loads(content_cleaned)
        return data['question'], data['options'], data['answer']
    except json.JSONDecodeError:
        raise ValueError("❌ Could not parse JSON from model response.")

def main():
    print("📘 Welcome to the AI Quiz!")
    score = 0
    total = 0

    topic = input("Enter a topic for the quiz: ").strip()

    while True:
        try:
            question, options, correct_index = callAIModel(topic)
        except Exception as e:
            print(f"Error generating question: {e}")
            break

        print(f"\nQuestion: {question}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        answer = input("Enter your answer (1-4): ").strip()
        if answer.isdigit() and 1 <= int(answer) <= 4:
            total += 1
            if int(answer) - 1 == correct_index:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect! The correct answer was: {correct_index + 1}. {options[correct_index]}")
        else:
            print("⚠️ Invalid input. Skipping this question.")

        cont = input("\nDo you want another question? (yes/no): ").strip().lower()
        if cont not in ['yes', 'y']:
            break

    print(f"\n🏁 Quiz ended. Your final score: {score}/{total} ({(score/total*100 if total > 0 else 0):.1f}%)")

if __name__ == "__main__":
    main()
