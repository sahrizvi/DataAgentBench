code = """import json
import re
import pandas as pd

# Load the JSON results from the stored file paths
with open(var_call_BMgq6LjFE0XefpPiDnRIb6Ne, 'r') as f:
    books = json.load(f)
with open(var_call_GaIsdAW26tC6Ar7PpjmVqKCK, 'r') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract numeric id suffix from book_id and purchase_id
books_df['id_num'] = books_df['book_id'].astype(str).str.extract(r'(\d+)$')
reviews_df['id_num'] = reviews_df['purchase_id'].astype(str).str.extract(r'(\d+)$')

# Drop rows where id_num is missing
books_df = books_df[books_df['id_num'].notna()].copy()
reviews_df = reviews_df[reviews_df['id_num'].notna()].copy()

books_df['id_num'] = books_df['id_num'].astype(int)
reviews_df['id_num'] = reviews_df['id_num'].astype(int)

# Extract publication year from details field using regex for years between 1000 and 2029
def extract_year(text):
    if not isinstance(text, str):
        return None
    m = re.search(r'(19|20)\d{2}', text)
    if m:
        try:
            y = int(m.group(0))
            if 1000 <= y <= 2029:
                return y
        except:
            return None
    return None

books_df['pub_year'] = books_df['details'].apply(extract_year)

# Compute decade string
books_df['decade'] = books_df['pub_year'].apply(lambda y: f"{(y//10)*10}s" if pd.notna(y) else None)

# Prepare reviews: convert rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Compute per-book average rating and ensure the book exists in books_df
book_ratings = reviews_df.groupby('id_num', as_index=False).agg(book_avg_rating=('rating', 'mean'), num_reviews=('rating','count'))

# Merge with books to get publication decade
merged = pd.merge(book_ratings, books_df[['id_num','pub_year','decade','book_id','title']], on='id_num', how='left')

# Drop entries without decade
merged = merged[merged['decade'].notna()].copy()

# Compute per-decade stats: count distinct books and average of book average ratings
decade_stats = merged.groupby('decade', as_index=False).agg(num_books=('id_num','nunique'), avg_of_book_avgs=('book_avg_rating','mean'))

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10].copy()

if eligible.empty:
    result = {'error':'No decade has at least 10 distinct rated books.'}
else:
    # Find decade with highest average
    eligible = eligible.sort_values(['avg_of_book_avgs','decade'], ascending=[False, True]).reset_index(drop=True)
    best = eligible.iloc[0]
    result = {
        'best_decade': best['decade'],
        'avg_rating': round(float(best['avg_of_book_avgs']),4),
        'num_books': int(best['num_books'])
    }

# Also include eligible table for transparency (limit to top 50)
eligible_records = eligible.sort_values('avg_of_book_avgs', ascending=False).to_dict(orient='records')[:50]
output = {'result': result, 'eligible_decades': eligible_records}

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_j6x3TWWTtM2ocu17gxSqNcFO': ['books_info'], 'var_call_BMgq6LjFE0XefpPiDnRIb6Ne': 'file_storage/call_BMgq6LjFE0XefpPiDnRIb6Ne.json', 'var_call_SqsG5MEYAUS2ldnC17TS1irx': ['review'], 'var_call_GaIsdAW26tC6Ar7PpjmVqKCK': 'file_storage/call_GaIsdAW26tC6Ar7PpjmVqKCK.json'}

exec(code, env_args)
