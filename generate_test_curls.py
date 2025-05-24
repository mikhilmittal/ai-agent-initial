from openai import OpenAI
import subprocess
import re
import os

# Set your OpenAI API key
client = OpenAI(api_key="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")

def generate_test_curls(input_curl):
    prompt = f"""
You are a test automation assistant.
Given this base cURL command:
{input_curl}

Generate 10 variations that test edge cases, missing fields, invalid types, etc.
Return each variation as a full cURL command, one per line.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    content = response.choices[0].message.content
    curl_commands = re.findall(r'curl .*', content)
    return curl_commands

def run_curl_and_get_response(curl_cmd):
    try:
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Request timed out."

def main():
    input_curl = input("Enter a cURL command: ").strip()

    print("Generating test cases using OpenAI...")
    test_curls = generate_test_curls(input_curl)

    print(f"\nGenerated {len(test_curls)} test cases. Executing them...\n")

    if not os.path.exists("responses.txt"):
        open("responses.txt", "w").close()

    with open("responses.txt", "w", encoding="utf-8") as f:
        for idx, curl in enumerate(test_curls, 1):
            f.write(f"Test Case {idx}:\n")
            f.write(f"Command: {curl}\n")
            response = run_curl_and_get_response(curl)
            f.write(f"Response:\n{response}\n")
            f.write("-" * 80 + "\n")
            print(f"Executed Test Case {idx}")

    print("\nAll responses saved to responses.txt")

if __name__ == "__main__":
    main()