code = """import json
import pandas as pd
import math

# Load data from previous tool calls. These variables are provided by the system.
books_data_var = var_call_nrYy8mmH0Al1fp4LB0H8yn4D
reviews_data_var = var_call_kPJvQjH7XgfuSEsPr3dP6uZC

def load_var(v):
    # If v is a string, assume it's a filepath to a JSON file; otherwise assume it's already a list of records
    if isinstance(v, str):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books_records = load_var(books_data_var)
reviews_records = load_var(reviews_data_var)

# Create DataFrames
df_books = pd.DataFrame(books_records)
df_reviews = pd.DataFrame(reviews_records)

# Normalize column names
# books: book_id, pub_year (may be string)
if 'pub_year' not in df_books.columns:
    # try to extract year from details
    df_books['pub_year'] = df_books['details'].str.extract(r'([0-9]{4})')

# Clean pub_year to numeric
df_books['pub_year'] = pd.to_numeric(df_books['pub_year'], errors='coerce')

# Reviews: purchase_id, rating
# Convert rating to numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = pd.Series(dtype=float)

# Map purchase_id to book_id by replacing prefix 'purchaseid_' with 'bookid_'
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
elif 'purchaseid' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchaseid'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
else:
    # try common column name
    if 'purchase_id' not in df_reviews.columns and 'purchaseid' not in df_reviews.columns:
        # try to find any column that looks like purchase id
        possible = [c for c in df_reviews.columns if 'purchase' in c or 'purchase_id' in c]
        if possible:
            df_reviews['book_id'] = df_reviews[possible[0]].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
        else:
            df_reviews['book_id'] = None

# Compute average rating per book
book_avg = df_reviews.dropna(subset=['book_id','rating']).groupby('book_id', as_index=False)['rating'].mean()
book_avg.rename(columns={'rating':'avg_rating'}, inplace=True)

# Merge with books to get pub_year
df_merged = pd.merge(book_avg, df_books[['book_id','pub_year']], on='book_id', how='left')

# Drop entries without pub_year
df_merged = df_merged.dropna(subset=['pub_year'])

# Compute decade label
df_merged['pub_year'] = df_merged['pub_year'].astype(int)

def decade_label(y):
    start = (y // 10) * 10
    return f"{start}s"

df_merged['decade'] = df_merged['pub_year'].apply(decade_label)

# For each decade, count distinct books and average the book avg_ratings
decade_stats = df_merged.groupby('decade').agg(
    num_books = ('book_id', 'nunique'),
    decade_avg = ('avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['num_books'] >= 10]

if decade_stats_filtered.empty:
    result = None
else:
    # Find decade with highest average
    top = decade_stats_filtered.sort_values(['decade_avg','decade'], ascending=[False, True]).iloc[0]
    result = {
        'decade': top['decade'],
        'average_rating': round(float(top['decade_avg']), 4),
        'num_books': int(top['num_books'])
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_Go94iL3BH7Fqsq58PtZxXId0': ['books_info'], 'var_call_oI5RuCu1PxXkYwt9ky9nrDZw': 'file_storage/call_oI5RuCu1PxXkYwt9ky9nrDZw.json', 'var_call_nrYy8mmH0Al1fp4LB0H8yn4D': 'file_storage/call_nrYy8mmH0Al1fp4LB0H8yn4D.json', 'var_call_FOfXAEqcpmsQzHKwQE5yeScW': ['review'], 'var_call_kPJvQjH7XgfuSEsPr3dP6uZC': 'file_storage/call_kPJvQjH7XgfuSEsPr3dP6uZC.json'}

exec(code, env_args)
