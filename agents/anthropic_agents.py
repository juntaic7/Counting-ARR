from anthropic import Anthropic
from copy import deepcopy
import json

from util import claude_batch_request_template, ANTHROPIC_API_KEY, read_jsonl

def create_requests(
        docs: dict[str, str],
        prompt: str,
        model: str = "claude-3-5-sonnet-20240620",
        sys_message: str = "You are a helpful assistant.",
        filename: str = "batch_input.jsonl",
        max_tokens: int = 4096,
        template=claude_batch_request_template) -> None:
    with open(filename, 'w') as file:
        for i, doc in docs.items():
            item = deepcopy(template)

            item["custom_id"] = f"request-{i}"
            item["params"]["model"] = model
            item["params"]["max_tokens"] = max_tokens
            item["params"]["messages"][0]["content"] = prompt.format(doc=doc)
            file.write(json.dumps(item) + '\n')
    

def send_requests(
        filename: str = "batch_input.jsonl",
        verbose: bool = True) -> str:
    try:
        client = Anthropic(
            api_key= ANTHROPIC_API_KEY
            )

        requests = read_jsonl(filename)

        batch_obj = client.beta.messages.batches.create(requests=requests)
        return batch_obj.id
    except Exception as e:
        if verbose:
            print(e)

def retrieve_results(
        batch_id: str,
        filename: str = "batch_output.jsonl",
        verbose: bool = True) -> list[dict[str, str]]:
    try:
        client = Anthropic(
            api_key= ANTHROPIC_API_KEY
            )
        results = []
        with open(filename, 'w') as file:
            for result in client.beta.messages.batches.results(batch_id):
                line = {}
                line['id'] = result.custom_id.split('-')[1]
                line['result'] = result.result.message.content[0].text
                results.append(line)
                file.write(json.dumps(line) + '\n')
        return results

    except Exception as e:
        if verbose:
            print(e)