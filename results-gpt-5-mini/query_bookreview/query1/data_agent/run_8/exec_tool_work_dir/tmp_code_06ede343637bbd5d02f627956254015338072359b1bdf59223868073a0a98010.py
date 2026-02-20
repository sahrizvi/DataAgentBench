code = """import json
import pandas as pd
import re

# Load data from previous tool call storage files
with open(var_call_GniwUtsSp9f2pYlZhGhl7Skr, 'r') as f:
    books = json.load(f)
with open(var_call_OQd8lJCc46ftZwMhyUhqs8JE, 'r') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize reviews: ensure rating numeric, extract numeric id and map to bookid_N
reviews_df = reviews_df.dropna(subset=['purchase_id', 'rating'])

# Convert rating to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating'])

# Extract numeric id
def extract_num(pid):
    m = re.search(r"(\d+)", str(pid))
    return m.group(1) if m else None

reviews_df['num'] = reviews_df['purchase_id'].apply(extract_num)
reviews_df = reviews_df.dropna(subset=['num'])
reviews_df['book_id'] = 'bookid_' + reviews_df['num'].astype(str)

# Aggregate per-book average rating
book_ratings = reviews_df.groupby('book_id', as_index=False)['rating'].mean()
book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

# Extract publication year from books.details
def extract_year(text):
    if not isinstance(text, str):
        return None
    # look for years between 1000 and 2023
    matches = re.findall(r"\b(1[0-9]{3}|20[0-2][0-9]|2023)\b", text)
    if matches:
        try:
            return int(matches[0])
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)

# Join book_ratings with books_df on book_id
merged = pd.merge(book_ratings, books_df[['book_id', 'year']], on='book_id', how='inner')

# Compute decade label
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# For each decade, count distinct books and compute average of per-book average ratings
decade_stats = merged.groupby('decade').agg(
    book_count=('book_id', 'nunique'),
    decade_avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10]

if eligible.empty:
    result = {'best_decade': None, 'message': 'No decade with at least 10 distinct rated books found.'}
else:
    # find decade with highest average rating
    best_row = eligible.sort_values(['decade_avg_rating', 'decade'], ascending=[False, True]).iloc[0]
    result = {
        'best_decade': best_row['decade'],
        'decade_avg_rating': round(float(best_row['decade_avg_rating']), 4),
        'book_count': int(best_row['book_count'])
    }

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_kD1JgrgEE8aNluB4BcHZm5CG': ['books_info'], 'var_call_GniwUtsSp9f2pYlZhGhl7Skr': 'file_storage/call_GniwUtsSp9f2pYlZhGhl7Skr.json', 'var_call_WebfN6HiMJIkOFoNIbyACLNc': ['review'], 'var_call_OQd8lJCc46ftZwMhyUhqs8JE': 'file_storage/call_OQd8lJCc46ftZwMhyUhqs8JE.json'}

exec(code, env_args)
