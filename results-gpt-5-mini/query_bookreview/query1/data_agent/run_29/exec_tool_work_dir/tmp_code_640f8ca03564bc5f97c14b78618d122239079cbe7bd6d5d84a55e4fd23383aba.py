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
# drop rows without numeric
df_books = df_books[df_books['id_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['id_num'].notna()].copy()
# convert to int
df_books['id_num'] = df_books['id_num'].astype(int)
df_reviews['id_num'] = df_reviews['id_num'].astype(int)

# Extract publication year: take the latest year found in details within range
year_re = re.compile(r'(18\d{2}|19\d{2}|20\d{2})')

def extract_year(text):
    if not isinstance(text, str):
        return None
    matches = year_re.findall(text)
    if not matches:
        return None
    years = []
    for m in matches:
        try:
            y = int(m)
            if 1800 <= y <= 2023:
                years.append(y)
        except:
            continue
    if not years:
        return None
    # choose the most recent year as publication year
    return max(years)

df_books['pub_year'] = df_books['details'].apply(extract_year)
# Drop books without pub_year
df_books = df_books[df_books['pub_year'].notna()].copy()
df_books['pub_year'] = df_books['pub_year'].astype(int)
# Create decade label
df_books['decade'] = (df_books['pub_year'] // 10 * 10).astype(int).astype(str) + 's'

# Clean ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

# Merge
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))

if merged.empty:
    out = {"error": "No matched reviews and books after join."}
    print('__RESULT__:')
    print(json.dumps(out))
else:
    # Compute per-book average rating
    book_avg = merged.groupby(['book_id','decade'], as_index=False)['rating'].mean()
    # Per-decade stats
    per_decade = book_avg.groupby('decade', as_index=False).agg(book_count=('book_id','nunique'), average_rating=('rating','mean'))
    # Filter decades with at least 10 distinct books
    per_decade = per_decade[per_decade['book_count'] >= 10].copy()
    if per_decade.empty:
        out = {"error": "No decade has at least 10 distinct rated books."}
        print('__RESULT__:')
        print(json.dumps(out))
    else:
        # choose decade with highest average_rating, tie-breaker by decade ascending
        per_decade = per_decade.sort_values(['average_rating','decade'], ascending=[False, True]).reset_index(drop=True)
        best = per_decade.iloc[0]
        out = {"decade": str(best['decade']), "average_rating": round(float(best['average_rating']),4), "book_count": int(best['book_count'])}
        print('__RESULT__:')
        print(json.dumps(out))"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json', 'var_call_aR6UX9hpPPFJp9mKhHqshRo4': {'error': 'No matched reviews and books after fuzzy numeric id join.'}, 'var_call_kZWI5G5YvvZNgvtJ34upADAx': {'books_total': 200, 'reviews_total': 1833, 'books_with_num': 200, 'reviews_with_num': 200, 'books_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'reviews_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'intersection_count': 200, 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_76', 'purchaseid_115', 'purchaseid_167', 'purchaseid_188', 'purchaseid_23', 'purchaseid_196', 'purchaseid_3', 'purchaseid_48', 'purchaseid_154', 'purchaseid_99', 'purchaseid_169', 'purchaseid_145', 'purchaseid_194', 'purchaseid_81', 'purchaseid_199']}, 'var_call_tZT56yqXTJfyWBmH174CmQyu': {'error': 'No matched reviews and books after join.'}, 'var_call_VVrmJaDl400FEdaox2BPvYVq': {'total_books': 200, 'books_with_year_count': 0, 'books_with_year_sample_ids': [], 'books_with_year_id_nums_sample': [], 'total_reviews': 1833, 'reviews_id_nums_sample': ['186', '191', '190', '8', '178', '76', '115', '167', '188', '23', '196', '3', '48', '154', '99', '169', '145', '194', '81', '199'], 'intersection_id_nums_count': 0}, 'var_call_iwBj8ZLRGYPRVbQUAO30M7xd': 'file_storage/call_iwBj8ZLRGYPRVbQUAO30M7xd.json', 'var_call_zpOQd00sbY4ONSoInB2NGDof': {'sample': [{'book_id': 'bookid_1', 'years_found': ['2004']}, {'book_id': 'bookid_2', 'years_found': ['1996']}, {'book_id': 'bookid_3', 'years_found': ['1853', '2012']}, {'book_id': 'bookid_4', 'years_found': ['2013']}, {'book_id': 'bookid_5', 'years_found': ['2014']}, {'book_id': 'bookid_6', 'years_found': ['2021']}, {'book_id': 'bookid_7', 'years_found': ['1994', '2004']}, {'book_id': 'bookid_8', 'years_found': ['2015']}, {'book_id': 'bookid_9', 'years_found': ['2019']}, {'book_id': 'bookid_10', 'years_found': ['1932', '2004']}, {'book_id': 'bookid_11', 'years_found': ['1993']}, {'book_id': 'bookid_12', 'years_found': ['2022']}, {'book_id': 'bookid_13', 'years_found': ['2023']}, {'book_id': 'bookid_14', 'years_found': ['2019']}, {'book_id': 'bookid_15', 'years_found': ['2000']}, {'book_id': 'bookid_16', 'years_found': ['1997']}, {'book_id': 'bookid_17', 'years_found': ['1987']}, {'book_id': 'bookid_18', 'years_found': ['2012']}, {'book_id': 'bookid_19', 'years_found': ['2013']}, {'book_id': 'bookid_20', 'years_found': ['2003']}, {'book_id': 'bookid_21', 'years_found': ['1945']}, {'book_id': 'bookid_22', 'years_found': ['2006']}, {'book_id': 'bookid_23', 'years_found': ['2021']}, {'book_id': 'bookid_24', 'years_found': ['1939']}, {'book_id': 'bookid_25', 'years_found': []}, {'book_id': 'bookid_32', 'years_found': ['1852', '1998']}, {'book_id': 'bookid_26', 'years_found': ['1995']}, {'book_id': 'bookid_27', 'years_found': ['1939']}, {'book_id': 'bookid_28', 'years_found': ['1995']}, {'book_id': 'bookid_29', 'years_found': ['1929', '2017']}, {'book_id': 'bookid_30', 'years_found': ['2016']}, {'book_id': 'bookid_31', 'years_found': ['2012']}, {'book_id': 'bookid_33', 'years_found': ['2016']}, {'book_id': 'bookid_34', 'years_found': ['1983']}, {'book_id': 'bookid_35', 'years_found': ['2006']}, {'book_id': 'bookid_36', 'years_found': ['1945', '2018']}, {'book_id': 'bookid_37', 'years_found': ['2011']}, {'book_id': 'bookid_38', 'years_found': ['1947', '2019']}, {'book_id': 'bookid_56', 'years_found': ['1835', '2012']}, {'book_id': 'bookid_39', 'years_found': ['2019', '2023']}, {'book_id': 'bookid_40', 'years_found': ['2012']}, {'book_id': 'bookid_41', 'years_found': ['1916', '2019']}, {'book_id': 'bookid_42', 'years_found': ['2018']}, {'book_id': 'bookid_43', 'years_found': ['2015']}, {'book_id': 'bookid_62', 'years_found': ['1981', '2016']}, {'book_id': 'bookid_44', 'years_found': ['2019']}, {'book_id': 'bookid_45', 'years_found': ['2016']}, {'book_id': 'bookid_46', 'years_found': ['2017']}, {'book_id': 'bookid_47', 'years_found': ['1986']}, {'book_id': 'bookid_48', 'years_found': ['2014']}], 'books_with_year_count': 192}}

exec(code, env_args)
