import json
from datasets import load_dataset
from openai import OpenAI
from pydantic import BaseModel

dataset = load_dataset("westenfelder/NL2SH-ALFA", "test", split = "train")

completions = []
with open('completions.jsonl', 'r') as f:
    for line in f:
        completions.append(json.loads(line))

n_exact_matches = 0
unresolved_examples = []
for completion, example in zip(completions, dataset):
  if completion == example['bash'] or completion == example['bash2']:
    n_exact_matches += 1
  else:
    unresolved_examples.append((example, completion))
    print("LLM    : ", completion)
    print("Expert : ", example['bash'])
    print("------------------")
    
print(f"Exact matches: {n_exact_matches}/{len(completions)}")

class Evaluation(BaseModel):
    is_faithful: bool
    explanation: str
    
client = OpenAI()

for example, completion in unresolved_examples:
  response = client.responses.parse(
    model="gpt-4o",
    input=[
        {
            "role": "system",
            "content": "You are an expert in Natural Language to Bash translation. You are given a natural language description, an expert's translation of it in bash, and a LLM's translation of it in bash. Your job is to evaluate whether the LLM's completion is faithful to the task."
        },
        {
            "role": "user",
            "content": f"Natural Language Description: {example['nl']}\nLLM's completion: {completion}\nExpert's completion: {example['bash']}"
        }
    ],
    text_format=Evaluation,
  )
  print(response.output_parsed)
