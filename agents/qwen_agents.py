import json
from copy import deepcopy
from openai import OpenAI
from pathlib import Path
import time
from util import DASHSCOPE_API_KEY, qwen_batch_request_template

'''
Models supported:
qwen-turbo
qwen-plus
qwen-max
'''

def create_requests(
        docs: dict[str, str],
        prompt: str,
        model: str = "qwen-turbo",
        sys_message: str = "You are a helpful assistant.",
        temperature: float = 0.8,
        filename: str = "batch_input.jsonl",
        max_tokens: int = 8192,
        template=qwen_batch_request_template) -> None:

    with open(filename, 'w') as file:
        for i, doc in docs.items():
            item = deepcopy(template)

            item["custom_id"] = f"request-{i}"
            item["body"]["model"] = model
            item["body"]["temperature"] = temperature
            item["body"]["messages"][0]["content"] = sys_message
            item["body"]["messages"][1]["content"] = prompt.format(doc=doc)
            item["body"]["max_tokens"] = max_tokens
            file.write(json.dumps(item) + '\n')

def send_requests(
        filename: str = "batch_input.jsonl",
        api_key: str = DASHSCOPE_API_KEY,
        verbose: bool = True) -> str:
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        file_object = client.files.create(file=Path(filename), purpose="batch")
        batch_input_file_id = file_object.id

        batch_obj = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
        )
        return batch_obj.id
    except Exception as e:
        if verbose:
            print(e)
            
def retrieve_results(
        batch_obj_id: str,
        results_file_name: str,
        check_interval: float = 180,
        verbose: bool = True) -> None:
    try:
        client = OpenAI(api_key=DASHSCOPE_API_KEY, 
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

        while True:

            batch = client.batches.retrieve(batch_obj_id)

            if batch.status == "completed":
                responses = client.files.content(batch.output_file_id).content

                with open(results_file_name, 'wb') as file:
                    file.write(responses)
                break

            elif batch.status in ["failed", "expired", "cancelled"]:
                raise Exception(f"Batch processing failed with status: {batch.status}")

            else:
                time.sleep(check_interval)

    except Exception as e:
        if verbose:
            print(e)