code = """import json
import re
import pandas as pd

# Load data from storage-provided file paths
books_path = var_call_lRgz9uRSy59VUWELBSEQ3vdv
reviews_path = var_call_1mJ61SrGIUSUtCkpgwF9BoJd

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize column types
if 'rating' in reviews_df.columns:
    reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Map purchase_id to book_id by replacing prefix
if 'purchase_id' in reviews_df.columns:
    reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Extract publication year from details in books_df
year_regex = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    m = year_regex.search(detail)
    if m:
        try:
            y = int(m.group(1))
            return y
        except:
            return None
    return None

books_df['pub_year'] = books_df['details'].apply(extract_year)
# Drop books without a publication year
books_with_year = books_df.dropna(subset=['pub_year']).copy()
books_with_year['pub_year'] = books_with_year['pub_year'].astype(int)
books_with_year['decade'] = books_with_year['pub_year'].apply(lambda y: f"{(y//10)*10}s")

# Compute average rating per book from reviews
# Keep only reviews that map to books present in books_with_year
merged = reviews_df.merge(books_with_year[['book_id','decade']], on='book_id', how='inner')

# Exclude null ratings
merged = merged[merged['rating'].notna()].copy()
merged['rating'] = merged['rating'].astype(float)

book_avg = merged.groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})
# attach decade
book_avg = book_avg.merge(books_with_year[['book_id','decade']], on='book_id', how='left')

# For each decade, compute number of distinct books and average of book_avg_rating
decade_stats = book_avg.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books']>=10].copy()

if eligible.empty:
    result = json.dumps(None)
else:
    # pick decade with highest avg_rating
    best = eligible.sort_values(['avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = json.dumps(best['decade'])

print("__RESULT__:")
print(result)"""

env_args = {'var_call_FLueJjtMsnzlJW2HnGZt2loy': ['books_info'], 'var_call_lRgz9uRSy59VUWELBSEQ3vdv': 'file_storage/call_lRgz9uRSy59VUWELBSEQ3vdv.json', 'var_call_tKWYo7BxsY88mTv76gRnzmuJ': ['review'], 'var_call_1mJ61SrGIUSUtCkpgwF9BoJd': 'file_storage/call_1mJ61SrGIUSUtCkpgwF9BoJd.json'}

exec(code, env_args)
