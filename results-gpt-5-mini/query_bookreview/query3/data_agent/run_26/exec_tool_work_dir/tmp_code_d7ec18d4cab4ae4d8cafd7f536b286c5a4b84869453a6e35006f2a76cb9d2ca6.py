code = """import json, re, pandas as pd

# Load data from previous query files
with open(var_call_Z6VKobWBdTZKNfTkiWeWX5tN, 'r') as f:
    books = json.load(f)
with open(var_call_1f0HwMQb2lOd8NE2zfG2kTeG, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize books categories: categories field is a string representation of a list
def parse_categories(cat_str):
    try:
        if not cat_str:
            return []
        return json.loads(cat_str)
    except Exception:
        # fallback: try to extract items via regex
        items = re.findall(r"\"(.*?)\"", str(cat_str))
        return items

df_books['categories_list'] = df_books['categories'].apply(parse_categories)

# Identify children's books
df_books['is_children'] = df_books['categories_list'].apply(lambda lst: any("Children" in c or "Children's Books" in c for c in lst))

# Prepare reviews: convert rating to float
# Some ratings may be strings; coerce errors
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id like 'purchaseid_8' -> 'bookid_8'
def purchase_to_bookid(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r"(\d+)$", pid)
    if m:
        return f"bookid_{m.group(1)}"
    # fallback: replace prefix
    return pid.replace('purchase', 'book')

df_reviews['book_id'] = df_reviews['purchase_id'].apply(purchase_to_bookid)

# Join reviews with books on book_id
# Filter reviews with valid numeric rating
df_reviews = df_reviews[df_reviews['rating'].notna()]

# Merge
merged = pd.merge(df_reviews, df_books, on='book_id', how='left', suffixes=('_r','_b'))

# Filter to only books that are children's books
merged_children = merged[merged['is_children'] == True]

# Compute average rating per book (based on reviews from 2020 onwards already filtered at SQL)
group = merged_children.groupby(['book_id','title'], dropna=False).agg(
    avg_rating=('rating', 'mean'),
    review_count=('rating', 'count')
).reset_index()

# Filter avg_rating >= 4.5
result_df = group[group['avg_rating'] >= 4.5].copy()

# Round avg_rating to 3 decimals
result_df['avg_rating'] = result_df['avg_rating'].round(3)

# Sort by avg_rating desc, then review_count desc
result_df = result_df.sort_values(['avg_rating','review_count'], ascending=[False, False])

# Prepare output list of dicts
output = []
for _, row in result_df.iterrows():
    output.append({
        'book_id': row['book_id'],
        'title': row['title'],
        'average_rating': float(row['avg_rating']),
        'review_count': int(row['review_count'])
    })

# Print result in required format as JSON string
print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_Z6VKobWBdTZKNfTkiWeWX5tN': 'file_storage/call_Z6VKobWBdTZKNfTkiWeWX5tN.json', 'var_call_1f0HwMQb2lOd8NE2zfG2kTeG': 'file_storage/call_1f0HwMQb2lOd8NE2zfG2kTeG.json'}

exec(code, env_args)
