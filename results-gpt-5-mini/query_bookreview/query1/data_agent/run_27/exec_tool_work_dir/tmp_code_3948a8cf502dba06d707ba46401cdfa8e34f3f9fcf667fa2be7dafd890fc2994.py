code = """import json
import pandas as pd
import re

# load data from storage-provided file paths
with open(var_call_bl0OalULUPxWRsLVavUjyoNu, 'r') as f:
    books = json.load(f)
with open(var_call_2ekejQnzaNplQxWwjsy4e7qc, 'r') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# normalize columns
books_df = books_df[['book_id', 'details']].dropna(subset=['book_id'])

# function to extract year from details
def extract_year(text):
    if not isinstance(text, str):
        return None
    # find all 4-digit numbers
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", text)
    if not years:
        return None
    # convert to int and filter reasonable range 1500-2023
    for y in years:
        try:
            yi = int(y)
            if 1500 <= yi <= 2023:
                return yi
        except:
            continue
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade'] = (books_df['year'] // 10 * 10).astype(int).astype(str) + 's'

# prepare reviews: convert rating to float and map purchase_id -> book_id
reviews_df = reviews_df.dropna(subset=['purchase_id','rating'])
# convert rating to float
def to_float(x):
    try:
        return float(x)
    except:
        return None

reviews_df['rating'] = reviews_df['rating'].apply(to_float)
reviews_df = reviews_df.dropna(subset=['rating'])

# map purchaseid to bookid (fuzzy mapping assumed as replace prefix)
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# only keep reviews whose book exists in books_df
books_set = set(books_df['book_id'])
reviews_df = reviews_df[reviews_df['book_id'].isin(books_set)]

# compute per-book average rating
book_avg = reviews_df.groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating':'avg_rating'})

# merge with books to get decade
merged = pd.merge(book_avg, books_df[['book_id','decade']], on='book_id', how='left')
merged = merged.dropna(subset=['decade'])

# compute per-decade stats: number of distinct books and average of book average ratings
decade_stats = merged.groupby('decade').agg(num_books=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['num_books'] >= 10]

result = None
if not decade_stats_filtered.empty:
    # find decade with highest average rating
    best = decade_stats_filtered.sort_values(['decade_avg_rating','num_books'], ascending=[False, False]).iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['decade_avg_rating']), 4),
        'num_books': int(best['num_books'])
    }
else:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_aJISRXFVks0RCkkveOuXfOfR': ['books_info'], 'var_call_Sc2yHvzTHzf8hisV1ug2TXBH': ['review'], 'var_call_bl0OalULUPxWRsLVavUjyoNu': 'file_storage/call_bl0OalULUPxWRsLVavUjyoNu.json', 'var_call_2ekejQnzaNplQxWwjsy4e7qc': 'file_storage/call_2ekejQnzaNplQxWwjsy4e7qc.json'}

exec(code, env_args)
