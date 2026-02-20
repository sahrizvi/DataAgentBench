code = """import json
from pathlib import Path
import re
import pandas as pd

books_path = Path(var_call_CUdkO2yEe1cPmTYus0qHCUgo)
reviews_path = Path(var_call_x83zbwbj5mEwvUZg0hsrUepd)

books = json.load(books_path.open('r', encoding='utf-8'))
reviews = json.load(reviews_path.open('r', encoding='utf-8'))

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Improved year extraction: find all 4-digit years in range and pick the last occurrence

def extract_year_last(s):
    if not isinstance(s, str):
        return None
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", s)
    if not years:
        return None
    # pick last
    for y in reversed(years):
        yi = int(y)
        if 1500 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year_last)

# Numeric ids
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

books_df['num'] = books_df['book_id'].apply(extract_num)
reviews_df['num'] = reviews_df['purchase_id'].apply(extract_num)

# Convert rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df[reviews_df['rating'].notna()]

# Merge
merged = pd.merge(reviews_df, books_df[['num','book_id','title','year']], on='num', how='inner')

# Keep only with year
merged = merged[merged['year'].notna()]
merged['year'] = merged['year'].astype(int)

# Decade label
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s")

# Per-book average
book_avg = merged.groupby('num').agg(book_id=('book_id','first'), title=('title','first'), year=('year','first'), decade=('decade','first'), avg_rating=('rating','mean'), n_reviews=('rating','count')).reset_index()

# Per-decade stats
decade_stats = book_avg.groupby('decade').agg(book_count=('num','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# Sort and prepare output
decade_stats = decade_stats.sort_values(by='decade')

# Filter >=10
eligible = decade_stats[decade_stats['book_count']>=10].copy()

result = {
    'total_books_in_books_table': int(len(books_df)),
    'total_reviews_in_review_table': int(len(reviews_df)),
    'books_with_extracted_year': int(books_df['year'].notna().sum()),
    'books_with_reviews_and_year': int(book_avg.shape[0]),
    'decade_stats_all': [],
    'eligible_decades': []
}

for _,row in decade_stats.iterrows():
    result['decade_stats_all'].append({'decade': row['decade'], 'book_count': int(row['book_count']), 'decade_avg_rating': round(float(row['decade_avg_rating']),4)})

for _,row in eligible.iterrows():
    result['eligible_decades'].append({'decade': row['decade'], 'book_count': int(row['book_count']), 'decade_avg_rating': round(float(row['decade_avg_rating']),4)})

if not eligible.empty:
    best = eligible.sort_values(by=['decade_avg_rating','book_count'], ascending=[False,False]).iloc[0]
    result['best_decade'] = {'decade': best['decade'], 'book_count': int(best['book_count']), 'average_rating': round(float(best['decade_avg_rating']),4)}
else:
    result['best_decade'] = None

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_t8ICoTdZa5hhfV8cD7hQJlQf': ['books_info'], 'var_call_CUdkO2yEe1cPmTYus0qHCUgo': 'file_storage/call_CUdkO2yEe1cPmTYus0qHCUgo.json', 'var_call_GRCXW9zYHtaqYli2lmJg1NBh': ['review'], 'var_call_x83zbwbj5mEwvUZg0hsrUepd': 'file_storage/call_x83zbwbj5mEwvUZg0hsrUepd.json', 'var_call_pWym9YvF1umLsL0l4XXJaoQ8': {'best_decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_ZmhAUewJuPHzFH1v3EarTie1': {'num_books': 200, 'num_reviews': 1833, 'unique_book_nums': 200, 'unique_review_nums': 200, 'intersection_count': 200, 'intersection_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'full_string_intersection_count': 0, 'full_string_intersection_sample': []}}

exec(code, env_args)
