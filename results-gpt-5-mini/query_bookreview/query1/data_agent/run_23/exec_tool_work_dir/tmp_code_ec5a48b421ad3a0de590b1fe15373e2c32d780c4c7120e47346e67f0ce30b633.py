code = """import json
import re
import pandas as pd

# Load data from previous query results stored as JSON file paths
with open(var_call_39gXnyWYar7LTqIiW86LzpXl, 'r') as f:
    books = json.load(f)
with open(var_call_lVzzRj6s3F8ocOSU5Xp6OWcq, 'r') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract publication year from details using regex for years between 1800 and 2099
year_pattern = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    m = year_pattern.search(detail)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['pub_year'] = books_df['details'].apply(extract_year)
books_df = books_df.dropna(subset=['pub_year'])
books_df['pub_year'] = books_df['pub_year'].astype(int)
books_df['decade'] = (books_df['pub_year'] // 10 * 10).astype(int).astype(str) + 's'

# Normalize reviews: convert rating to float and map purchase_id to book_id by numeric suffix
# Extract numeric part
num_pattern = re.compile(r"(\d+)$")

def map_purchase_to_book(pid):
    if not isinstance(pid, str):
        return None
    m = num_pattern.search(pid)
    if m:
        return 'bookid_' + m.group(1)
    return None

reviews_df['book_id'] = reviews_df['purchase_id'].apply(map_purchase_to_book)
# Convert rating to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['book_id', 'rating'])

# Join reviews with books on book_id
merged = reviews_df.merge(books_df[['book_id','decade']], on='book_id', how='inner')

# Compute per-book mean rating
book_means = merged.groupby('book_id', as_index=False)['rating'].mean()
# attach decade
book_means = book_means.merge(books_df[['book_id','decade']], on='book_id', how='left')

# Compute per-decade stats: number of distinct books and average of per-book means
decade_stats = book_means.groupby('decade', as_index=False).agg(
    num_books=('book_id','nunique'),
    avg_rating=('rating','mean')
)

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10]

if eligible.empty:
    result = {'decade': None, 'average_rating': None, 'note': 'No decade has at least 10 distinct rated books.'}
else:
    # find decade with highest average rating
    best = eligible.sort_values(['avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['avg_rating']), 3),
        'num_books': int(best['num_books'])
    }

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_XHoJnj79KG90C95CK9tbdJhP': ['books_info'], 'var_call_39gXnyWYar7LTqIiW86LzpXl': 'file_storage/call_39gXnyWYar7LTqIiW86LzpXl.json', 'var_call_kywSihPBtvDvgDPFx0ETY4c5': ['review'], 'var_call_lVzzRj6s3F8ocOSU5Xp6OWcq': 'file_storage/call_lVzzRj6s3F8ocOSU5Xp6OWcq.json'}

exec(code, env_args)
