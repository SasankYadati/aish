import json
from datasets import load_dataset
from openai import OpenAI
from pydantic import BaseModel
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model_dir", type=str, required=True)
args = parser.parse_args()

model_dir = args.model_dir

dataset = load_dataset("westenfelder/NL2SH-ALFA", "test", split = "train")

completions = []
with open(f'{model_dir}/completions.jsonl', 'r') as f:
    for line in f:
        row = json.loads(line)
        completions.append(row['completion'])

n_exact_matches = 0
n_faithful = 0
n_unfaithful = 0
unresolved_examples = []

def clean_completion(completion):
    completion = completion.strip()
    if completion.startswith("```bash"):
        completion = completion[7:]
    if completion.startswith("```"):
        completion = completion[3:]
    if completion.endswith("```"):
        completion = completion[:-3]
    completion = completion.strip()
    return completion

for completion, example in zip(completions, dataset):
    completion = clean_completion(completion)
    if completion == example['bash'] or completion == example['bash2']:
        n_exact_matches += 1
    else:
        unresolved_examples.append((example, completion))

class Evaluation(BaseModel):
    is_faithful: bool
    explanation: str
    
client = OpenAI()

for example, completion in unresolved_examples:
    user_prompt = f"Natural Language Description: {example['nl']}\nLLM's completion: {completion}\nExpert's completion: {example['bash']}"
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "You are an expert in Natural Language to Bash translation. You are given a natural language description, an expert's translation of it in bash, and a LLM's translation of it in bash. Your job is to evaluate whether the LLM's completion is faithful to the task."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        text_format=Evaluation,
    )
    if response.output_parsed.is_faithful:
        n_faithful += 1
    else:
        n_unfaithful += 1
    print(user_prompt)
    print(response.output_parsed)
    print("----------------------------------------")

print(f"Exact matches: {n_exact_matches} / {len(completions)}")
print(f"Faithful: {n_faithful} / {len(unresolved_examples)}")
print(f"Unfaithful: {n_unfaithful} / {len(unresolved_examples)}")

print(f"Accuracy: {(n_faithful + n_exact_matches) / len(completions)}")
