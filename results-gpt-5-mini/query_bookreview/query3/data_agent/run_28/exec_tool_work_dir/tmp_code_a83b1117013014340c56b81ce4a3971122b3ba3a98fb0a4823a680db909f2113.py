code = """import json
import pandas as pd

# Load the query results from storage files
with open(var_call_R1Orz97CQZvTtZdNM5N0NWcG, 'r') as f:
    books_data = json.load(f)
with open(var_call_pcHGhCdMt2oBt8X4ytx0zA2j, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Normalize review fields
# Ensure rating numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Parse review_time
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'], errors='coerce')
# Filter reviews from 2020-01-01 onwards
df_reviews = df_reviews[df_reviews['review_time'] >= pd.to_datetime('2020-01-01')]

# Extract numeric id suffix from book_id and purchase_id
# e.g., bookid_4 -> 4, purchaseid_4 -> 4
import re

def extract_suffix(x):
    if pd.isna(x):
        return None
    m = re.search(r"_(\d+)$", str(x))
    return m.group(1) if m else None

if 'book_id' in df_books.columns:
    df_books['id'] = df_books['book_id'].apply(extract_suffix)
else:
    df_books['id'] = None

if 'purchase_id' in df_reviews.columns:
    df_reviews['id'] = df_reviews['purchase_id'].apply(extract_suffix)
else:
    df_reviews['id'] = None

# Merge reviews with books on the extracted id
merged = pd.merge(df_reviews, df_books, on='id', how='inner', suffixes=('_rev', '_book'))

# Identify Children's Books from books' categories field
def is_childrens(cat_str):
    if pd.isna(cat_str):
        return False
    # Try to parse as JSON list
    try:
        parsed = json.loads(cat_str)
        if isinstance(parsed, list):
            for c in parsed:
                if "children" in str(c).lower():
                    return True
    except Exception:
        pass
    # Fallback substring check
    if "children" in str(cat_str).lower():
        return True
    return False

merged['is_childrens'] = merged['categories'].apply(is_childrens)

# Keep only children's books
childrens = merged[merged['is_childrens']]

# Group by book (use book_id and title) and compute average rating and count based only on filtered reviews
grouped = childrens.groupby(['book_id', 'title'], dropna=False).agg(
    avg_rating=('rating', 'mean'),
    num_reviews=('rating', 'count')
).reset_index()

# Filter for avg_rating >= 4.5
result_df = grouped[grouped['avg_rating'] >= 4.5].copy()

# Round avg_rating to 3 decimals
result_df['avg_rating'] = result_df['avg_rating'].round(3)

# Prepare final list
result_list = []
for _, row in result_df.sort_values(by=['avg_rating','num_reviews'], ascending=[False, False]).iterrows():
    result_list.append({
        'title': row['title'],
        'book_id': row['book_id'],
        'average_rating': float(row['avg_rating']),
        'review_count_since_2020': int(row['num_reviews'])
    })

# Print result in required format
print("__RESULT__:")
print(json.dumps(result_list))"""

env_args = {'var_call_2oSIe3HQKBmwmgmxyoQJ8axd': ['books_info'], 'var_call_R1Orz97CQZvTtZdNM5N0NWcG': 'file_storage/call_R1Orz97CQZvTtZdNM5N0NWcG.json', 'var_call_9hPu6dpFIVkloRdm7E7w1Mc9': ['review'], 'var_call_pcHGhCdMt2oBt8X4ytx0zA2j': 'file_storage/call_pcHGhCdMt2oBt8X4ytx0zA2j.json'}

exec(code, env_args)
