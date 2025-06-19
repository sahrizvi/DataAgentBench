#Query 1: “What are the top 5 locations with the highest average score in Los Angeles?”
import json
import random
from tqdm import tqdm
from openai import AzureOpenAI

def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = [json.loads(line.strip()) for line in f if line.strip()]
        print(f"✅ Loaded {len(data)} records from {file_path}")
        return data
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error in {file_path}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error reading {file_path}: {e}")
    return []

    
    
def query_top_locations_by_llm(query_text: str, review_json_path: str, meta_json_path: str, deployment_name: str) -> str:
    review_data = load_json_file(review_json_path)
    meta_data = load_json_file(meta_json_path)
    
    prompt = f"""
        You are an AI assistant helping to answer structured semantic queries using two JSON-based datasets.

        ---

        **Data Sources:**

        1. **review_dataset**
        - Database content:{json.dumps(review_data, indent=2)}
        - Contains user reviews for Google Maps locations.
        - Fields:
            - user_id (float)
            - name (str)
            - time (str)
            - rating (int)
            - text (str)
            - pics (dict)
            - resp (dict)
            - gmap_id (str) 

        2. **meta_dataset**
        - Database content:{json.dumps(meta_data, indent=2)}
        - Contains business metadata for Google Maps locations.
        - Fields:
            - name (str)
            - gmap_id (str)
            - description (str)
            - num_of_reviews (int)
            - price (float)
            - hours (list), 
            - MISC (dict), 
            - state (string), 
            - relative_results (list), 
            - url (string),

        ---

        **Your Task:**
        Answer the following query using information from both datasets:

        **Query:** {query_text}

        Provide a clean, readable list of the top businesses and their average ratings.
        """

#**Instructions:**
#- Join review_dataset and meta_dataset via `gmap_id`.
#- The `meta_dataset` does not have a structured "city" column. Instead, location info (e.g., "Los Angeles") is embedded in the `description` field. Use this to infer which businesses are located in the target city or region.
#- Group reviews by business, and compute the average rating for each.
#- For businesses located in the target location (e.g., Los Angeles), return the top-N based on average rating.

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers data-driven business queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=None
        )
        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None


if __name__ == "__main__":
    client = AzureOpenAI(
    api_key="609ced4d971240b8a08f7fb0e6d846ea",
    api_version="2024-08-01-preview",
    azure_endpoint="https://promptdelta-nc.openai.azure.com",  
)

    deployment_name = "gpt-4o-mini"  
    query_text = "What are the top 5 locations with the highest average score in Los Angeles?"
    review_json_path = "../dataset/googlelocal/light_review_LLM_tt.json"
    meta_json_path = "../dataset/googlelocal/light_meta_LLM_tt.json"
    result = query_top_locations_by_llm(
        query_text=query_text,
        review_json_path=review_json_path,
        meta_json_path=meta_json_path,
        deployment_name=deployment_name
    )

    if result:
        print("📍 Query Result:\n", result)
    else:
        print("⚠️ No result returned.")




