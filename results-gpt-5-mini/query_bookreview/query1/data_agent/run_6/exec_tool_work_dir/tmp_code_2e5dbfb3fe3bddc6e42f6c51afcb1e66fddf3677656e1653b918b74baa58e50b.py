code = """import json
import re
from pathlib import Path
import pandas as pd

# Load data from storage files
books_path = Path(var_call_CUdkO2yEe1cPmTYus0qHCUgo)
reviews_path = Path(var_call_x83zbwbj5mEwvUZg0hsrUepd)

with books_path.open('r', encoding='utf-8') as f:
    books = json.load(f)
with reviews_path.open('r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract numeric id from book_id and purchase_id
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)', s)
    return int(m.group(1)) if m else None

books_df['num_id'] = books_df['book_id'].apply(extract_num_id)
reviews_df['num_id'] = reviews_df['purchase_id'].apply(extract_num_id)

# Extract year from details field in books
def extract_year(s):
    if not isinstance(s, str):
        return None
    # find all 4-digit numbers between 1500 and 2023
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", s)
    if not years:
        return None
    # years are strings; pick first that is in a reasonable range
    for y in years:
        try:
            yi = int(y)
        except:
            continue
        if 1500 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year)

# Drop books without numeric id or year
books_df = books_df[books_df['num_id'].notna()]

# Convert ratings to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df[reviews_df['rating'].notna()]

# Merge reviews with books on numeric id
merged = pd.merge(reviews_df, books_df[['num_id','book_id','title','year']], on='num_id', how='inner')

# Keep only entries with a valid year
merged = merged[merged['year'].notna()]
merged['year'] = merged['year'].astype(int)

# Compute decade label
def decade_label(y):
    start = (y // 10) * 10
    return f"{start}s"

merged['decade'] = merged['year'].apply(decade_label)

# Compute per-book average rating
book_avg = merged.groupby('num_id').agg(book_id=('book_id','first'), title=('title','first'), year=('year','first'), decade=('decade','first'), avg_rating=('rating','mean')).reset_index()

# Compute per-decade stats: number of distinct books and average of book averages
decade_stats = book_avg.groupby('decade').agg(book_count=('num_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10]

if eligible.empty:
    result = {"best_decade": None, "average_rating": None, "book_count": 0}
else:
    # Choose decade with highest average rating; in case of tie, choose highest average then highest book_count then earliest decade
    eligible_sorted = eligible.sort_values(by=['decade_avg_rating','book_count','decade'], ascending=[False, False, True])
    best = eligible_sorted.iloc[0]
    result = {"best_decade": best['decade'], "average_rating": round(float(best['decade_avg_rating']), 4), "book_count": int(best['book_count'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_t8ICoTdZa5hhfV8cD7hQJlQf': ['books_info'], 'var_call_CUdkO2yEe1cPmTYus0qHCUgo': 'file_storage/call_CUdkO2yEe1cPmTYus0qHCUgo.json', 'var_call_GRCXW9zYHtaqYli2lmJg1NBh': ['review'], 'var_call_x83zbwbj5mEwvUZg0hsrUepd': 'file_storage/call_x83zbwbj5mEwvUZg0hsrUepd.json'}

exec(code, env_args)
