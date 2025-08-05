import argparse
import json
import random
import string
from random_word import RandomWords
import nltk
from nltk.corpus import words, brown

def generate_random_string(min_len: int, max_len: int) -> str:
    """
    Generates a random string of letters with length between min_len and max_len.
    """
    length = random.randint(min_len, max_len)
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for _ in range(length))
    return random_str

def get_common_words() -> list[str]:
    # Get word frequencies from Brown corpus
    word_freq = nltk.FreqDist(w.lower() for w in brown.words())
    
    # Get the most common words (e.g., top 1000)
    common_words = [word for word, freq in word_freq.most_common(6000)]
    
    # Filter out very short words and non-alphabetic words
    common_words = [word for word in common_words if len(word) >= 3 and word.isalpha()]
    
    return common_words

def main():
    parser = argparse.ArgumentParser(description="Generate a dataset of reversing string task.")
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
        "-w", "--word",
        action='store_true',
        default=False,  
        help="Generate dataset using English words."
    )
    parser.add_argument(
        "-f", "--high_freq_word",
        action='store_true',
        default=False,  
        help="Generate dataset using high frequency English words."
    )
    args = parser.parse_args()

    dataset = []
    
    assert not (args.word and args.high_freq_word), "Only one of --word or --high_freq_word can be used."
    
    if args.word:
        r = RandomWords()
        for i in range(args.num):
            random_str = ""
            while len(random_str) < args.lower:
                random_str += r.get_random_word()
            if len(random_str) > args.upper:
                random_str = random_str[:args.upper]
            dataset.append({"id": i, "string": random_str, "reversed": random_str[::-1]})
        out_file = f"reverse_string/datasets/reverse_word_{args.lower}_{args.upper}.jsonl"
        
    elif args.high_freq_word:
        common_words = get_common_words()
        for i in range(args.num):
            random_str = ""
            while len(random_str) < args.lower:
                word = random.choice(common_words)
                if len(random_str) + len(word) <= args.upper:
                    random_str += word
            if len(random_str) > args.upper:
                random_str = random_str[:args.upper]
            dataset.append({"id": i, "string": random_str, "reversed": random_str[::-1]})
        out_file = f"reverse_string/datasets/reverse_high_freq_word_{args.lower}_{args.upper}.jsonl"
        
    else:
        for i in range(args.num):
            random_str = generate_random_string(args.lower, args.upper)
            dataset.append({"id": i, "string": random_str, "reversed": random_str[::-1]})
        out_file = f"reverse_string/datasets/reverse_{args.lower}_{args.upper}.jsonl"
    
    with open(out_file, "w") as file:
        for item in dataset:
            file.write(json.dumps(item) + '\n')
            
    print(f"Dataset successfully saved to {out_file}")
            
if __name__ == "__main__":
    main()