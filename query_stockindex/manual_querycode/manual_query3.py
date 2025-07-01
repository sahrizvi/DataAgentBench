import pandas as pd
import sqlite3
import duckdb
import json
import re
import ast
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import AzureOpenAI

# ========= Step 1: Load index_info from SQLite ==========
conn_info = sqlite3.connect("../query_dataset/indexInfo_query.db")
df_info = pd.read_sql("SELECT * FROM index_info", conn_info)
conn_info.close()

# ========= Step 2: Setup Azure OpenAI Client ==========
client = AzureOpenAI(
    api_key="609ced4d971240b8a08f7fb0e6d846ea",
    api_version="2024-08-01-preview",
    azure_endpoint="https://promptdelta-nc.openai.azure.com",
)
deployment_name = "gpt-4o"

# ========= Step 3: Define LLM inference function ==========
def infer_region_and_symbol(exchange_name, client, deployment_name):
    prompt = (
         f"""You are given the name of a stock exchange: '{exchange_name}'.
            Please answer the following two fields:
            - Region: The **country** it belongs to (e.g., Japan, India, United States).
            - Index Symbol: The exact symbol used in financial datasets or APIs (e.g., from Yahoo Finance, TradingView, Bloomberg).

            Important:
            - The Index Symbol must be the actual code used in trading data (e.g., in Yahoo Finance).
            - Do NOT return descriptive names like “KOSPI” or “JSE All Share Index”.
            - Return only the standard **index code** used in market data feeds.

            Format:
            Region: <country>  
            Index Symbol: <symbol>"""
    )
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a financial assistant that maps stock exchanges to their country and index symbol."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=50
        )
        output = response.choices[0].message.content.strip().split("\n")
        region = output[0].replace("Region:", "").strip()
        index_symbol = output[1].replace("Index Symbol:", "").strip()
        return region, index_symbol
    except Exception as e:
        print(f"[ERROR] {exchange_name}: {e}")
        return None, None

# ========= Step 4: Apply LLM to get region and symbol ==========
df_info["region"] = ""
df_info["index_symbol"] = ""

for i, row in tqdm(df_info.iterrows(), total=len(df_info)):
    exchange = row.get("Exchange", "")
    if not exchange:
        continue
    region, symbol = infer_region_and_symbol(exchange, client, deployment_name)
    df_info.at[i, "region"] = region
    df_info.at[i, "index_symbol"] = symbol
    print(f"[{i}] Exchange: {exchange} | Region: {region} | Symbol: {symbol}")

# ========= Step 5: Load index_trade from DuckDB ==========
con_trade = duckdb.connect("../query_dataset/indexTrade_query.db")
df_trade = con_trade.execute("SELECT * FROM index_trade").fetchdf()
con_trade.close()

# ========= Step 6: Extract unique symbols ==========
index_symbol_list = sorted(df_info["index_symbol"].dropna().unique().tolist())
index_list = sorted(df_trade["Index"].dropna().unique().tolist())

# ========= Step 7: Build and send prompt for mapping ==========
def build_mapping_prompt(index_symbols, index_list):
    return (
        "You are given two lists of stock index symbols from two different datasets.\n\n"
        f"List A (`index_symbol` from metadata):\n{json.dumps(index_symbols, indent=2)}\n\n"
        f"List B (`Index` from trading data):\n{json.dumps(index_list, indent=2)}\n\n"
        "Each symbol in List A has exactly one semantically equivalent counterpart in List B.\n"
        "Your task is to map each symbol in List A to its corresponding symbol in List B.\n\n"
        "For example, if 'KS11' appears in both lists, then:\n"
        "  'KS11' in List A → 'KS11' in List B\n\n"
        "Respond ONLY with a Python dictionary in this format (no explanation, no markdown):\n"
        "{\n"
        "  '<index_symbol_from_list_A>': '<corresponding_Index_from_list_B>',\n"
        "  ...\n"
        "}"
    )


