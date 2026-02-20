code = """import json
import re
import pandas as pd

# Load data from storage file paths
with open(var_call_5gwHasFpI6kVoY8i3hCkbgB7, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_lUdtuDvKPw2Fs6RGZRTAgYof, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract publication year from details using regex
def extract_year(details):
    if not isinstance(details, str):
        return None
    m = re.search(r"\b(17|18|19|20)\d{2}\b", details)
    if m:
        return int(m.group(0))
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# Drop rows without year
books_df = books_df.dropna(subset=['year']).copy()
books_df['year'] = books_df['year'].astype(int)
books_df['decade'] = books_df['year'].apply(lambda y: f"{(y//10)*10}s")

# Clean reviews: rating to float, map purchaseid to bookid
# Some ratings may be strings
reviews_df = reviews_df.dropna(subset=['purchase_id', 'rating']).copy()
reviews_df['rating'] = reviews_df['rating'].astype(float)
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Compute mean rating per book
book_ratings = reviews_df.groupby('book_id', as_index=False)['rating'].mean()
book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

# Join with books to get decade
merged = pd.merge(book_ratings, books_df[['book_id', 'year', 'decade']], on='book_id', how='inner')

# For each decade, compute number of distinct books and average of book average ratings
decade_stats = merged.groupby('decade').agg(book_count=('book_id', 'nunique'), decade_avg_rating=('avg_rating', 'mean')).reset_index()

# Filter decades with at least 10 distinct books
qualifying = decade_stats[decade_stats['book_count'] >= 10].copy()

if qualifying.empty:
    result = {'decade': None, 'avg_rating': None, 'book_count': 0}
else:
    # Get decade with highest average rating
    best = qualifying.sort_values(['decade_avg_rating', 'book_count'], ascending=[False, False]).iloc[0]
    result = {'decade': best['decade'], 'avg_rating': round(float(best['decade_avg_rating']), 4), 'book_count': int(best['book_count'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_3pCpiJFe1xkpGbMMrh6rwLdL': ['books_info'], 'var_call_5gwHasFpI6kVoY8i3hCkbgB7': 'file_storage/call_5gwHasFpI6kVoY8i3hCkbgB7.json', 'var_call_ykA5Ukfnu2mwqSuQmXuZIQID': ['review'], 'var_call_lUdtuDvKPw2Fs6RGZRTAgYof': 'file_storage/call_lUdtuDvKPw2Fs6RGZRTAgYof.json'}

exec(code, env_args)
