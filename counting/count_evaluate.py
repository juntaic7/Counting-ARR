import argparse
from util import read_jsonl
import json
import os
from agents.claude_agents import retrieve_results

def main():
    parser = argparse.ArgumentParser(description="Calculate accuracy.")
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path of batch_output file from GPT/claude, or path to save the batch results from claude if batch id is provided."
    )
    parser.add_argument(
        "-b", "--batch",
        type=str,
        help="The batch id from claude."
    )
    parser.add_argument(
        "-d", "--dataset",
        type=str,
        required=True,
        help="Path of the dataset."
    )
    parser.add_argument(
        "-c", "--content",
        type=str,
        required=True,
        help="The content (substring) to evaluate."
    )

    parser.add_argument(
        "-a", "--agent",
        type=str,
        default="gpt",
        choices=["gpt", "claude", "qwen"],
        help="The foundation model for evaluation."
    )
    
    
    args = parser.parse_args()
    
    preds = {}
    dataset = read_jsonl(args.dataset)
    match args.agent:
        case "gpt":
            results = read_jsonl(args.path)
            for r in results:
                id = int(r["custom_id"].split("-")[1])
                completion = r["response"]["body"]["choices"][0]["message"]["content"]
                if completion.rfind("Result: ") != -1:
                    last_result_index = completion.rfind("Result: ")
                    padding = len("Result: ")
                else:  
                    print(f"Completion: {repr(completion)}")
                    raise Exception(f"'Result:' not found in response for ID {id}. Please check the response and revise prompt template.")
                
                result_str = completion[last_result_index + padding:].strip()

                try:
                    preds[id] = int(result_str)
                except (ValueError, TypeError) as e:
                    print(f"Error converting result_str to int for ID {id}: {e}. Setting prediction to 0.")
                    pass
        case "claude":
            if args.batch is not None:
                results = retrieve_results(args.batch, args.path)
            else:
                results = read_jsonl(args.path)
            for r in results:
                id = int(r["id"])
                completion = r["result"]
                if completion.rfind("Result: ") != -1:
                    last_result_index = completion.rfind("Result: ")
                    padding = len("Result: ")
                else:  
                    print(f"Completion: {repr(completion)}")
                    raise Exception(f"'Result:' not found in response for ID {id}. Please check the response and revise prompt template.")
                
                result_str = completion[last_result_index + padding:].strip()
                try:
                    preds[id] = int(result_str)
                except (ValueError, TypeError) as e:
                    print(f"Error converting result_str to int for ID {id}: {e}. Setting prediction to 0.")
                    pass

    differences = {}
    correct_count = 0
    for idx, pred in preds.items():
        if pred == dataset[idx][args.content]:
            correct_count += 1
        else:
            difference = pred - dataset[idx][args.content]
            if difference not in differences:
                differences[difference] = 0
            differences[difference] += 1
    
    accuracy = correct_count / len(preds) if len(preds) > 0 else 0
    print(f"The final accuracy is: {accuracy:.2%}")
    print(f"Differences: {differences}")

    dirname = os.path.dirname(args.path)
    basename = os.path.basename(args.path) 
    name, ext = os.path.splitext(basename)
    filename = f"{name}_eval.json"          
    path = os.path.join(dirname, filename)
    with open(path, 'w') as file:
        json.dump(differences, file, indent=4)

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
