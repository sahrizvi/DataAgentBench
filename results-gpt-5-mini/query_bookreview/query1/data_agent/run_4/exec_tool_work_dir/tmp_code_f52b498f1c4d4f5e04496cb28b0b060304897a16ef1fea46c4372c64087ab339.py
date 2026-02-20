code = """import json
import re
from pathlib import Path
import pandas as pd

# Load query results from storage file paths
books_path = Path(var_call_f6qwbMRGzupURhp4jevYsPZG)
reviews_path = Path(var_call_yyGrpufaDnePpaIi2wy3SImg)

with books_path.open('r', encoding='utf-8') as f:
    books = json.load(f)
with reviews_path.open('r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize column types
if 'details' not in df_books.columns:
    df_books['details'] = ''

# Extract year from details using regex looking for 4-digit year (1900-2099)
def extract_year(text):
    if not isinstance(text, str):
        return None
    m = re.search(r"(19|20)\d{2}", text)
    if m:
        try:
            return int(m.group(0))
        except:
            return None
    return None

df_books['pub_year'] = df_books['details'].apply(extract_year)

# Map purchase_id like 'purchaseid_8' to 'bookid_8'
if 'purchase_id' in df_reviews.columns:
    df_reviews['mapped_book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')
else:
    # fallback to purchase_id field name in preview: seems 'purchase_id' is used in some datasets
    df_reviews['mapped_book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Convert rating to float
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Join reviews to books on mapped_book_id == book_id
merged = df_reviews.merge(df_books[['book_id','pub_year']], left_on='mapped_book_id', right_on='book_id', how='left')

# Drop reviews without matched book or without pub_year
merged = merged.dropna(subset=['book_id','pub_year','rating'])
merged['pub_year'] = merged['pub_year'].astype(int)

# Compute per-book average rating
book_avg = merged.groupby('book_id', as_index=False)['rating'].mean()
# Add pub_year for each book
book_year = merged.groupby('book_id', as_index=False)['pub_year'].first()
book_avg = book_avg.merge(book_year, on='book_id')

# Compute decade string
def year_to_decade(y):
    try:
        y = int(y)
    except:
        return None
    decade_start = (y // 10) * 10
    return f"{decade_start}s"

book_avg['decade'] = book_avg['pub_year'].apply(year_to_decade)

# Filter out missing decades
book_avg = book_avg.dropna(subset=['decade'])

# For each decade, count distinct books and compute average of book average ratings
decade_stats = book_avg.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10]

if eligible.empty:
    result = {"decade": None, "average_rating": None, "num_books": 0}
else:
    # Find decade with highest average rating; in case of tie, choose decade with more books, then lexicographically
    eligible = eligible.sort_values(by=['avg_rating','num_books','decade'], ascending=[False, False, True])
    top = eligible.iloc[0]
    result = {"decade": top['decade'], "average_rating": round(float(top['avg_rating']), 4), "num_books": int(top['num_books'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_UwLDPY0oUSq34p8PvgsEcZMC': ['books_info'], 'var_call_f6qwbMRGzupURhp4jevYsPZG': 'file_storage/call_f6qwbMRGzupURhp4jevYsPZG.json', 'var_call_HSxkw88Mhu76c49Fxaks4hAQ': ['review'], 'var_call_yyGrpufaDnePpaIi2wy3SImg': 'file_storage/call_yyGrpufaDnePpaIi2wy3SImg.json'}

exec(code, env_args)
