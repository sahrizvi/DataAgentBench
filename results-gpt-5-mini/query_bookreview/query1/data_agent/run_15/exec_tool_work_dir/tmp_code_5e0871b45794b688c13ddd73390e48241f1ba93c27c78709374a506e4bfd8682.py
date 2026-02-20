code = """import pandas as pd
import json
import re

# Load data from previous query results stored as file paths
books_path = var_call_uVomxWXnBiyFdnKb2u6ckbGO
reviews_path = var_call_28kcxWuiIJTTzQDKBZFG2Th7

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract numeric id suffix from book_id and purchase_id
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)$", s)
    return int(m.group(1)) if m else None

books_df['id_num'] = books_df['book_id'].apply(extract_num)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_num)

# Extract year from details field using regex (first occurrence of 4-digit year between 1000 and 2023)
def extract_year(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(1[0-9]{3}|20[0-2][0-9]|2023)", s)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# Drop books without year or id_num
books_df = books_df.dropna(subset=['id_num','year']).copy()
books_df['id_num'] = books_df['id_num'].astype(int)
books_df['year'] = books_df['year'].astype(int)

# Normalize ratings to float
reviews_df = reviews_df.dropna(subset=['id_num','rating']).copy()
# rating may be string; convert
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating']).copy()
reviews_df['id_num'] = reviews_df['id_num'].astype(int)

# Merge reviews with books on id_num
merged = reviews_df.merge(books_df[['id_num','book_id','title','year']], on='id_num', how='inner')

# Compute book-level average ratings
book_avg = merged.groupby(['id_num','book_id','title','year'], as_index=False)['rating'].mean()
book_avg.rename(columns={'rating':'book_avg_rating'}, inplace=True)

# Compute decade label
book_avg['decade_start'] = (book_avg['year'] // 10) * 10
book_avg['decade'] = book_avg['decade_start'].astype(str) + 's'

# For each decade with at least 10 distinct books that have been rated, compute average of book_avg_rating
decade_stats = book_avg.groupby('decade').agg(
    book_count=('book_id','nunique'),
    avg_of_book_avg=('book_avg_rating','mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10].copy()

result = None
if not eligible.empty:
    # find decade with highest avg_of_book_avg
    best = eligible.sort_values(['avg_of_book_avg','book_count'], ascending=[False, False]).iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['avg_of_book_avg']), 4),
        'book_count': int(best['book_count'])
    }
else:
    result = {'decade': None, 'average_rating': None, 'book_count': 0, 'note': 'No decade has at least 10 distinct rated books.'}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_kEBp9ISZlmWo4T0V62iuHFre': ['books_info'], 'var_call_uVomxWXnBiyFdnKb2u6ckbGO': 'file_storage/call_uVomxWXnBiyFdnKb2u6ckbGO.json', 'var_call_28kcxWuiIJTTzQDKBZFG2Th7': 'file_storage/call_28kcxWuiIJTTzQDKBZFG2Th7.json'}

exec(code, env_args)
