code = """import json
import pandas as pd
import re

books_path = var_call_0obRIXKOWqtuchR2OVJHvKU7
reviews_path = var_call_IuGPOjM1WdkWZ5XslbM99Ftx
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# helper
import math

def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)$", s)
    return m.group(1) if m else None

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", detail)
    return int(m.group(0)) if m else None

def to_float(x):
    try:
        return float(x)
    except:
        return None

# add fields
if 'book_id' in df_books.columns:
    df_books['id_num'] = df_books['book_id'].apply(extract_num)
else:
    df_books['id_num'] = None

if 'purchase_id' in df_reviews.columns:
    df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_num)
else:
    df_reviews['id_num'] = None

if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

if 'rating' in df_reviews.columns:
    df_reviews['rating_f'] = df_reviews['rating'].apply(to_float)
else:
    df_reviews['rating_f'] = None

merged = pd.merge(df_reviews, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))
merged = merged[merged['rating_f'].notnull()]

per_book = merged.groupby('book_id').agg({'rating_f':'mean','pub_year':'first'}).reset_index().rename(columns={'rating_f':'avg_rating'})
per_book['has_year']=per_book['pub_year'].notnull()

# stats
total_books_with_reviews = per_book.shape[0]
books_with_year = per_book['has_year'].sum()
books_without_year = total_books_with_reviews - books_with_year

# decade breakdown for those with year
per_book_year = per_book[per_book['has_year']]
per_book_year['decade_start'] = (per_book_year['pub_year'].astype(int)//10)*10
per_book_year['decade'] = per_book_year['decade_start'].astype(str) + 's'

decade_counts = per_book_year['decade'].value_counts().to_dict()
decade_avg = per_book_year.groupby('decade')['avg_rating'].mean().round(4).to_dict()

result = {
    'total_books_with_reviews': int(total_books_with_reviews),
    'books_with_pub_year': int(books_with_year),
    'books_without_pub_year': int(books_without_year),
    'decade_counts': decade_counts,
    'decade_avg': decade_avg,
    'sample_per_book_head': per_book_year.sort_values('avg_rating', ascending=False).head(5).to_dict(orient='records')
}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_JzElwp0nBhaFszYaTyRXQASr': ['books_info'], 'var_call_HQx3OeaNbloAEYAsG6o5rLqr': ['review'], 'var_call_0obRIXKOWqtuchR2OVJHvKU7': 'file_storage/call_0obRIXKOWqtuchR2OVJHvKU7.json', 'var_call_IuGPOjM1WdkWZ5XslbM99Ftx': 'file_storage/call_IuGPOjM1WdkWZ5XslbM99Ftx.json', 'var_call_YcBGkBCTgB5McoXe7Wt83vG3': {'decade': None, 'average_rating': None, 'book_count': 0}}

exec(code, env_args)