prompt = build_mapping_prompt(index_symbol_list, index_list)
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a financial data assistant matching index symbols across datasets."},
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    max_tokens=800
)

reply = response.choices[0].message.content.strip()
try:
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    code_str = match.group(0) if match else reply
    index_symbol_to_index = ast.literal_eval(code_str)
except Exception as e:
    print("❌ Failed to parse GPT response:\n", reply)
    raise e

print("\n✅ Inferred Mapping:")
print(index_symbol_to_index)

# ========= Step 8: Merge metadata and trade data ==========
df_info["index_mapped"] = df_info["index_symbol"].map(index_symbol_to_index)
df_joined = pd.merge(df_info, df_trade, left_on="index_mapped", right_on="Index", how="inner")

# ========= Step 9: Normalize dates using GPT ==========
def normalize_batch_dates(dates):
    prompt = (
        "You are given a list of date strings in natural language format.\n"
        "Convert each of them into ISO format (yyyy-mm-dd).\n"
        "If any date is invalid, return 'None' for that entry.\n\n"
        "Input:\n"
        + json.dumps(dates, indent=2) + "\n\n"
        "Output:\n"
        "**Only return a plain Python list of ISO-formatted date strings in same order**, no explanation, no variable assignments, and no markdown (no ```python)."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You convert a list of messy human-readable dates into ISO 8601 format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=500
        )
        text = response.choices[0].message.content.strip()
        match = re.search(r"\[(.*?)\]", text, re.DOTALL)
        if match:
            parsed_list = ast.literal_eval("[" + match.group(1) + "]")
        else:
            parsed_list = ast.literal_eval(text)
        return parsed_list
    except Exception as e:
        print(f"❌ GPT error on batch: {e}")
        print("Raw reply:\n", response.choices[0].message.content if 'response' in locals() else "")
        return [None] * len(dates)

# ========= Step 10: Parallel date parsing ==========
def parallel_date_normalization(date_list, batch_size=50, max_workers=32):
    batches = [date_list[i:i + batch_size] for i in range(0, len(date_list), batch_size)]
    normalized = [None] * len(date_list)
    failed_batches = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for idx, batch in enumerate(batches):
            future = executor.submit(normalize_batch_dates, batch)
            futures[future] = idx

        for future in tqdm(as_completed(futures), total=len(futures)):
            idx = futures[future]
            try:
                result = future.result()
                normalized[idx * batch_size : idx * batch_size + len(result)] = result
            except Exception as e:
                print(f"❌ Batch {idx} failed during main thread: {e}")
                failed_batches[idx] = batch

    if failed_batches:
        print(f"\n🔁 Retrying {len(failed_batches)} failed batches (after main run)...")
        for idx, batch in failed_batches.items():
            try:
                result = normalize_batch_dates(batch)
                normalized[idx * batch_size : idx * batch_size + len(result)] = result
                print(f"✅ Retry batch {idx} succeeded")
            except Exception as e:
                print(f"❌ Retry batch {idx} failed again: {e}")
                continue

    return normalized

date_list = df_joined["Date"].tolist()
standardized_dates = parallel_date_normalization(date_list)
df_joined["parsed_date"] = pd.to_datetime(standardized_dates, errors="coerce")

# ========= Step 11: Filter data since 2000 ==========
df_filtered = df_joined[df_joined["parsed_date"].dt.year >= 2000].copy()

# ========= Step 12: Compute cumulative return based on Adj Close ==========
returns = (
    df_filtered
    .sort_values(["Index", "parsed_date"])
    .groupby("Index")
    .agg(
        start_price=("Adj Close", "first"),
        end_price=("Adj Close", "last"),
        country=("region", "first")
    )
    .assign(total_return=lambda x: (x["end_price"] - x["start_price"]))
    .sort_values(by="total_return", ascending=False)
)

print("\n Top 5 indices by return since 2000:")
print(returns[["total_return", "country"]].head(5))
