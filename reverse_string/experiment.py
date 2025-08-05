import argparse
from datetime import datetime
import os
from utils import read_jsonl
from agents.gpt_batch_agents import create_requests, send_requests

def main():
    parser = argparse.ArgumentParser(description="Calculate accuracy.")
    parser.add_argument(    
        "-d", "--dataset",
        type=str,
        required=True,
        help="The path to load the dataset."
    )
    
    parser.add_argument(    
        "-s", "--supervised_cot",
        action='store_true',
        default=False,
        help="Enable supervised CoT."
    )
    
    parser.add_argument(    
        "-e", "--experiment",
        type=int,
        choices=[1,2],
        required=True,
        help="The type of experiment."
    )
    
    parser.add_argument(    
        "-m", "--model",
        default="gpt-4o-mini",
        help="Specify model version."
    )
    
    args = parser.parse_args()
    dataset = read_jsonl(args.dataset)
    docs = {}
            
    match args.experiment:
        case 1:
            if args.supervised_cot:
                with open(f"reverse_string/prompts/reverse.supervise.txt", 'r') as file:
                    prompt = file.read().strip()
            else:  
                with open(f"reverse_string/prompts/reverse.cot.txt", 'r') as file:
                    prompt = file.read().strip()
            for line in dataset:
                docs[str(line["id"])] = prompt.replace("{{string}}", line["string"])
        case 2:
            if args.supervised_cot:
                with open(f"reverse_string/prompts/reverse.list.supervise.txt", 'r') as file:
                    prompt = file.read().strip()
            else:  
                with open(f"reverse_string/prompts/reverse.list.cot.txt", 'r') as file:
                    prompt = file.read().strip()
            for line in dataset:
                docs[str(line["id"])] = prompt.replace("{{string}}", str(list(line["string"])))

    create_requests(docs=docs, prompt="{doc}", model=args.model)
    batch_id = send_requests()
    
    print(f"Requests sent to evaluate ability of GPT in reversing.\nPlease download the batch_output file from the OpenAI API dashboard, or retrieve the result using the batch id {batch_id}.\nBatch request details will be saved to batch_history.txt for future reference.")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('batch_history.txt', 'a') as file:
        file.write(f"{current_time} - {os.path.splitext(os.path.basename(args.dataset))[0]} - {args.model} - {args.experiment} - {args.supervised} - {batch_id}\n")
if __name__ == "__main__":
    main()