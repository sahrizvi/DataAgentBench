code = """import json
import pandas as pd
import re

# Load query results from storage file paths
with open(var_call_BgihlwyIZ4U9KuHo5t3MsRI4, 'r') as f:
    books = json.load(f)
with open(var_call_wJqlV7suAZNtIFs3Hyws1UlT, 'r') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Clean reviews: convert rating to numeric, create book_id by replacing prefix
reviews_df = reviews_df.dropna(subset=['purchase_id'])
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')
# convert rating to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating'])

# Extract publication year from books.details
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # look for 4-digit year between 1500 and 2023
    m = re.search(r"(17|18|19|20)\d{2}", detail)
    if m:
        year = int(m.group(0))
        # basic sanity
        if 1500 <= year <= 2023:
            return year
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# drop books without year
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade'] = (books_df['year'] // 10 * 10).astype(int).astype(str) + 's'

# Merge reviews with books on book_id
merged = reviews_df.merge(books_df[['book_id','decade']], on='book_id', how='inner')

# Compute per-book average rating
book_avg = merged.groupby('book_id', as_index=False)['rating'].mean()
# attach decade
book_avg = book_avg.merge(books_df[['book_id','decade']], on='book_id', how='left')

# Compute per-decade stats: number of distinct books with ratings, average of book averages
decade_stats = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()
# Filter decades with at least 10 distinct books
decade_stats = decade_stats[decade_stats['book_count'] >= 10]

# If none meet threshold, return None
if decade_stats.empty:
    result = None
else:
    # Get decade with highest avg_rating. If tie, pick highest avg_rating then highest book_count, then earliest decade lexicographically
    top = decade_stats.sort_values(['avg_rating','book_count','decade'], ascending=[False,False,True]).iloc[0]
    result = {
        'decade': top['decade'],
        'average_rating': round(float(top['avg_rating']), 4),
        'book_count': int(top['book_count'])
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_3TK5we0UalUUIyoPLOi9Z2fj': ['books_info'], 'var_call_KaoGR9lGdK3vx7nLyNc1bkSd': ['review'], 'var_call_BgihlwyIZ4U9KuHo5t3MsRI4': 'file_storage/call_BgihlwyIZ4U9KuHo5t3MsRI4.json', 'var_call_wJqlV7suAZNtIFs3Hyws1UlT': 'file_storage/call_wJqlV7suAZNtIFs3Hyws1UlT.json'}

exec(code, env_args)
