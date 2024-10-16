# Role of Tokenization in the Counting Ability of Language Models

This project explores the role of tokenization in the counting abilities of various language models. Tokenization, the process of converting a sequence of characters into tokens, can significantly affect how well models perform on tasks requiring the counting of characters or tokens. The different methods of tokenization are illustrated below, showing how they affect the representation of a simple string when counting the number of occurrences of the character 'a'.

## Counting Example

In this example, we count the number of times the character "a" appears in different tokenized forms of the same string.

### The String Variations:

- **(a) Original String**: `abbab`
- **(b) Spaced String**: `a b b a b`
- **(c) Comma-separated String**: `a, b, b, a, b`
- **(d) Quoted String**: `"a", "b", "b", "a", "b"`

Each string produces a different number of tokens and characters, which impacts the model's ability to count accurately.

### Tokenization and Character Count

- **(a) Original String**: 5 characters, 2 tokens
- **(b) Spaced String**: 9 characters, 5 tokens
- **(c) Comma-separated String**: 13 characters, 9 tokens
- **(d) Quoted String**: 23 characters, 14 tokens

The figure below illustrates these examples with tokenization details.

![Tokenization Example](./tokenizations.png)

## Examples of Running Experiments

```bash
# Run an experiment with a newly generated dataset
# -n: Number of examples (e.g., 1000)
# -l: Minimum sequence length (e.g., 20)
# -u: Maximum sequence length (e.g., 30)
# -t: The letter set (e.g., "ab" for constructing a dataset with "a" and "b")
# -c: The target character to count (e.g., "a")
# -e: The experiment version or type (e.g., 1 for original string)
python -m counting.count_experiment -n 1000 -l 20 -u 30 -t "ab" -c "a" -e 1 

# Run an experiment using an existing dataset with supervised chain-of-thought
# -d: Path to the existing dataset
# -c: The target character to count (e.g., "a")
# -e: The experiment type (e.g., 3 for Quoted String)
# -s: Enables supervised chain-of-thought
python -m counting.count_experiment -d "path_to_dataset" -c "a" -e 3 -s

```

### Experiment Number Correspondence to Tokenization

- **(a) Original String**: `-e 1`
- **(b) Spaced String**: `-e 4`
- **(c) Comma-separated String**: `-e 2`
- **(d) Quoted String**: `-e 3`

## Examples of Evaluating Experiment Results

```bash
# Evaluate experiment results
# -d: Path to the dataset used for the experiment
# -p: Path to the result file to be evaluated
# -c: The target character that was counted (e.g., 'a')
python -m counting.evaluate -d "path_to_dataset" -p "path_to_result_file" -c a
```
