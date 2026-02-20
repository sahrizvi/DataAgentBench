code = """import json
import pandas as pd
import ast

# Load data from storage files
with open(var_call_BlkXgYzlPUK5Xm2iMx0eGmTl, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_ZFE2SIRbVjlDhcX52cFyoZVi, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize books categories: parse string representation to list where possible
def parse_categories(cat_str):
    try:
        parsed = ast.literal_eval(cat_str)
        if isinstance(parsed, list):
            return parsed
        return [str(parsed)]
    except Exception:
        # fallback: simple substring check
        return [cat_str]

books_df['categories_list'] = books_df['categories'].fillna('[]').apply(parse_categories)

# Filter books that have "Children's Books" in categories
children_books_df = books_df[books_df['categories_list'].apply(lambda lst: any("Children's Books" == c for c in lst))].copy()

# Prepare reviews: convert rating to numeric and map purchase_id to book_id by replacing prefix
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating'])

# Map purchaseid to bookid by replacing 'purchaseid_' with 'bookid_'
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Aggregate reviews from 2020 onwards (query already filtered) by book_id
agg = reviews_df.groupby('book_id').rating.agg(['mean', 'count']).reset_index()
agg = agg.rename(columns={'mean': 'avg_rating', 'count': 'review_count'})

# Merge with children books
merged = pd.merge(children_books_df, agg, on='book_id', how='inner')

# Filter avg_rating >= 4.5
result_df = merged[merged['avg_rating'] >= 4.5].copy()

# Prepare output list
output = []
for _, row in result_df.iterrows():
    output.append({
        'book_id': row['book_id'],
        'title': row['title'],
        'avg_rating': round(float(row['avg_rating']), 3),
        'review_count': int(row['review_count'])
    })

# Sort by avg_rating desc then review_count desc
output = sorted(output, key=lambda x: (-x['avg_rating'], -x['review_count']))

import json
print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_8nplIdIWXafd9QugusODViWI': ['books_info'], 'var_call_BlkXgYzlPUK5Xm2iMx0eGmTl': 'file_storage/call_BlkXgYzlPUK5Xm2iMx0eGmTl.json', 'var_call_laHanQeGmmZx61dKbabJRxex': ['review'], 'var_call_ZFE2SIRbVjlDhcX52cFyoZVi': 'file_storage/call_ZFE2SIRbVjlDhcX52cFyoZVi.json'}

exec(code, env_args)
