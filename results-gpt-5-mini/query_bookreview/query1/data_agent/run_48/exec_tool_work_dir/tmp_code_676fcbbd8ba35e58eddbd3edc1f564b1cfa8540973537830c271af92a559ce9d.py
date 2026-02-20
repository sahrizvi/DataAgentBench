code = """import json
import pandas as pd
import re

# Load the JSON results from the stored file paths
books_path = var_call_u47Br4No7IXo4KjFR64IViwc
reviews_path = var_call_1bRBHR5BOUPXuGhMNNeh7fdh

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize ids by extracting numeric part
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

books_df['num_id'] = books_df['book_id'].apply(extract_num_id)
reviews_df['num_id'] = reviews_df['purchase_id'].apply(extract_num_id)

# Convert rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating','num_id'])

# Compute per-book average rating
book_avg = reviews_df.groupby('num_id', as_index=False)['rating'].mean().rename(columns={'rating':'avg_rating'})

# Merge with books to get details and extract year
merged = pd.merge(book_avg, books_df[['num_id','details']], on='num_id', how='left')

# Extract year from details
def extract_year(s):
    if not isinstance(s, str):
        return None
    years = re.findall(r"(1[0-9]{3}|20[0-9]{2})", s)
    if years:
        # choose the first plausible year <= 2023
        for y in years:
            try:
                yi = int(y)
                if 1000 <= yi <= 2023:
                    return yi
            except:
                continue
    return None

merged['year'] = merged['details'].apply(extract_year)
# Drop if no year
merged = merged.dropna(subset=['year'])
merged['year'] = merged['year'].astype(int)

# Compute decade label
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(str) + 's'

# For each decade, count distinct books and compute average of per-book avg_rating
decade_stats = merged.groupby('decade').agg(
    num_books = ('num_id', 'nunique'),
    decade_avg_rating = ('avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10]

if eligible.empty:
    result = None
else:
    # Find decade with highest average rating
    best = eligible.sort_values(['decade_avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['decade_avg_rating']), 4),
        'num_books': int(best['num_books'])
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_G1CY9kxyW2THGHHF8Dxn8DZE': ['books_info'], 'var_call_Nhk4bAUavPquFrXsrhaO43Ej': ['review'], 'var_call_u47Br4No7IXo4KjFR64IViwc': 'file_storage/call_u47Br4No7IXo4KjFR64IViwc.json', 'var_call_1bRBHR5BOUPXuGhMNNeh7fdh': 'file_storage/call_1bRBHR5BOUPXuGhMNNeh7fdh.json'}

exec(code, env_args)
