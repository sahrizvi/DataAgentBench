code = """import json
import re
import pandas as pd

# Load data from previous tool calls stored in variables
books_raw = var_call_THvtEYeFNyupV3rFXwV8MAY6
reviews_raw = var_call_2YzYZpvlvkxO5SzL48yq4Jkd

# If the variables are file paths (strings ending with .json), load them
def load_maybe_file(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books_data = load_maybe_file(books_raw)
reviews_data = load_maybe_file(reviews_raw)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Clean and prepare reviews
if 'rating' in df_reviews.columns:
    # Convert rating to numeric, coerce errors
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = pd.NA

# Map purchase_id to book_id by replacing prefix
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
else:
    df_reviews['book_id'] = None

# Keep relevant columns
df_reviews = df_reviews[['book_id', 'rating', 'review_time']]

# Extract publication year from books details
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # find all 4-digit numbers
    matches = re.findall(r"(\d{4})", detail)
    for m in matches:
        y = int(m)
        if 1000 <= y <= 2023:
            return y
    return None

if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

# Merge reviews with books on book_id
df_merged = pd.merge(df_reviews, df_books[['book_id', 'pub_year']], on='book_id', how='left')

# Drop rows without rating or without pub_year
df_merged = df_merged.dropna(subset=['rating', 'pub_year'])

# Compute per-book average rating and pub_year (use pub_year from books)
book_avg = df_merged.groupby('book_id').agg({'rating':'mean', 'pub_year':'first'}).reset_index()
book_avg.rename(columns={'rating':'book_avg_rating'}, inplace=True)

# Compute decade label
book_avg['decade_start'] = (book_avg['pub_year'].astype(int) // 10) * 10
book_avg['decade'] = book_avg['decade_start'].astype(str) + 's'

# For each decade compute number of distinct books and average of per-book averages
decade_stats = book_avg.groupby('decade').agg(
    book_count = ('book_id', 'nunique'),
    avg_rating = ('book_avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['book_count'] >= 10]

# If none meet criteria, return None
if decade_stats_filtered.empty:
    result = {'decade': None, 'average_rating': None, 'book_count': 0}
else:
    # select decade with highest avg_rating; in tie pick the one with highest avg then smallest decade_start maybe
    top = decade_stats_filtered.sort_values(by=['avg_rating', 'decade'], ascending=[False, True]).iloc[0]
    result = {'decade': top['decade'], 'average_rating': round(float(top['avg_rating']), 4), 'book_count': int(top['book_count'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_bBgONVeHyXRTXA0iYijX3gvq': ['books_info'], 'var_call_THvtEYeFNyupV3rFXwV8MAY6': 'file_storage/call_THvtEYeFNyupV3rFXwV8MAY6.json', 'var_call_azFVIjoQNfdxX5rpwTfw8oSG': ['review'], 'var_call_2YzYZpvlvkxO5SzL48yq4Jkd': 'file_storage/call_2YzYZpvlvkxO5SzL48yq4Jkd.json'}

exec(code, env_args)
