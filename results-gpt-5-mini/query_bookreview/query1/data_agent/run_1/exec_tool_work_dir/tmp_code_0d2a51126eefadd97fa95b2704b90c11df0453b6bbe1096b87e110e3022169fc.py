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

# New extraction without word boundaries
def extract_year_simple(s):
    if not isinstance(s, str):
        return None
    years = re.findall(r"(1[5-9]\d{2}|20\d{2})", s)
    years_int = [int(y) for y in years if 1500 <= int(y) <= 2023]
    if not years_int:
        return None
    return min(years_int)

merged['year'] = merged['details'].apply(extract_year_simple)
merged_with_year = merged[merged['year'].notnull()].copy()
merged_with_year['year'] = merged_with_year['year'].astype(int)
merged_with_year['decade'] = merged_with_year['year'].floordiv(10).mul(10).astype(int).astype(str) + 's'

decade_stats = merged_with_year.groupby('decade').agg(book_count=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()
# filter >=10
decade_stats_filtered = decade_stats[decade_stats['book_count'] >= 10].copy()

result = None
if not decade_stats_filtered.empty:
    best = decade_stats_filtered.sort_values(by=['decade_avg_rating','book_count','decade'], ascending=[False, False, True]).iloc[0]
    result = {'decade': best['decade'], 'average_rating': round(float(best['decade_avg_rating']),4), 'book_count': int(best['book_count'])}
else:
    result = None

out = {
    'result': result,
    'total_books': int(books_df['book_id'].nunique()),
    'distinct_books_with_reviews': int(book_ratings['book_id'].nunique()),
    'books_with_extracted_year': int(merged_with_year['book_id'].nunique()),
    'decade_stats': decade_stats.sort_values('decade').to_dict(orient='records')
}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_olewwEUuShxXJ2uEYtMawO89': ['books_info'], 'var_call_ZzgS1iTAYTwhiKjy61oq2Gth': ['review'], 'var_call_mgh9ob5dcKUeDO89uHrr4IUc': 'file_storage/call_mgh9ob5dcKUeDO89uHrr4IUc.json', 'var_call_8c7MOoJAmwZLvXCKT3ZbfT1q': 'file_storage/call_8c7MOoJAmwZLvXCKT3ZbfT1q.json', 'var_call_jeKqTvUuTNXBzAEGT5b0ML0R': None, 'var_call_ZYxxwl4ZTj5qv08wj86TlRqN': {'total_books_in_books_table': 200, 'distinct_books_with_reviews': 200, 'books_with_extracted_year': 0, 'decade_stats_all': [], 'top_decades_by_avg_rating': [], 'sample_merged_rows': []}, 'var_call_Dnw1YOiED7zod6bPJ9AOFOVX': 'file_storage/call_Dnw1YOiED7zod6bPJ9AOFOVX.json', 'var_call_Ivy8n4sBV2yk98hVQhPjvmf7': 'file_storage/call_Ivy8n4sBV2yk98hVQhPjvmf7.json', 'var_call_uof6h1jRwY18ziZ3QU81wrHi': {'book_id': 'bookid_1', 'details_repr': "'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'"}}

exec(code, env_args)
