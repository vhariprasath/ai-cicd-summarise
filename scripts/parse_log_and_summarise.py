import sys
import os
import openai

def extract_log_section(logfile):
    with open(logfile) as f:
        lines = f.readlines()
    start_idx = next(i for i, l in enumerate(lines) if "start log summary" in l)
    end_idx = next(i for i, l in enumerate(lines) if "end log summary" in l)
    return ''.join(lines[start_idx + 1:end_idx])

def main():
    logfile = sys.argv[1]
    log = extract_log_section(logfile)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = "Create a summary of this log for a comment on a PR. Use markdown format for readability:\n" + log

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=256
    )
    summary = response.choices[0].text.strip()
    with open("summary.txt", "w") as f:
        f.write(summary)

if __name__ == "__main__":
    main()
