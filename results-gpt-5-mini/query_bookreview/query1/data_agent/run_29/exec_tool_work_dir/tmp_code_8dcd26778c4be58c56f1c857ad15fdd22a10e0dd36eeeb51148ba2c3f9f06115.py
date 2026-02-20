code = """import json
import pandas as pd
import re
with open(var_call_fCXKjFuQR0KVnKs5USPd527y,'r',encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_0WiZXUQS5sLYvZ5ccFLAWezZ,'r',encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# extract numeric id
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)')
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)')
# convert
df_books['id_num'] = df_books['id_num'].astype(float).astype('Int64')
df_reviews['id_num'] = df_reviews['id_num'].astype(float).astype('Int64')

# Extract pub year
year_re = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')
def extract_year(text):
    if not isinstance(text, str):
        return None
    matches = year_re.findall(text)
    if not matches:
        return None
    for m in matches:
        try:
            y = int(m)
            if 1800 <= y <= 2023:
                return y
        except:
            continue
    return None

df_books['pub_year'] = df_books['details'].apply(extract_year)

books_with_year = df_books[df_books['pub_year'].notna()].copy()
books_with_year['pub_year'] = books_with_year['pub_year'].astype(int)

# stats
info = {
    'total_books': int(len(df_books)),
    'books_with_year_count': int(len(books_with_year)),
    'books_with_year_sample_ids': list(books_with_year['book_id'].astype(str).unique()[:20]),
    'books_with_year_id_nums_sample': list(map(int, books_with_year['id_num'].dropna().astype(int).unique()[:20])),
    'total_reviews': int(len(df_reviews)),
    'reviews_id_nums_sample': list(map(str, df_reviews['id_num'].dropna().unique()[:20])),
    'intersection_id_nums_count': int(len(set(books_with_year['id_num'].dropna().astype(int)).intersection(set(df_reviews['id_num'].dropna().astype(int))))),
}
print('__RESULT__:')
print(json.dumps(info))"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json', 'var_call_aR6UX9hpPPFJp9mKhHqshRo4': {'error': 'No matched reviews and books after fuzzy numeric id join.'}, 'var_call_kZWI5G5YvvZNgvtJ34upADAx': {'books_total': 200, 'reviews_total': 1833, 'books_with_num': 200, 'reviews_with_num': 200, 'books_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'reviews_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'intersection_count': 200, 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_76', 'purchaseid_115', 'purchaseid_167', 'purchaseid_188', 'purchaseid_23', 'purchaseid_196', 'purchaseid_3', 'purchaseid_48', 'purchaseid_154', 'purchaseid_99', 'purchaseid_169', 'purchaseid_145', 'purchaseid_194', 'purchaseid_81', 'purchaseid_199']}, 'var_call_tZT56yqXTJfyWBmH174CmQyu': {'error': 'No matched reviews and books after join.'}}

exec(code, env_args)
