OPENAI_API_KEY = "YOUR-OPENAI-API-KEY"

ANTHROPIC_API_KEY = "YOUR-ANTHROPIC-API-KEY"

DASHSCOPE_API_KEY = "YOUR-DASHSCOPE-API-KEY"

gpt_batch_request_template = {
    "custom_id": "", 
    "method": "POST", 
    "url": "/v1/chat/completions",
    "body": {"model": "",
            "messages": [{"role": "system", "content": ""}, {"role": "user", "content": ""}],
            "max_tokens": 10240}}
claude_batch_request_template = {
    "custom_id": "",
    "params": {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 8192,
        "messages": [
                    {
                        "role": "user",
                        "content": "",
                    }
                ],
            },
        }
qwen_batch_request_template = {
    "custom_id": "request-1", 
    "method": "POST", 
    "url": "/v1/chat/completions", 
    "body": {"model": "qwen-turbo", 
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}, 
                {"role": "user", "content": "What is 2+2?"}]
                }
        }
    

import json

def read_jsonl(file: str) -> list[dict[any,any]]:

    with open(file, 'r') as file:
        results = [json.loads(line.strip()) for line in file]

    return results
