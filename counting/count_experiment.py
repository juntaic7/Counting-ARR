import random
import argparse
import json
from agents import gpt_agents as gpt, claude_agents as claude, qwen_agents as qwen
from util import read_jsonl

def generate_string(min_len: int, max_len: int, letters: str="ab") -> str:
    """Generates a random string with length between min_len and max_len."""
    length = random.randint(min_len, max_len)
    sample = ''.join(random.choice(letters) for _ in range(length))
    return sample

def generate_samples(min_len: int, max_len: int, num: int, letters: str="ab") -> list[str]:
    """Generates num unique random strings with length between min_len and max_len."""
    samples = set()
    
    while len(samples) < num:
        samples.add(generate_string(min_len, max_len, letters))
    
    return list(samples)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random strings composed of letters with counting information.")

    parser.add_argument(    
        "-d", "--dataset",
        type=str,
        help="The path to load the dataset."
    )
    
    parser.add_argument(
        "-n", "--num",
        type=int,
        help="Number of samples to generate."
    )

    parser.add_argument(
        "-l", "--lower",
        type=int,
        help="Lower bound of sample length."
    )

    parser.add_argument(
        "-u", "--upper",
        type=int,
        help="Upper bound of sample length."
    )

    parser.add_argument(
        "-t", "--letters",
        type=str,
        help="Letters used in the dataset."
    )

    parser.add_argument(    
        "-c", "--content",
        type=str,
        required=True,
        help="The content (substring) to evaluate."
    )

    parser.add_argument(    
        "-e", "--experiment",
        type=int,
        choices=[1,2,3,4],
        required=True,
        help="The type of experiment."
    )
    
    parser.add_argument(    
        "-o", "--cot",
        action='store_true',
        help="Enable CoT."
    )

    parser.add_argument(    
        "-s", "--supervised_cot",
        action='store_true',
        help="Enable supervised CoT."
    )

    parser.add_argument(    
        "-a", "--agent",
        default="gpt",
        choices=["gpt", "claude", "qwen"],
        help="Choose foundation model."
    )

    parser.add_argument(    
        "-m", "--model",
        help="Specify model version."
    )


    args = parser.parse_args()

    assert args.dataset is not None or (args.num is not None and args.lower is not None and args.upper is not None and args.letters is not None), "Either provide a dataset or specify the number of samples to generate."
    

    if not args.dataset:
        assert args.lower < args.upper, "Lower bound of length cannot be greater than upper bound."
        assert args.content in args.letters, "Content must be a letter in the dataset."

        random.seed(42)
        samples = generate_samples(min_len=args.lower, max_len=args.upper, num=args.num, letters=args.letters)

        dataset = []
        for i, sample in enumerate(samples):
            line = {"id": i,
                    "sample": sample,
                    }
            for letter in args.letters:
                line[letter] = sample.count(letter)
            dataset.append(line)

        output_file = f"counting/dataset/count_dataset_{args.lower}_{args.upper}_{args.letters}.jsonl"
        with open(output_file, "w") as f:
            for entry in dataset:
                f.write(json.dumps(entry) + "\n")

        print(f"Dataset saved to {output_file}.")
    else:
        dataset = read_jsonl(args.dataset)

    docs = {}
    
    if args.cot or args.supervised_cot:
        assert (args.cot and args.supervised_cot) is False, "You cannot enable both CoT and supervised CoT."

    if args.supervised_cot:
        with open(f"counting/prompts/count.supervise.txt", 'r') as file:
            prompt = file.read().strip()
    elif args.cot:
        with open(f"counting/prompts/count.cot.txt", 'r') as file:
            prompt = file.read().strip()
    else:
        with open(f"counting/prompts/count.txt", 'r') as file:
            prompt = file.read().strip()

    match args.experiment:
        case 1:
            for line in dataset:
                docs[str(line["id"])] = prompt.format(sample=line["sample"], substring = args.content)
        case 2:
            for line in dataset:
                docs[str(line["id"])] = prompt.format(sample=', '.join(line["sample"]), substring = args.content)
        case 3:
            for line in dataset:
                docs[str(line["id"])] = prompt.format(sample=str(list(line["sample"])), substring = args.content)
        case 4:
            for line in dataset:
                docs[str(line["id"])] = prompt.format(sample=' '.join(line["sample"]), substring = args.content)

    if args.agent == "gpt":
        gpt.create_requests(docs=docs, prompt="{doc}", model=args.model if args.model else "gpt-4o-mini")
        gpt.send_requests()
        print(f"Requests sent to evaluate counting ability for {args.content}. Please download the batch_output file from the gpt API dashboard.")
    elif args.agent == "claude":
        claude.create_requests(docs=docs, prompt="{doc}", model=args.model if args.model else "claude-3-5-sonnet-20240620")
        batch_id = claude.send_requests()
        print(f"Requests sent to evaluate counting ability for {args.content}. Please check the batch_output file via batch id:\n{batch_id}.")
    elif args.agent == "qwen":
        qwen.create_requests(docs=docs, prompt="{doc}", model=args.model if args.model else "qwen-turbo")
        batch_id = qwen.send_requests()
        print(f"Requests sent to evaluate counting ability for {args.content}. Please check the batch_output file via batch id:\n{batch_id}.")
        