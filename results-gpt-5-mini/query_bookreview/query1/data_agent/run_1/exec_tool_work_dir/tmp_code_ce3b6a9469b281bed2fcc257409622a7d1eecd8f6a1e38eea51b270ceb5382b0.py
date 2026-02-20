code = """import json
import pandas as pd
import re

books_path = var_call_mgh9ob5dcKUeDO89uHrr4IUc
reviews_path = var_call_8c7MOoJAmwZLvXCKT3ZbfT1q

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df[reviews_df['rating'].notnull()].copy()
reviews_df['book_id'] = reviews_df['purchase_id'].str.replace('purchaseid_', 'bookid_')

book_ratings = reviews_df.groupby('book_id')['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})
merged = pd.merge(book_ratings, books_df[['book_id','details']], on='book_id', how='left')

def extract_year(s):
    if not isinstance(s, str):
        return None
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", s)
    if not years:
        return None
    years_int = [int(y) for y in years if 1500 <= int(y) <= 2023]
    if not years_int:
        return None
    return min(years_int)

merged['year'] = merged['details'].apply(extract_year)
merged['year_count'] = merged['year'].notnull().astype(int)
merged_with_year = merged[merged['year'].notnull()].copy()
merged_with_year['year'] = merged_with_year['year'].astype(int)
merged_with_year['decade'] = merged_with_year['year'].floordiv(10).mul(10).astype(int).astype(str) + 's'

decade_stats_all = merged_with_year.groupby('decade').agg(book_count=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

top_decades = decade_stats_all.sort_values(by='decade_avg_rating', ascending=False).head(10)

# prepare sample merged rows
sample_rows = merged_with_year[['book_id','avg_rating','year','decade','details']].head(20).to_dict(orient='records')

out = {
    'total_books_in_books_table': int(books_df['book_id'].nunique()),
    'distinct_books_with_reviews': int(book_ratings['book_id'].nunique()),
    'books_with_extracted_year': int(merged_with_year['book_id'].nunique()),
    'decade_stats_all': decade_stats_all.sort_values('decade').to_dict(orient='records'),
    'top_decades_by_avg_rating': top_decades.to_dict(orient='records'),
    'sample_merged_rows': sample_rows
}

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_olewwEUuShxXJ2uEYtMawO89': ['books_info'], 'var_call_ZzgS1iTAYTwhiKjy61oq2Gth': ['review'], 'var_call_mgh9ob5dcKUeDO89uHrr4IUc': 'file_storage/call_mgh9ob5dcKUeDO89uHrr4IUc.json', 'var_call_8c7MOoJAmwZLvXCKT3ZbfT1q': 'file_storage/call_8c7MOoJAmwZLvXCKT3ZbfT1q.json', 'var_call_jeKqTvUuTNXBzAEGT5b0ML0R': None}

exec(code, env_args)
