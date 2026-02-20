code = """import json
import pandas as pd
import re
with open(var_call_fCXKjFuQR0KVnKs5USPd527y,'r',encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_0WiZXUQS5sLYvZ5ccFLAWezZ,'r',encoding='utf-8') as f:
    reviews = json.load(f)
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)
# extract numeric
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)')
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)')
# convert
b_ids = df_books['id_num'].dropna().astype(int)
r_ids = df_reviews['id_num'].dropna().astype(int)

info = {
    'books_total': len(df_books),
    'reviews_total': len(df_reviews),
    'books_with_num': int(b_ids.nunique()),
    'reviews_with_num': int(r_ids.nunique()),
    'books_num_min_max_sample': [int(b_ids.min()) if not b_ids.empty else None, int(b_ids.max()) if not b_ids.empty else None, list(sorted(b_ids.unique())[:10])],
    'reviews_num_min_max_sample': [int(r_ids.min()) if not r_ids.empty else None, int(r_ids.max()) if not r_ids.empty else None, list(sorted(r_ids.unique())[:10])],
    'intersection_count': int(len(set(b_ids.unique()).intersection(set(r_ids.unique())))),
    'sample_book_ids': list(df_books['book_id'].astype(str).unique()[:20]),
    'sample_purchase_ids': list(df_reviews['purchase_id'].astype(str).unique()[:20])
}

import json
print('__RESULT__:')
print(json.dumps(info))"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json', 'var_call_aR6UX9hpPPFJp9mKhHqshRo4': {'error': 'No matched reviews and books after fuzzy numeric id join.'}}

exec(code, env_args)
