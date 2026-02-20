code = """import json
import pandas as pd
import re

# Load data files from storage paths
with open(var_call_fCXKjFuQR0KVnKs5USPd527y, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_0WiZXUQS5sLYvZ5ccFLAWezZ, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract numeric id from book_id and purchase_id
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)')
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)')

# Drop rows without numeric ids
df_books = df_books[df_books['id_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['id_num'].notna()].copy()

# Convert id_num to int
df_books['id_num'] = df_books['id_num'].astype(int)
df_reviews['id_num'] = df_reviews['id_num'].astype(int)

# Function to extract publication year from details
year_re = re.compile(r'\b(1[89]\d{2}|20[0-2]\d|2023)\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    found = year_re.findall(text)
    if not found:
        return None
    # findall with groups returns tuples sometimes; ensure conversion
    # If regex has groups, findall returns tuples; but our pattern has one group so returns strings
    for item in found:
        try:
            y = int(item)
            if 1800 <= y <= 2023:
                return y
        except:
            continue
    return None

# Apply extraction
df_books['pub_year'] = df_books['details'].apply(extract_year)
# Drop books without year
df_books = df_books[df_books['pub_year'].notna()].copy()

df_books['pub_year'] = df_books['pub_year'].astype(int)
# Create decade label
df_books['decade'] = (df_books['pub_year'] // 10 * 10).astype(int).astype(str) + 's'

# Convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Drop invalid ratings
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

# Merge reviews with books on numeric id
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))

# If merged empty, return no data
if merged.empty:
    result = json.dumps({"error": "No matched reviews and books after fuzzy numeric id join."})
    print("__RESULT__:")
    print(result)
else:
    # Compute per-book average rating
    book_avg = merged.groupby(['book_id','decade'])['rating'].mean().reset_index()
    # Count distinct books per decade and average of per-book averages
    per_decade = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), average_rating=('rating','mean')).reset_index()
    # Filter decades with at least 10 distinct books
    per_decade = per_decade[per_decade['book_count'] >= 10].copy()
    if per_decade.empty:
        result = json.dumps({"error": "No decade has at least 10 distinct rated books."})
        print("__RESULT__:")
        print(result)
    else:
        # Find decade with highest average_rating
        best = per_decade.sort_values(['average_rating','decade'], ascending=[False, True]).iloc[0]
        out = {"decade": best['decade'], "average_rating": round(float(best['average_rating']), 4), "book_count": int(best['book_count'])}
        result = json.dumps(out)
        print("__RESULT__:")
        print(result)"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json'}

exec(code, env_args)
