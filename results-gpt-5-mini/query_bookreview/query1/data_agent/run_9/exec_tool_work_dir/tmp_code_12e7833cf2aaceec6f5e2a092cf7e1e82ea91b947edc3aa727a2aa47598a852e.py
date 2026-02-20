code = """import json
import pandas as pd

# Read previous data
books_path = var_call_Zj8yKwYRbRsCgNcVmijtPaTc
reviews_path = var_call_CpfnhHR6EUPJlSUcPHuAHqvK

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Prepare years and decades, but try alternative parsing: look for 'Published' or 'published' with year near it
import re

def extract_year_extended(text):
    if not isinstance(text, str):
        return None
    # common patterns: 'Published ... on Month Day, YYYY' or 'published on YYYY' or 'first edition on Month Day, YYYY'
    m = re.search(r"(Published|published|published by).*?(\b\d{4}\b)", text)
    if m:
        y = int(m.group(2))
        if 1500 <= y <= 2023:
            return y
    # fallback to any 4-digit year
    years = re.findall(r"\b(\d{4})\b", text)
    for y in years:
        yi = int(y)
        if 1500 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year_extended)
books_df['decade'] = books_df['year'].apply(lambda y: f"{(y//10)*10}s" if pd.notnull(y) else None)

# Map purchase_id to book_id
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

book_avg = reviews_df.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})
merged = pd.merge(book_avg, books_df[['book_id','decade']], on='book_id', how='left')
merged = merged[merged['decade'].notna()]

decade_stats = merged.groupby('decade').agg(num_books=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()
eligible = decade_stats[decade_stats['num_books'] >= 10]

# Output debugging info: show top decades
if eligible.empty:
    out = {'message':'No decade has at least 10 distinct rated books.', 'decade_stats_top5': decade_stats.sort_values('num_books', ascending=False).head(10).to_dict(orient='records')}
else:
    best = eligible.sort_values(['decade_avg_rating','num_books'], ascending=[False,False]).iloc[0]
    out = {'best_decade': best['decade'], 'decade_stats': eligible.to_dict(orient='records')}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_WFM4a4mO1u1oUwDKxN3pHU4v': ['books_info'], 'var_call_Zj8yKwYRbRsCgNcVmijtPaTc': 'file_storage/call_Zj8yKwYRbRsCgNcVmijtPaTc.json', 'var_call_zDjqcyji5fYMtuED9ELxiQ53': ['review'], 'var_call_CpfnhHR6EUPJlSUcPHuAHqvK': 'file_storage/call_CpfnhHR6EUPJlSUcPHuAHqvK.json', 'var_call_bEvlZcJXgqGcNtBZU4xjdEJ6': 'No decade has at least 10 distinct rated books.'}

exec(code, env_args)
