import json
import time
from openai import AzureOpenAI
from tqdm import tqdm

client = AzureOpenAI(
    api_key="609ced4d971240b8a08f7fb0e6d846ea",
    api_version="2024-08-01-preview",
    azure_endpoint="https://promptdelta-nc.openai.azure.com",  
)

# --- Loaders ---
def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

# --- Prompt Builder ---
def build_prompt(query, review_data, meta_data, db_description, prompt_template):
    return prompt_template.format(
        query=query,
        db_description=db_description,
        review_batch=json.dumps(review_data, indent=2),
        meta_batch=json.dumps(meta_data, indent=2)
    )

# --- GPT Caller ---
def call_gpt(prompt, deployment_name):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You answer semantic data queries using JSON databases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return None

# --- Runner ---
def run_model():
    queries = json.loads(load_file("queries.json"))
    db_description = load_file("db_description.txt")
    prompt_template = load_file("prompt_template.txt")
    meta_data = load_json_file("dataset/light_meta.json")
    review_data = load_json_file("dataset/light_review.json")

    for query in queries:
        print(f"\n🔍 Running query: {query}")
        results = []

        batch_size = 40
        for i in tqdm(range(0, len(meta_data), batch_size)):
            meta_batch = meta_data[i:i+batch_size]
            gmap_ids = {m["gmap_id"] for m in meta_batch}
            review_batch = [r for r in review_data if r["gmap_id"] in gmap_ids]

            prompt = build_prompt(query, meta_batch, review_batch, db_description, prompt_template)
            result = call_gpt(prompt, deployment_name="gpt-4o")
            if result:
                results.append(result)

            time.sleep(1)

        print(f"\nCombined results for query '{query}':")
        for idx, res in enumerate(results):
            print(f"\nBatch {idx+1}:\n{res}")

if __name__ == "__main__":
    run_model()
