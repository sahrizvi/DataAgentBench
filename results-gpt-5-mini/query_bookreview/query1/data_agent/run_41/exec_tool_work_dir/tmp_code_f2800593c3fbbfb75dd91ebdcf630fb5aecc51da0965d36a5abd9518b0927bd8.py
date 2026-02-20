code = """import json
import pandas as pd
import re

# Load query results from storage files (paths provided by previous query_db calls)
books_path = var_call_Qr1wrn5u3pJdKHUVW16Zxfyw
reviews_path = var_call_kA2chKSYy0lWlC7erPBffhZl

books = pd.read_json(books_path)
reviews = pd.read_json(reviews_path)

# Extract numeric id from book_id and purchase_id
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)$", s)
    return int(m.group(1)) if m else None

books['num_id'] = books['book_id'].apply(extract_num_id)
reviews['num_id'] = reviews['purchase_id'].apply(extract_num_id)

# Extract year from details using first 4-digit year between 1500 and 2023
def extract_year(details):
    if not isinstance(details, str):
        return None
    years = re.findall(r"(1[5-9]\d{2}|20\d{2})", details)
    for y in years:
        yi = int(y)
        if 1500 <= yi <= 2023:
            return yi
    return None

books['pub_year'] = books['details'].apply(extract_year)
# Drop rows without num_id or pub_year
books_clean = books.dropna(subset=['num_id','pub_year']).copy()
reviews_clean = reviews.dropna(subset=['num_id','rating']).copy()

# Convert rating to float
reviews_clean['rating'] = pd.to_numeric(reviews_clean['rating'], errors='coerce')
reviews_clean = reviews_clean.dropna(subset=['rating'])

# Compute per-book average rating using num_id
book_avg = reviews_clean.groupby('num_id', as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})

# Merge with books to get pub_year
merged = pd.merge(book_avg, books_clean[['num_id','book_id','pub_year']], on='num_id', how='inner')

# Compute decade string
merged['decade_start'] = (merged['pub_year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# For each decade, consider distinct books count and average of book_avg_rating
decade_grp = merged.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
decade_filtered = decade_grp[decade_grp['num_books'] >= 10]

result = None
if not decade_filtered.empty:
    top = decade_filtered.sort_values(['avg_rating','decade'], ascending=[False,True]).iloc[0]
    result = {'decade': top['decade'], 'average_rating': round(float(top['avg_rating']), 4), 'num_books': int(top['num_books'])}
else:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_qyUusfUYPu9Szcp8NacZlU3R': ['books_info'], 'var_call_GqD2YuyvCINS3TQcNyheqM49': ['review'], 'var_call_Qr1wrn5u3pJdKHUVW16Zxfyw': 'file_storage/call_Qr1wrn5u3pJdKHUVW16Zxfyw.json', 'var_call_kA2chKSYy0lWlC7erPBffhZl': 'file_storage/call_kA2chKSYy0lWlC7erPBffhZl.json'}

exec(code, env_args)
