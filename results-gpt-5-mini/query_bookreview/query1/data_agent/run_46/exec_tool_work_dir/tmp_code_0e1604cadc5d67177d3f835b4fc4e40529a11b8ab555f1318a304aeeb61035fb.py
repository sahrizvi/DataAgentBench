code = """import json
import pandas as pd
import re

# Load data from storage variables
books_path = var_call_IgzP9mcCLvIHahQeyTMgy2fN
reviews_path = var_call_DjjcDS9g6IjEnM4EWPD0ZeDP

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract year from details using regex for years between 1000 and 2023
def extract_year(text):
    if not isinstance(text, str):
        return None
    # find all 4-digit numbers that look like years
    candidates = re.findall(r"(1[0-9]{3}|20[0-9]{2})", text)
    for c in candidates:
        y = int(c)
        if 1000 <= y <= 2023:
            return y
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Normalize review ratings and map purchase_id to book_id by replacing 'purchaseid_' with 'bookid_'
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Join reviews to books on book_id
# Keep only reviews that map to a book present in books table
merged = pd.merge(df_reviews, df_books[['book_id', 'title', 'year']], on='book_id', how='inner')

# Drop entries without year
merged = merged[merged['year'].notna()].copy()
merged['year'] = merged['year'].astype(int)

# Compute book-level average rating
book_avg = merged.groupby('book_id', as_index=False).agg(book_avg_rating=('rating', 'mean'), title=('title','first'), year=('year','first'))

# Compute decade for each book
book_avg['decade_start'] = (book_avg['year'] // 10) * 10
book_avg['decade'] = book_avg['decade_start'].astype(int).astype(str) + 's'

# For each decade, consider distinct books count and average of book averages
decade_stats = book_avg.groupby('decade').agg(num_books=('book_id','nunique'), decade_avg_rating=('book_avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['num_books'] >= 10].copy()

# If no decades meet criteria, prepare a fallback
if decade_stats_filtered.empty:
    result = {"best_decade": None, "decade_avg_rating": None, "message": "No decade has at least 10 distinct rated books."}
else:
    # Find decade with highest average rating
    best_row = decade_stats_filtered.sort_values(['decade_avg_rating','num_books'], ascending=[False, False]).iloc[0]
    result = {"best_decade": best_row['decade'], "decade_avg_rating": round(float(best_row['decade_avg_rating']), 4), "num_books": int(best_row['num_books'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_IgzP9mcCLvIHahQeyTMgy2fN': 'file_storage/call_IgzP9mcCLvIHahQeyTMgy2fN.json', 'var_call_DjjcDS9g6IjEnM4EWPD0ZeDP': 'file_storage/call_DjjcDS9g6IjEnM4EWPD0ZeDP.json'}

exec(code, env_args)
