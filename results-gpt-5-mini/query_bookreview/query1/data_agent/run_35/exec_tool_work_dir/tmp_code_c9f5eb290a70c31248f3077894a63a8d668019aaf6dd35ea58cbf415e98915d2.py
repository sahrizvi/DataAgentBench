code = """import json
import pandas as pd
import re

# Load tool results from storage variables
books_path = var_call_ro8JdSTArIxNI3mgZc1y6P8N
reviews_path = var_call_Gbr4XrEs6ReGZzoZHbT0Pcrm

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# extract numeric id from strings like 'bookid_123' or 'purchaseid_123'
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

books_df['book_num'] = books_df['book_id'].apply(extract_num)
reviews_df['book_num'] = reviews_df['purchase_id'].apply(extract_num)

# parse rating
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# extract publication year from details
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # find all 4-digit numbers between 1500 and 2023
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", detail)
    if not years:
        return None
    # convert and filter range
    for y in years:
        try:
            yi = int(y)
        except:
            continue
        if 1500 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# derive decade string
books_df['decade'] = books_df['year'].apply(lambda y: f"{(y//10)*10}s" if pd.notnull(y) else None)

# Merge reviews with books on numeric id
merged = pd.merge(reviews_df, books_df[['book_num','book_id','title','year','decade']], on='book_num', how='inner')

# Keep only entries with valid decade
merged = merged[merged['decade'].notnull()]

# compute per-book average rating (book must have at least one review)
book_avg = merged.groupby(['book_num','book_id','title','decade','year'], as_index=False)['rating'].mean()
book_avg.rename(columns={'rating':'avg_rating'}, inplace=True)

# group by decade: count distinct books and average of per-book averages
decade_stats = book_avg.groupby('decade').agg(num_books=('book_num','nunique'),
                                               decade_avg_rating=('avg_rating','mean')).reset_index()
# filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['num_books']>=10]

if decade_stats_filtered.empty:
    result = {"decade": None, "message": "No decade has at least 10 distinct rated books."}
else:
    # pick decade with highest average rating
    top = decade_stats_filtered.sort_values(['decade_avg_rating','num_books'], ascending=[False, False]).iloc[0]
    result = {"decade": top['decade'], "avg_rating": round(float(top['decade_avg_rating']),4), "num_books": int(top['num_books'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_q14bTIlDF2re1BTH3QFWYEmT': ['books_info'], 'var_call_ro8JdSTArIxNI3mgZc1y6P8N': 'file_storage/call_ro8JdSTArIxNI3mgZc1y6P8N.json', 'var_call_o2ejEIifRgRMkCWNttzgET90': ['review'], 'var_call_Gbr4XrEs6ReGZzoZHbT0Pcrm': 'file_storage/call_Gbr4XrEs6ReGZzoZHbT0Pcrm.json'}

exec(code, env_args)
