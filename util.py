OPENAI_API_KEY = "YOUR-OPENAI-API-KEY"

ANTHROPIC_API_KEY = "YOUR-ANTHROPIC-API-KEY"

gpt_batch_request_template = {
    "custom_id": "", 
    "method": "POST", 
    "url": "/v1/chat/completions",
    "body": {"model": "",
            "messages": [{"role": "system", "content": ""}, {"role": "user", "content": ""}],
            "max_tokens": 1000}}
claude_batch_request_template = {
    "custom_id": "",
    "params": {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 100,
        "messages": [
                    {
                        "role": "user",
                        "content": "",
                    }
                ],
            },
        }

import json

def read_jsonl(file: str) -> list[dict[any,any]]:

    with open(file, 'r') as file:
        results = [json.loads(line.strip()) for line in file]

    return results
