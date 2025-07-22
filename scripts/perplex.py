import os
import sys
import requests
import json

# Set your Perplexity API Key as PPLX_API_KEY env variable
PPLX_API_KEY = os.environ.get("OPENAI_API_KEY")
PPLX_MODEL = "sonar-pro"
PPLX_URL = "https://api.perplexity.ai/chat/completions"

def parse_log_file(log_file_path):
    start_tag = "Start log summary"
    end_tag = "End log summary"

    with open(log_file_path, 'r') as f:
        lines = f.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if start_tag in line:
            start_index = i + 1
        elif end_tag in line and start_index is not None:
            end_index = i
            break

    if start_index is None:
        raise ValueError("Start tag not found in log file.")
    if end_index is None:
        raise ValueError("End tag not found in log file.")
    if start_index >= end_index:
        raise ValueError("Start tag appears after end tag.")

    return ''.join(lines[start_index:end_index]).strip()


def generate_summary_with_perplexity(log_content):
    if not PPLX_API_KEY:
        raise EnvironmentError("❌ Please set PPLX_API_KEY as an environment variable.")

    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": PPLX_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Summarize CI/CD build logs as a markdown bullet list, suitable for a GitHub pull request."
            },
            {
                "role": "user",
                "content": log_content
            }
        ],
        "temperature": 0.5,
        "max_tokens": 300
    }

    response = requests.post(PPLX_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"❌ API error: {response.status_code} — {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()


def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_log_and_summarize_pplx.py <log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    try:
        log_text = parse_log_file(log_file_path)
        summary = generate_summary_with_perplexity(log_text)

        with open("summary.txt", "w") as f:
            f.write(summary)

        print("✅ Summary written to summary.txt")
        print("\n" + summary)

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
