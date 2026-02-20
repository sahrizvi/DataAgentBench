code = """import json
import pandas as pd
import re

books_path = var_call_7FJ9IMMgIMHkvLUrf4c303HD
reviews_path = var_call_Gj1sMenyHy1SfsivQvI5Vnz3

with open(books_path,'r',encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path,'r',encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)
reviews_df['avg_rating'] = reviews_df['avg_rating'].astype(float)
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_','bookid_')

# extract year as before
def extract_year(text):
    if not isinstance(text, str):
        return None
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)
    if m:
        try:
            return int(m.group(0))
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)

merged = pd.merge(reviews_df[['book_id','avg_rating']], books_df[['book_id','title','year']], on='book_id', how='left')

# Count how many merged rows have year
total_reviews = len(merged)
with_year = merged['year'].notnull().sum()

# Compute decade and group even for missing years
merged['year'] = merged['year'].apply(lambda x: int(x) if pd.notnull(x) else None)
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s" if y is not None else None)

# Drop duplicates by book_id
book_level = merged.drop_duplicates(subset=['book_id']).copy()
# Group by decade
grp = book_level.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('avg_rating','mean')).reset_index()
# sort
grp_sorted = grp.sort_values(by='avg_rating', ascending=False).fillna({'decade':'Unknown'})

# Build output
out = {
    'total_books_considered': len(book_level),
    'total_review_rows': total_reviews,
    'rows_with_year': int(with_year),
    'decade_stats_top20': grp_sorted.head(20).to_dict(orient='records')
}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_FSwmNwxkbsM9XsVSeLxTynuU': ['books_info'], 'var_call_xNukcDXZlRQMiVAO8i7iK71g': ['review'], 'var_call_7FJ9IMMgIMHkvLUrf4c303HD': 'file_storage/call_7FJ9IMMgIMHkvLUrf4c303HD.json', 'var_call_Gj1sMenyHy1SfsivQvI5Vnz3': 'file_storage/call_Gj1sMenyHy1SfsivQvI5Vnz3.json', 'var_call_vLgNVjauTd7s2IR92nuKrtXd': None, 'var_call_20K3batRwWELXaFfVMStzZrK': {'sample_books': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_reviews': ['purchaseid_1', 'purchaseid_10', 'purchaseid_100', 'purchaseid_101', 'purchaseid_102', 'purchaseid_103', 'purchaseid_104', 'purchaseid_105', 'purchaseid_106', 'purchaseid_107', 'purchaseid_108', 'purchaseid_109', 'purchaseid_11', 'purchaseid_110', 'purchaseid_111', 'purchaseid_112', 'purchaseid_113', 'purchaseid_114', 'purchaseid_115', 'purchaseid_116'], 'books_id_prefixes': {'bookid': 200}, 'reviews_id_prefixes': {'purchaseid': 200}, 'num_reviews': 200, 'num_matches_by_replace': 200}}

exec(code, env_args)
