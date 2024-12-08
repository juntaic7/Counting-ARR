import argparse
from anthropic import Anthropic
from openai import OpenAI
from util import OPENAI_API_KEY, ANTHROPIC_API_KEY, DASHSCOPE_API_KEY


def main():
    parser = argparse.ArgumentParser(description="Check the status of a batch job.")
    parser.add_argument(
        "-a", "--agent",
        type=str,
        choices=["gpt", "claude", "qwen"],
        required=True,
        help="Specify the agent working on the job (gpt or claude)."
    )
    parser.add_argument(
        "-b", "--batch_id",
        type=str,
        required=True,
        help="Provide the batch ID of the job to check."
    )
    
    args = parser.parse_args()
    if args.agent == "claude":
        client = Anthropic(api_key= ANTHROPIC_API_KEY)
        message = client.beta.messages.batches.retrieve(args.batch_id)
    elif args.agent == "gpt":
        client = OpenAI(api_key=OPENAI_API_KEY)
        message = client.batches.retrieve(args.batch_id)
    elif args.agent == "qwen":
        client = OpenAI(api_key=DASHSCOPE_API_KEY, 
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)
        message = client.batches.retrieve(args.batch_id)
    print(f"Status of batch job {args.batch_id}:\n {message}")
    
if __name__ == "__main__":
    main()