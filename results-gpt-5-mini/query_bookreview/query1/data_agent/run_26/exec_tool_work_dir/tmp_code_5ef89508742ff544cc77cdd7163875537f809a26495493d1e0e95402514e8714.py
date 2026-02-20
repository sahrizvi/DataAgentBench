code = """import json
import pandas as pd
import re

# Load data from storage variables (file paths or lists)
books_path_or_list = var_call_t7VeWsSJrFNRbp3btXYScz0k
reviews_path_or_list = var_call_6rktXsfDLiZ87C4uCukITp3G

def load(obj):
    if isinstance(obj, str):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

books = load(books_path_or_list)
reviews = load(reviews_path_or_list)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize reviews: rating to float, map purchase_id to book_id
reviews_df = reviews_df.dropna(subset=['purchase_id', 'rating'])
reviews_df['rating'] = reviews_df['rating'].astype(float)
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Compute per-book average rating
book_avg = reviews_df.groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating': 'book_avg'})

# Extract year from books.details
year_pattern = re.compile(r"\b(1[5-9]\d{2}|20[0-2]\d|2023)\b")

def extract_year(text):
    if not isinstance(text, str):
        return None
    m = year_pattern.search(text)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# Keep only books with a year
books_df = books_df.dropna(subset=['book_id', 'year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade'] = (books_df['year'] // 10 * 10).astype(int).astype(str) + 's'

# Merge book averages with books to get decade
merged = pd.merge(book_avg, books_df[['book_id', 'year', 'decade']], on='book_id', how='inner')

# For each decade, consider distinct books (we have one row per book)
decade_stats = merged.groupby('decade').agg(book_count=('book_id', 'nunique'), average_rating=('book_avg', 'mean')).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['book_count'] >= 10]

if decade_stats_filtered.empty:
    result = {'decade': None, 'average_rating': None, 'book_count': 0}
else:
    # Find decade with highest average_rating
    top = decade_stats_filtered.sort_values(['average_rating', 'decade'], ascending=[False, True]).iloc[0]
    result = {'decade': top['decade'], 'average_rating': round(float(top['average_rating']), 4), 'book_count': int(top['book_count'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_vR1GXsw3kIrYIyz9jmBbvc5r': ['books_info'], 'var_call_t7VeWsSJrFNRbp3btXYScz0k': 'file_storage/call_t7VeWsSJrFNRbp3btXYScz0k.json', 'var_call_PryAUKaLiRTCavMor8iE9hgw': ['review'], 'var_call_6rktXsfDLiZ87C4uCukITp3G': 'file_storage/call_6rktXsfDLiZ87C4uCukITp3G.json'}

exec(code, env_args)
