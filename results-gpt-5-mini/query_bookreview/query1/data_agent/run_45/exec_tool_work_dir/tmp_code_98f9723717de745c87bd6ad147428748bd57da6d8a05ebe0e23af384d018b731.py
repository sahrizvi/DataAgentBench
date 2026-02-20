code = """import json
import pandas as pd
import re

# Load data from storage-provided file paths
books_path = var_call_wH00EPDFUiIvhWtUqMwNbWGK
reviews_path = var_call_fuCn8CSsx6oKvAusBKg4fr63

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize column names
# Ensure rating numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Map purchase_id -> book_id by replacing prefix
if 'purchase_id' in reviews_df.columns:
    reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace(r'^purchaseid_', 'bookid_', regex=True)
else:
    reviews_df['book_id'] = reviews_df['purchaseid'].astype(str).str.replace(r'^purchaseid_', 'bookid_', regex=True)

# Extract publication year from books_df.details
def extract_year(text):
    if not isinstance(text, str):
        return None
    # find first 4-digit year between 1000 and 2099
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)
    return int(m.group(0)) if m else None

books_df['pub_year'] = books_df['details'].apply(extract_year)

# Merge reviews with books on book_id
merged = pd.merge(reviews_df, books_df[['book_id','pub_year']], on='book_id', how='left')

# Drop reviews with no pub_year or no rating
merged = merged.dropna(subset=['pub_year','rating'])
merged['pub_year'] = merged['pub_year'].astype(int)

# Compute decade label
merged['decade_start'] = (merged['pub_year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(str) + 's'

# Compute average rating per book
book_avg = merged.groupby('book_id', as_index=False).agg({'rating':'mean','decade':'first'})
book_avg.rename(columns={'rating':'book_avg_rating'}, inplace=True)

# Compute per-decade stats
decade_stats = book_avg.groupby('decade').agg(
    num_books=('book_id','count'),
    decade_avg_rating=('book_avg_rating','mean')
).reset_index()

# Filter decades with at least 10 distinct books
candidate = decade_stats[decade_stats['num_books']>=10]

if candidate.empty:
    result = {'decade': None, 'message': 'No decade has at least 10 distinct rated books.'}
else:
    # Find decade with highest average rating; if tie pick the one with more books, then smallest decade
    candidate = candidate.sort_values(by=['decade_avg_rating','num_books','decade'], ascending=[False,False,True])
    top = candidate.iloc[0]
    result = {
        'decade': top['decade'],
        'avg_rating': round(float(top['decade_avg_rating']),4),
        'num_books': int(top['num_books'])
    }

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_hYj2f4ihOCmY2CwwoO1oPSrX': ['books_info'], 'var_call_JEoJLHZUSLttAcyopVaAXzDv': ['review'], 'var_call_MUjcCZjRiSwY51uNeUBjNb1S': 'file_storage/call_MUjcCZjRiSwY51uNeUBjNb1S.json', 'var_call_wH00EPDFUiIvhWtUqMwNbWGK': 'file_storage/call_wH00EPDFUiIvhWtUqMwNbWGK.json', 'var_call_fuCn8CSsx6oKvAusBKg4fr63': 'file_storage/call_fuCn8CSsx6oKvAusBKg4fr63.json'}

exec(code, env_args)
