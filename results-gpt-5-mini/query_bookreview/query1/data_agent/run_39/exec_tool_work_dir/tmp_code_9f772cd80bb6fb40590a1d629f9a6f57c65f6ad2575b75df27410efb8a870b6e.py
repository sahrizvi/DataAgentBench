code = """import json
import re
import pandas as pd

with open(var_call_wH4Hl9v9HJaphYQUk8Ctw6wN, 'r', encoding='utf-8') as f:
    review_aggs = json.load(f)
with open(var_call_V6AnT36wTL1cNBXWgaG8OkF5, 'r', encoding='utf-8') as f:
    books = json.load(f)

# DataFrames
rev = pd.DataFrame(review_aggs)
books_df = pd.DataFrame(books)
rev['avg_rating'] = rev['avg_rating'].astype(float)

# mapping function
rev['book_id'] = rev['purchase_id'].str.replace('purchaseid_','bookid_')

# year extraction
import re

def extract_year(details):
    if not isinstance(details, str):
        return None
    m = re.search(r'Published[^\d]{0,50}(\d{4})', details, flags=re.I)
    if m:
        y = int(m.group(1));
        if 1500 <= y <= 2023:
            return y
    m2 = re.search(r'on\s+([A-Za-z]+\s+\d{1,2},\s*(\d{4}))', details)
    if m2:
        y = int(m2.group(2));
        if 1500 <= y <= 2023:
            return y
    allyears = re.findall(r'\b(\d{4})\b', details)
    for ys in allyears:
        y = int(ys)
        if 1500 <= y <= 2023:
            return y
    return None

books_df['year'] = books_df['details'].apply(extract_year)

merged = pd.merge(rev, books_df[['book_id','title','year']], on='book_id', how='inner')
merged = merged[merged['year'].notna()].copy()
merged['year'] = merged['year'].astype(int)
merged['decade'] = (merged['year']//10*10).astype(str) + 's'

books_per_decade = merged.groupby('decade').agg(
    num_books=('book_id', lambda x: x.nunique()),
    avg_rating=('avg_rating', 'mean')
).reset_index()

eligible = books_per_decade[books_per_decade['num_books']>=10].copy()

out = {
    'total_merged_rows': len(merged),
    'unique_books_in_merged': int(merged['book_id'].nunique()),
    'books_per_decade': books_per_decade.to_dict(orient='records'),
    'eligible_decades': eligible.to_dict(orient='records')
}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_wH4Hl9v9HJaphYQUk8Ctw6wN': 'file_storage/call_wH4Hl9v9HJaphYQUk8Ctw6wN.json', 'var_call_ZhDl5Ukh9lwtVtRdoSBT8Bw7': ['books_info'], 'var_call_V6AnT36wTL1cNBXWgaG8OkF5': 'file_storage/call_V6AnT36wTL1cNBXWgaG8OkF5.json', 'var_call_tdSaWQFbILWpnlONCyDjnNTn': {'decade': None, 'avg_rating': None, 'num_books': 0}}

exec(code, env_args)
