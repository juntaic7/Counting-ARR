import argparse

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
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Provide the path to save the batch output file."
    )
    
    args = parser.parse_args()
    if args.agent == "claude":
        from agents.claude_agents import retrieve_results
    elif args.agent == "gpt":
        from agents.gpt_agents import retrieve_results
    elif args.agent == "qwen":
        from agents.qwen_agents import retrieve_results
    retrieve_results(args.batch_id, args.path)
    print(f"Batch results of job {args.batch_id} successfully saved to {args.path}.")
    
if __name__ == "__main__":
    main()