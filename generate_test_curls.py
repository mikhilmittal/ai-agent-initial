import subprocess
import re
import os
import requests
from huggingface_hub import InferenceClient
import os

os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '50000'  # 5 seconds

# Then start your debugger (e.g., PyCharm/VS Code debug session)

HF_API_TOKEN = "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"  # Get it from https://huggingface.co/settings/tokens

def generate_test_curls(input_curl):
    prompt = f"""
You are a test automation assistant.
Given this base cURL command:
{input_curl}

Generate 10 variations that test edge cases, missing fields, invalid types, etc.
Return each variation as a full cURL command, one per line.
"""
    client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_TOKEN,
    timeout=1000)

    completion = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],)

    print(completion.choices[0].message)

def run_curl_and_get_response(curl_cmd):
    try:
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Request timed out."

def main():
    input_curl = input("Enter a cURL command: ").strip()

    print("Generating test cases using Hugging Face...")
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



#Nmiikthailli@2912