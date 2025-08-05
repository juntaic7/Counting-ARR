import argparse
import json
import random
import string

def generate_random_letter_string(min_len: int, max_len: int) -> str:
    """
    Generates a random string of letters with length between min_len and max_len (upper and lower case letters).
    """
    length = random.randint(min_len, max_len)
    random_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return random_str

def generate_random_number_string(min_len: int, max_len: int) -> str:
    """
    Generates a random string of letters with length between min_len and max_len (digits).
    """
    length = random.randint(min_len, max_len)
    random_str = ''.join(random.choice(string.digits) for _ in range(length))
    return random_str

def generate_random_string(min_len: int, max_len: int) -> str:
    """
    Generates a random string of letters with length between min_len and max_len (upper, lower case letters and digits).
    """
    length = random.randint(min_len, max_len)
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return random_str

def main():
    parser = argparse.ArgumentParser(description="Generate a dataset of sorting task.")
    parser.add_argument(
        "-n", "--num",
        type=int,
        help="Number of samples to generate."
    )
    parser.add_argument(
        "-l", "--lower",
        required=True,
        type=int,
        help="Lower bound of sample length."
    )
    parser.add_argument(
        "-u", "--upper",
        required=True,
        type=int,
        help="Upper bound of sample length."
    )
    parser.add_argument(
        "-e", "--letter_only",
        action='store_true',
        default=False,
        help="Generate letter-only dataset."
    )
    parser.add_argument(
        "-d", "--digit_only",
        action='store_true',
        default=False,
        help="Generate digit-only dataset."
    )
    args = parser.parse_args()
    dataset = []
    
    for i in range(args.num):
        if args.letter_only:
            random_str = generate_random_letter_string(args.lower, args.upper)
            dataset.append({"id": i, "string": random_str, "sorted": ''.join(sorted(random_str))})
            out_file = f"sorting/datasets/sort_letters_{args.lower}_{args.upper}.jsonl"
        elif args.digit_only:
            random_str = generate_random_number_string(args.lower, args.upper)
            dataset.append({"id": i, "string": random_str, "sorted": ''.join(sorted(random_str))})
            out_file = f"sorting/datasets/sort_digits_{args.lower}_{args.upper}.jsonl"
        else:
            random_str = generate_random_string(args.lower, args.upper)
            dataset.append({"id": i, "string": random_str, "sorted": ''.join(sorted(random_str))})
            out_file = f"sorting/datasets/sort_{args.lower}_{args.upper}.jsonl"
    
    with open(out_file, 'w') as file:
        for line in dataset:
            file.write(json.dumps(line) + "\n")
    print(f"Dataset successfully saved to {out_file}.")
    
if __name__ == "__main__":
    main()