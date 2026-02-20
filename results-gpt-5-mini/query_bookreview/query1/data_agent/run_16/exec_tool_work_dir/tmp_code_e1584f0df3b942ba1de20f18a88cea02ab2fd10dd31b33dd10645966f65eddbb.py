code = """import json, re, statistics
import pandas as pd

# Load data from storage-provided file paths
with open(var_call_zY5ogCQhaFgOuTnCyCu1V40W, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_HFQ2SHbSA4PpNbrQ6TKt3dWV, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize ID numeric suffix to join
def extract_num(s):
    if pd.isna(s):
        return None
    m = re.search(r"(\d+)", str(s))
    return int(m.group(1)) if m else None

books_df['num_id'] = books_df['book_id'].apply(extract_num)
reviews_df['num_id'] = reviews_df['purchase_id'].apply(extract_num)

# Parse rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Extract publication year from details (first 4-digit year between 1000 and 2023)
def extract_year(detail):
    if pd.isna(detail):
        return None
    # find all 4-digit numbers
    years = re.findall(r"(1[0-9]{3}|20[0-2][0-9]|2023)", str(detail))
    if years:
        return int(years[0])
    # fallback: any 4-digit
    m = re.search(r"(\d{4})", str(detail))
    return int(m.group(1)) if m else None

books_df['year'] = books_df['details'].apply(extract_year)
# Drop books without numeric id or year
books_df = books_df.dropna(subset=['num_id','year'])
reviews_df = reviews_df.dropna(subset=['num_id','rating'])

# Compute per-book average rating using numeric id
book_ratings = reviews_df.groupby('num_id')['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

# Merge with books to get year
merged = pd.merge(book_ratings, books_df[['num_id','year','book_id','title']], on='num_id', how='inner')

# Compute decade label
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# For each decade with at least 10 distinct books, compute average of per-book averages
decade_stats = merged.groupby('decade').agg(book_count=('num_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()
# Filter decades with at least 10 distinct books
decade_stats = decade_stats[decade_stats['book_count'] >= 10]

# If no decades meet criteria, return None
if decade_stats.empty:
    result = None
else:
    # find decade with highest average rating, tie-breaker: highest book_count then lexicographic
    top = decade_stats.sort_values(by=['decade_avg_rating','book_count','decade'], ascending=[False,False,True]).iloc[0]
    result = top['decade']

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_dxkONNJnkBRi4IqApjbgtjgO': ['books_info'], 'var_call_FN5NQCGiAMA5zhvrjA6G3sBs': ['review'], 'var_call_zY5ogCQhaFgOuTnCyCu1V40W': 'file_storage/call_zY5ogCQhaFgOuTnCyCu1V40W.json', 'var_call_HFQ2SHbSA4PpNbrQ6TKt3dWV': 'file_storage/call_HFQ2SHbSA4PpNbrQ6TKt3dWV.json'}

exec(code, env_args)
