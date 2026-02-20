code = """import json, re, pandas as pd

# load books details
books_src = var_call_hdAFFJSz2ZQuh0EomTsoOSaa
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# load reviews ratings
rev_src = var_call_m8Tbbj9OFVsM37AbcqbBB2Pa
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = rev_src

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# parse year from details
year_re = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if s is None:
        return None
    s = str(s)
    # try patterns around Published/published/released/on
    m = year_re.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2030:
        return y
    return None

books_df['year'] = books_df['details'].map(extract_year)
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade'] = (books_df['year']//10)*10

# fuzzy join: purchaseid_X -> bookid_X
# extract trailing integer
books_df['id_num'] = books_df['book_id'].str.extract(r'(\d+)$')[0].astype('Int64')
reviews_df['id_num'] = reviews_df['purchase_id'].astype(str).str.extract(r'(\d+)$')[0].astype('Int64')

# keep valid ratings
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating','id_num'])
books_df = books_df.dropna(subset=['id_num'])

merged = reviews_df.merge(books_df[['id_num','book_id','decade']], on='id_num', how='inner')

# decades with at least 10 distinct rated books
by_decade = merged.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('book_id','nunique')
).reset_index()

eligible = by_decade[by_decade['distinct_books']>=10].copy()
if eligible.empty:
    out = None
else:
    top = eligible.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    out = f"{int(top['decade'])}s"

print('__RESULT__:')
print(json.dumps({'decade': out}))"""

env_args = {'var_call_5GwQIA9lJvaLdC1pxvwOfj0M': 'file_storage/call_5GwQIA9lJvaLdC1pxvwOfj0M.json', 'var_call_m8Tbbj9OFVsM37AbcqbBB2Pa': 'file_storage/call_m8Tbbj9OFVsM37AbcqbBB2Pa.json', 'var_call_CMChKnAtqVx5m6zmgYZb0x1b': 'file_storage/call_CMChKnAtqVx5m6zmgYZb0x1b.json', 'var_call_oRv2lUQX8g2esK3PgnIImSNm': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-02-20 16:09:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2020-02-27 05:11:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-01-06 07:52:00'}, {'purchase_id': 'purchaseid_115', 'rating': '5', 'review_time': '2019-07-24 13:29:00'}, {'purchase_id': 'purchaseid_167', 'rating': '2', 'review_time': '2020-06-01 07:33:00'}, {'purchase_id': 'purchaseid_188', 'rating': '1', 'review_time': '2016-01-25 19:03:00'}, {'purchase_id': 'purchaseid_23', 'rating': '5', 'review_time': '2021-07-31 18:34:00'}, {'purchase_id': 'purchaseid_196', 'rating': '5', 'review_time': '2013-05-21 13:42:00'}, {'purchase_id': 'purchaseid_196', 'rating': '5', 'review_time': '2013-02-27 19:49:00'}, {'purchase_id': 'purchaseid_3', 'rating': '5', 'review_time': '2014-10-24 10:52:00'}, {'purchase_id': 'purchaseid_48', 'rating': '5', 'review_time': '2015-11-10 10:51:00'}, {'purchase_id': 'purchaseid_154', 'rating': '3', 'review_time': '2018-09-04 11:04:00'}, {'purchase_id': 'purchaseid_99', 'rating': '2', 'review_time': '2021-01-27 07:08:00'}, {'purchase_id': 'purchaseid_190', 'rating': '5', 'review_time': '2013-02-05 06:53:00'}, {'purchase_id': 'purchaseid_3', 'rating': '5', 'review_time': '2013-02-18 04:04:00'}, {'purchase_id': 'purchaseid_169', 'rating': '5', 'review_time': '2014-07-12 19:16:00'}, {'purchase_id': 'purchaseid_3', 'rating': '5', 'review_time': '2015-03-07 04:30:00'}, {'purchase_id': 'purchaseid_145', 'rating': '5', 'review_time': '2015-12-18 05:07:00'}, {'purchase_id': 'purchaseid_194', 'rating': '4', 'review_time': '2017-08-24 14:29:00'}, {'purchase_id': 'purchaseid_81', 'rating': '5', 'review_time': '2018-12-19 14:40:00'}, {'purchase_id': 'purchaseid_199', 'rating': '1', 'review_time': '2019-09-09 10:16:00'}, {'purchase_id': 'purchaseid_48', 'rating': '5', 'review_time': '2016-03-10 20:11:00'}, {'purchase_id': 'purchaseid_96', 'rating': '5', 'review_time': '2018-12-22 04:31:00'}, {'purchase_id': 'purchaseid_167', 'rating': '4', 'review_time': '2020-06-14 11:52:00'}, {'purchase_id': 'purchaseid_196', 'rating': '5', 'review_time': '2019-04-27 18:20:00'}, {'purchase_id': 'purchaseid_196', 'rating': '5', 'review_time': '2019-03-27 13:46:00'}, {'purchase_id': 'purchaseid_196', 'rating': '4', 'review_time': '2017-02-08 09:44:00'}, {'purchase_id': 'purchaseid_148', 'rating': '5', 'review_time': '2012-06-25 09:52:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2017-03-13 20:33:04'}, {'purchase_id': 'purchaseid_145', 'rating': '5', 'review_time': '2016-08-06 10:31:00'}, {'purchase_id': 'purchaseid_200', 'rating': '5', 'review_time': '2015-11-28 11:40:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2017-11-07 10:11:54'}, {'purchase_id': 'purchaseid_178', 'rating': '1', 'review_time': '2015-06-27 14:34:00'}, {'purchase_id': 'purchaseid_20', 'rating': '5', 'review_time': '2021-10-31 19:46:00'}, {'purchase_id': 'purchaseid_52', 'rating': '5', 'review_time': '2019-12-05 14:52:00'}, {'purchase_id': 'purchaseid_159', 'rating': '2', 'review_time': '2018-04-28 14:09:00'}, {'purchase_id': 'purchaseid_83', 'rating': '5', 'review_time': '2021-06-22 12:04:00'}, {'purchase_id': 'purchaseid_67', 'rating': '3', 'review_time': '2021-02-10 16:28:00'}, {'purchase_id': 'purchaseid_3', 'rating': '5', 'review_time': '2017-02-02 06:42:00'}, {'purchase_id': 'purchaseid_58', 'rating': '4', 'review_time': '2018-04-21 01:04:00'}, {'purchase_id': 'purchaseid_196', 'rating': '4', 'review_time': '2014-05-28 09:10:00'}, {'purchase_id': 'purchaseid_95', 'rating': '5', 'review_time': '2019-08-02 19:18:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2015-01-09 10:37:00'}, {'purchase_id': 'purchaseid_3', 'rating': '3', 'review_time': '2012-08-09 07:16:00'}, {'purchase_id': 'purchaseid_62', 'rating': '5', 'review_time': '2020-04-16 04:41:00'}], 'var_call_MHsFSexGPc4X6ymUxqEh3Ou7': [{'n': '200'}], 'var_call_oYI3luYlZq1cUSaKLKcUofAR': [{'n': '1833'}], 'var_call_hdAFFJSz2ZQuh0EomTsoOSaa': 'file_storage/call_hdAFFJSz2ZQuh0EomTsoOSaa.json'}

exec(code, env_args)
