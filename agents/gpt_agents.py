# Some parts are adapted/modified from OPENAI Cookbook (https://cookbook.openai.com/examples/batch_processing)
# Results can be monitored/downloaded from the dashboard on OpenAI API platform.
import json
from copy import deepcopy
from openai import OpenAI
import time

from util import OPENAI_API_KEY, gpt_batch_request_template


def create_requests(
        docs: dict[str, str],
        prompt: str,
        model: str = "gpt-4o-mini",
        sys_message: str = "You are a helpful assistant.",
        filename: str = "batch_input.jsonl",
        max_tokens: int = 10240,
        template=gpt_batch_request_template) -> None:

    with open(filename, 'w') as file:
        for i, doc in docs.items():
            item = deepcopy(template)

            item["custom_id"] = f"request-{i}"
            item["body"]["model"] = model
            item["body"]["messages"][0]["content"] = sys_message
            item["body"]["messages"][1]["content"] = prompt.format(doc=doc)
            item["body"]["max_tokens"] = max_tokens
            file.write(json.dumps(item) + '\n')


def send_requests(
        filename: str = "batch_input.jsonl",
        api_key: str = OPENAI_API_KEY,
        verbose: bool = True) -> str:
    try:
        client = OpenAI(
            api_key=api_key,
        )
        batch_input_file = client.files.create(
            file=open(filename, "rb"),
            purpose="batch"
        )

        batch_input_file_id = batch_input_file.id

        batch_obj = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": "nightly Eval job"
            }
        )
        return batch_obj.id
    except Exception as e:
        if verbose:
            print(e)

# We recommend download batch_output file directly from Batches section in openai api dashboard.
def retrieve_results(
        batch_obj_id: str,
        results_file_name: str = "batch_job_results.jsonl",
        check_interval: float = 180,
        api_key: str = OPENAI_API_KEY,
        verbose: bool = True) -> None:
    try:
        client = OpenAI(
            api_key=api_key,
        )

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

