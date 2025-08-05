import argparse
from utils import read_jsonl


def extract_result(completion_text):
    start = completion_text.rfind('{')
    end = completion_text.rfind('}')
    if start != -1 and end != -1 and start < end:
        content = completion_text[start + 1:end]
        if "'Result'" in content or '"Result"' in content:
            value_start = content.find(':') + 1
            value = content[value_start:].strip().strip("'\" ")
            return value
    return None



def main():
    parser = argparse.ArgumentParser(description="Calculate accuracy.")
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path of batch_output file."
    )
    parser.add_argument(
        "-d", "--dataset",
        type=str,
        required=True,
        help="Path of the dataset."
    )
    
    args = parser.parse_args()
    
    dataset = read_jsonl(args.dataset)
    results = read_jsonl(args.path)
    
    preds = {}
    for r in results:
        id = int(r["custom_id"].split("-")[1])
        completion = r["response"]["body"]["choices"][0]["message"]["content"]
        
        result_str = extract_result(completion)
        if result_str is not None:
            preds[id] = result_str
        else:
            print(f"Result not found in response for ID {id}. Please check the response and revise prompt template.")
            print(f"Completion: {repr(completion)}")
            continue
    with open("results.json", "w") as f:
        f.write(str(preds))
        
    correct = []
    for idx, pred in preds.items():
        try:
            if pred == dataset[idx]["reversed"]:
                correct.append(idx)
        except:
            print(f"Fix the expression in the result for ID {idx}.")
            continue

    accuracy = len(correct) / len(preds) if len(preds) > 0 else 0
    print(f"The final accuracy is: {accuracy:.2%}")
    # print(f"Correct: {correct}")
    
if __name__ == "__main__":
    main()
    