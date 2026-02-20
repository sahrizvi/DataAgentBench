code = """import json
import pandas as pd
import re

# Load data from previous tool results
with open(var_call_JbLH76KRr4cUAlnXdAZ7GjNl, 'r') as f:
    books = json.load(f)
with open(var_call_OvVThpITG7V98EweHXUF3VX2, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure required columns
if 'book_id' not in df_books.columns:
    df_books['book_id'] = None
if 'details' not in df_books.columns:
    df_books['details'] = None

# Extract year from details
def extract_year(s):
    if not isinstance(s, str):
        return None
    years = re.findall(r"\b(\d{4})\b", s)
    for y in years:
        yi = int(y)
        if 1500 <= yi <= 2023:
            return yi
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Map purchase_id to book_id by extracting numeric suffix
import math

def purchase_to_bookid(p):
    if not isinstance(p, str):
        return None
    m = re.search(r"(\d+)", p)
    if not m:
        return None
    return f"bookid_{m.group(1)}"

if 'purchase_id' not in df_reviews.columns:
    df_reviews['purchase_id'] = None

if 'rating' not in df_reviews.columns:
    df_reviews['rating'] = None

df_reviews['book_id'] = df_reviews['purchase_id'].apply(purchase_to_bookid)

# Convert rating to float

def to_float(x):
    try:
        return float(x)
    except:
        return None

df_reviews['rating_f'] = df_reviews['rating'].apply(to_float)

# Merge reviews with books on book_id
merged = pd.merge(df_reviews, df_books[['book_id','title','year']], on='book_id', how='left')

# Keep only rows with valid rating and book_id
merged = merged[merged['rating_f'].notna() & merged['book_id'].notna()]

# Compute per-book average rating (using reviews)
book_avg = merged.groupby(['book_id','title','year'], dropna=False)['rating_f'].mean().reset_index()
book_avg.rename(columns={'rating_f':'avg_rating'}, inplace=True)

# Drop books without year
book_avg = book_avg[book_avg['year'].notna()]
book_avg['year'] = book_avg['year'].astype(int)
book_avg['decade'] = (book_avg['year'] // 10 * 10).astype(int).astype(str) + 's'

# Count distinct books per decade
decade_counts = book_avg.groupby('decade')['book_id'].nunique().reset_index(name='num_books')

# Compute average of book averages per decade
decade_avg = book_avg.groupby('decade')['avg_rating'].mean().reset_index()
decade_stats = pd.merge(decade_avg, decade_counts, on='decade')

# Filter decades with at least 10 distinct books
decade_stats = decade_stats[decade_stats['num_books'] >= 10]

result = None
if not decade_stats.empty:
    # Find decade with highest average rating
    best = decade_stats.sort_values(['avg_rating','num_books'], ascending=[False,False]).iloc[0]
    result = {
        'decade': best['decade'],
        'avg_rating': round(float(best['avg_rating']), 4),
        'num_books': int(best['num_books'])
    }
else:
    result = {'decade': None, 'avg_rating': None, 'num_books': 0}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_IiNzrHUwJo78BDzBJg4iFZPH': ['books_info'], 'var_call_QvOSZ7NiEFl07K5XZXthmygk': ['review'], 'var_call_JbLH76KRr4cUAlnXdAZ7GjNl': 'file_storage/call_JbLH76KRr4cUAlnXdAZ7GjNl.json', 'var_call_OvVThpITG7V98EweHXUF3VX2': 'file_storage/call_OvVThpITG7V98EweHXUF3VX2.json'}

exec(code, env_args)
