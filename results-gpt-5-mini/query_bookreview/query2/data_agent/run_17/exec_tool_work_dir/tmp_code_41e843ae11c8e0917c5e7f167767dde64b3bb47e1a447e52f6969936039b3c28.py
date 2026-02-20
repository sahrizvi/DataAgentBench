code = """import json
import pandas as pd
import re

# Load data from previous tool calls (file paths are stored in these variables)
with open(var_call_0cIb3EK6wol2WEIiaHje0VuX, 'r') as f:
    books = json.load(f)
with open(var_call_ab0SKVov12g0SYFmKLZcETHB, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure rating is numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id -> book_id by replacing prefix
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace(r'^purchaseid_', 'bookid_', regex=True)

# Compute average rating per book_id
avg = df_reviews.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

# Merge with books
merged = pd.merge(df_books, avg, on='book_id', how='inner')

# Filter for Literature & Fiction category and English language in details
def contains_lit(cat):
    try:
        return 'literature & fiction' in cat.lower()
    except:
        return False

def contains_english(det):
    try:
        return 'english' in det.lower()
    except:
        return False

mask = merged['categories'].apply(contains_lit) & merged['details'].apply(contains_english)
filtered = merged[mask].copy()

# Select those with perfect average rating 5.0 (allow tiny float tolerance)
filtered['avg_rating'] = pd.to_numeric(filtered['avg_rating'], errors='coerce')
perfect = filtered[(filtered['avg_rating'] >= 4.999999) & (filtered['avg_rating'] <= 5.0)]

# Prepare result list of dicts
result = []
for _, row in perfect.iterrows():
    result.append({
        'book_id': row.get('book_id'),
        'title': row.get('title'),
        'categories': row.get('categories'),
        'details': row.get('details'),
        'avg_rating': float(row.get('avg_rating')) if pd.notna(row.get('avg_rating')) else None
    })

# Print in required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_LCpS4rVWxnNDVLkM6bk71FHL': ['books_info'], 'var_call_0cIb3EK6wol2WEIiaHje0VuX': 'file_storage/call_0cIb3EK6wol2WEIiaHje0VuX.json', 'var_call_qAo2Yae19LFdNUZ5UpjNo5AH': ['review'], 'var_call_ab0SKVov12g0SYFmKLZcETHB': 'file_storage/call_ab0SKVov12g0SYFmKLZcETHB.json'}

exec(code, env_args)
