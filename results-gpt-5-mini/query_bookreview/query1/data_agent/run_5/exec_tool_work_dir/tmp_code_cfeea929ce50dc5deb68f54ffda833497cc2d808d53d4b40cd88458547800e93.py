code = """import json
import pandas as pd
import re

# Load books data
books_data = None
if isinstance(var_call_nBsb3bz8kItIWn2tWw4QfEnd, str):
    with open(var_call_nBsb3bz8kItIWn2tWw4QfEnd, 'r', encoding='utf-8') as f:
        books_data = json.load(f)
else:
    books_data = var_call_nBsb3bz8kItIWn2tWw4QfEnd

# Load reviews data
reviews_data = None
if isinstance(var_call_71BLhMQ8VRq1OQ55Ls0BOjbF, str):
    with open(var_call_71BLhMQ8VRq1OQ55Ls0BOjbF, 'r', encoding='utf-8') as f:
        reviews_data = json.load(f)
else:
    reviews_data = var_call_71BLhMQ8VRq1OQ55Ls0BOjbF

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Clean ratings
reviews_df = reviews_df.dropna(subset=['rating', 'purchase_id'])
# Some ratings may be strings; convert
reviews_df['rating'] = reviews_df['rating'].astype(float)

# Map purchase_id -> book_id by replacing prefix
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace(r'^purchaseid_', 'bookid_', regex=True)

# Extract year from books details
year_regex = re.compile(r"\b(1[0-9]{3}|20[0-1][0-9]|202[0-3])\b")

def extract_year(details):
    if not isinstance(details, str):
        return None
    m = year_regex.search(details)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)

# Build book-level average ratings for books that have a year
# First, get reviews joined to books by book_id
# But ensure we only consider reviews that map to an existing book
books_with_year = books_df.dropna(subset=['year'])[['book_id','year']].drop_duplicates()

# Merge reviews with books_with_year
merged = pd.merge(reviews_df, books_with_year, on='book_id', how='inner')

# Compute book-level average rating
book_avg = merged.groupby('book_id', as_index=False).agg({'rating':'mean','year':'first'})
book_avg.rename(columns={'rating':'avg_rating'}, inplace=True)

# Compute decade string
book_avg['decade'] = book_avg['year'].apply(lambda y: f"{(y//10)*10}s")

# For each decade, compute number of distinct books and average of book averages
decade_stats = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10]

result = None
if not eligible.empty:
    top = eligible.sort_values(['decade_avg_rating','book_count'], ascending=[False, False]).iloc[0]
    result = {
        'top_decade': top['decade'],
        'avg_rating': round(float(top['decade_avg_rating']), 4),
        'book_count': int(top['book_count'])
    }
else:
    result = {'top_decade': None, 'avg_rating': None, 'book_count': 0}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_7VOh4xTcb57rnEvrY1f5MwJD': ['books_info'], 'var_call_sSj5ReKOEYbZc2JarxnfqDnj': ['review'], 'var_call_Me5Jno1YYjUTQbFDUKsAFOe0': 'file_storage/call_Me5Jno1YYjUTQbFDUKsAFOe0.json', 'var_call_71BLhMQ8VRq1OQ55Ls0BOjbF': 'file_storage/call_71BLhMQ8VRq1OQ55Ls0BOjbF.json', 'var_call_nBsb3bz8kItIWn2tWw4QfEnd': 'file_storage/call_nBsb3bz8kItIWn2tWw4QfEnd.json'}

exec(code, env_args)
