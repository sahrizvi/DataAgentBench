code = """import json
import pandas as pd
import re

with open(var_call_nIZtqYm1WnlSxW3jofWcK6ID, 'r') as f:
    books = json.load(f)
with open(var_call_yhdg6aG3UawDmz5sv6LZzVf5, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# basic stats
total_reviews = len(df_reviews)
unique_review_books = df_reviews['purchase_id'].nunique() if 'purchase_id' in df_reviews.columns else 0

# clean ratings
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# normalize ids
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# extract pub_year similar to before

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    matches = re.findall(r"\b(1[5-9][0-9]{2}|20[0-2][0-9]|2023)\b", detail)
    for m in matches:
        try:
            y = int(m)
            if 1500 <= y <= 2023:
                return y
        except:
            continue
    return None

if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

total_books = len(df_books)
books_with_pubyear = df_books['pub_year'].notna().sum()

# compute mean rating per book
book_mean = df_reviews.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'mean_rating'})
unique_books_with_rating = len(book_mean)

# merge
merged = pd.merge(book_mean, df_books[['book_id','pub_year']], on='book_id', how='left')
matched_with_pubyear = merged['pub_year'].notna().sum()

# compute decade groups
merged = merged[merged['pub_year'].notna()].copy()
merged['pub_year'] = merged['pub_year'].astype(int)
merged['decade'] = merged['pub_year'].apply(lambda y: f"{(y//10)*10}s")

decade_grp = merged.groupby('decade').agg(book_count=('book_id','nunique'), avg_book_rating=('mean_rating','mean')).reset_index()

decade_list = decade_grp.sort_values('decade').to_dict(orient='records')

out = {
    'total_reviews': int(total_reviews),
    'unique_review_books': int(unique_review_books),
    'total_books': int(total_books),
    'books_with_pubyear': int(books_with_pubyear),
    'unique_books_with_rating': int(unique_books_with_rating),
    'matched_with_pubyear': int(matched_with_pubyear),
    'decades': decade_list
}

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_WjxSnom9ZZcw1f2zfM8y68hn': ['books_info'], 'var_call_Qgq3KUZEryaZofz9J0cBHUJB': ['review'], 'var_call_NVoEnkMvFVyDYFIhkNKQFyML': 'file_storage/call_NVoEnkMvFVyDYFIhkNKQFyML.json', 'var_call_yhdg6aG3UawDmz5sv6LZzVf5': 'file_storage/call_yhdg6aG3UawDmz5sv6LZzVf5.json', 'var_call_UIXpxuBL5mV0zLs0iHxlnjQu': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'var_call_nIZtqYm1WnlSxW3jofWcK6ID': 'file_storage/call_nIZtqYm1WnlSxW3jofWcK6ID.json', 'var_call_2Ajd2K3gfeO0QAv9ozU1eszn': {'decade': None, 'avg_rating': None, 'book_count': 0}}

exec(code, env_args)
