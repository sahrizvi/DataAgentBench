code = """import json
import pandas as pd
import re

# Load tool results from storage paths
reviews_path = var_call_WA9ZvasR1bQ4LoatRVl7cuxP
books_path = var_call_EksPnBh5hXxFRRXu6PJ2q2yh

with open(reviews_path, 'r') as f:
    reviews = json.load(f)
with open(books_path, 'r') as f:
    books = json.load(f)

rev_df = pd.DataFrame(reviews)
books_df = pd.DataFrame(books)

# Ensure rating numeric
rev_df = rev_df[rev_df['purchase_id'].notnull()]
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['rating'])

# Map purchase_id to book_id by replacing prefix
rev_df['book_id'] = rev_df['purchase_id'].str.replace('purchaseid_', 'bookid_', regex=False)

# Extract year from books details
year_list = []
pattern = re.compile(r'\b(1[5-9]\d{2}|20\d{2})\b')
for det in books_df['details'].fillna(''):
    years = pattern.findall(det)
    yr = None
    if years:
        # years may be tuples if grouped; ensure flatten
        # pattern returns full match strings
        for y in years:
            try:
                yint = int(y)
            except:
                continue
            if 1500 <= yint <= 2023:
                yr = yint
                break
    year_list.append(yr)

books_df['pub_year'] = year_list
books_df = books_df[books_df['pub_year'].notnull()]
books_df['pub_year'] = books_df['pub_year'].astype(int)
books_df['decade'] = (books_df['pub_year'] // 10 * 10).astype(int).astype(str) + 's'

# Merge reviews with books on book_id
merged = pd.merge(rev_df, books_df[['book_id','decade']], on='book_id', how='inner')

# Compute per-book average rating
book_avg = merged.groupby('book_id', as_index=False)['rating'].mean()
# Attach decade
book_decade = pd.merge(book_avg, books_df[['book_id','decade']], on='book_id', how='left')

# For each decade compute number of distinct books and average of book averages
decade_stats = book_decade.groupby('decade').agg(books_count=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()
# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['books_count'] >= 10]

if decade_stats_filtered.empty:
    result = {'decade': None, 'average_rating': None, 'books_count': 0}
else:
    # Find decade with highest avg_rating
    best = decade_stats_filtered.sort_values(['avg_rating','books_count'], ascending=[False, False]).iloc[0]
    result = {'decade': best['decade'], 'average_rating': round(float(best['avg_rating']), 3), 'books_count': int(best['books_count'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_Cqm604gY8ZrAfZDetqWopI8c': ['books_info'], 'var_call_tMVCoftQ84MDpkJMialTtAyU': ['review'], 'var_call_3kxvGCZr7reGz9xhPVRmqpGF': [{'purchase_id': 'purchaseid_1', 'cnt': '1', 'first_review': '2014-11-24 09:03:00', 'last_review': '2014-11-24 09:03:00'}, {'purchase_id': 'purchaseid_10', 'cnt': '40', 'first_review': '2010-07-04 17:56:08', 'last_review': '2021-07-31 11:44:00'}, {'purchase_id': 'purchaseid_100', 'cnt': '3', 'first_review': '2008-01-13 05:32:00', 'last_review': '2015-10-10 10:19:00'}, {'purchase_id': 'purchaseid_101', 'cnt': '2', 'first_review': '2018-06-29 15:24:00', 'last_review': '2019-02-18 10:26:00'}, {'purchase_id': 'purchaseid_102', 'cnt': '1', 'first_review': '2019-10-21 16:43:00', 'last_review': '2019-10-21 16:43:00'}, {'purchase_id': 'purchaseid_103', 'cnt': '5', 'first_review': '2017-02-08 05:27:00', 'last_review': '2017-05-08 04:26:00'}, {'purchase_id': 'purchaseid_104', 'cnt': '3', 'first_review': '2012-03-04 18:00:00', 'last_review': '2015-01-09 07:11:00'}, {'purchase_id': 'purchaseid_105', 'cnt': '1', 'first_review': '2022-11-26 09:54:00', 'last_review': '2022-11-26 09:54:00'}, {'purchase_id': 'purchaseid_106', 'cnt': '10', 'first_review': '2005-07-17 16:09:00', 'last_review': '2012-12-27 16:07:00'}, {'purchase_id': 'purchaseid_107', 'cnt': '3', 'first_review': '2022-04-26 22:04:00', 'last_review': '2022-06-27 12:08:05'}, {'purchase_id': 'purchaseid_108', 'cnt': '3', 'first_review': '2021-09-01 08:22:00', 'last_review': '2022-06-02 09:48:00'}, {'purchase_id': 'purchaseid_109', 'cnt': '6', 'first_review': '2009-03-11 19:05:00', 'last_review': '2022-03-28 13:28:03'}, {'purchase_id': 'purchaseid_11', 'cnt': '1', 'first_review': '2021-04-13 09:55:28', 'last_review': '2021-04-13 09:55:28'}, {'purchase_id': 'purchaseid_110', 'cnt': '1', 'first_review': '2022-06-17 08:31:00', 'last_review': '2022-06-17 08:31:00'}, {'purchase_id': 'purchaseid_111', 'cnt': '6', 'first_review': '2014-12-04 08:32:00', 'last_review': '2016-05-15 05:08:00'}, {'purchase_id': 'purchaseid_112', 'cnt': '3', 'first_review': '2017-12-31 06:06:00', 'last_review': '2018-03-09 11:57:00'}, {'purchase_id': 'purchaseid_113', 'cnt': '1', 'first_review': '2013-11-14 11:37:00', 'last_review': '2013-11-14 11:37:00'}, {'purchase_id': 'purchaseid_114', 'cnt': '2', 'first_review': '2014-05-02 02:54:00', 'last_review': '2015-01-18 11:00:00'}, {'purchase_id': 'purchaseid_115', 'cnt': '17', 'first_review': '2019-07-24 13:29:00', 'last_review': '2023-03-16 13:03:00'}, {'purchase_id': 'purchaseid_116', 'cnt': '1', 'first_review': '2007-03-10 15:53:00', 'last_review': '2007-03-10 15:53:00'}, {'purchase_id': 'purchaseid_117', 'cnt': '2', 'first_review': '2015-06-18 13:17:00', 'last_review': '2015-09-12 11:52:00'}, {'purchase_id': 'purchaseid_118', 'cnt': '6', 'first_review': '2009-01-16 10:37:00', 'last_review': '2021-03-07 09:26:00'}, {'purchase_id': 'purchaseid_119', 'cnt': '2', 'first_review': '2012-11-18 16:23:00', 'last_review': '2013-05-30 05:22:00'}, {'purchase_id': 'purchaseid_12', 'cnt': '1', 'first_review': '2023-02-24 12:46:00', 'last_review': '2023-02-24 12:46:00'}, {'purchase_id': 'purchaseid_120', 'cnt': '1', 'first_review': '2015-12-30 12:33:00', 'last_review': '2015-12-30 12:33:00'}, {'purchase_id': 'purchaseid_121', 'cnt': '1', 'first_review': '2014-11-23 11:14:00', 'last_review': '2014-11-23 11:14:00'}, {'purchase_id': 'purchaseid_122', 'cnt': '1', 'first_review': '2022-09-17 13:59:00', 'last_review': '2022-09-17 13:59:00'}, {'purchase_id': 'purchaseid_123', 'cnt': '2', 'first_review': '2011-05-02 11:50:00', 'last_review': '2014-10-29 10:31:00'}, {'purchase_id': 'purchaseid_124', 'cnt': '4', 'first_review': '2019-08-27 10:49:00', 'last_review': '2019-09-14 12:36:00'}, {'purchase_id': 'purchaseid_125', 'cnt': '17', 'first_review': '2001-08-26 19:54:00', 'last_review': '2004-06-03 10:57:00'}, {'purchase_id': 'purchaseid_126', 'cnt': '1', 'first_review': '2021-02-07 06:44:00', 'last_review': '2021-02-07 06:44:00'}, {'purchase_id': 'purchaseid_127', 'cnt': '2', 'first_review': '2015-03-22 13:38:00', 'last_review': '2017-03-09 12:09:00'}, {'purchase_id': 'purchaseid_128', 'cnt': '2', 'first_review': '2011-03-05 07:58:00', 'last_review': '2013-04-05 09:20:00'}, {'purchase_id': 'purchaseid_129', 'cnt': '6', 'first_review': '2007-06-12 09:56:00', 'last_review': '2021-04-28 12:30:00'}, {'purchase_id': 'purchaseid_13', 'cnt': '13', 'first_review': '2023-01-29 04:17:00', 'last_review': '2023-05-16 17:49:00'}, {'purchase_id': 'purchaseid_130', 'cnt': '1', 'first_review': '2020-10-21 14:01:00', 'last_review': '2020-10-21 14:01:00'}, {'purchase_id': 'purchaseid_131', 'cnt': '3', 'first_review': '1999-11-09 15:17:59', 'last_review': '2016-12-31 11:32:00'}, {'purchase_id': 'purchaseid_132', 'cnt': '2', 'first_review': '2016-12-31 14:04:00', 'last_review': '2019-05-06 19:22:00'}, {'purchase_id': 'purchaseid_133', 'cnt': '1', 'first_review': '2014-02-04 11:26:00', 'last_review': '2014-02-04 11:26:00'}, {'purchase_id': 'purchaseid_134', 'cnt': '2', 'first_review': '2015-10-12 13:07:00', 'last_review': '2015-11-22 11:09:00'}, {'purchase_id': 'purchaseid_135', 'cnt': '7', 'first_review': '2013-10-03 18:37:00', 'last_review': '2019-11-02 10:59:00'}, {'purchase_id': 'purchaseid_136', 'cnt': '1', 'first_review': '2013-02-10 21:42:00', 'last_review': '2013-02-10 21:42:00'}, {'purchase_id': 'purchaseid_137', 'cnt': '1', 'first_review': '2020-01-14 14:23:00', 'last_review': '2020-01-14 14:23:00'}, {'purchase_id': 'purchaseid_138', 'cnt': '1', 'first_review': '2009-10-21 13:20:00', 'last_review': '2009-10-21 13:20:00'}, {'purchase_id': 'purchaseid_139', 'cnt': '1', 'first_review': '2019-10-05 19:37:00', 'last_review': '2019-10-05 19:37:00'}, {'purchase_id': 'purchaseid_14', 'cnt': '1', 'first_review': '2021-02-23 22:47:00', 'last_review': '2021-02-23 22:47:00'}, {'purchase_id': 'purchaseid_140', 'cnt': '4', 'first_review': '2020-12-13 13:55:11', 'last_review': '2021-09-04 22:40:00'}, {'purchase_id': 'purchaseid_141', 'cnt': '2', 'first_review': '2018-12-15 19:46:00', 'last_review': '2019-01-27 20:37:00'}, {'purchase_id': 'purchaseid_142', 'cnt': '3', 'first_review': '2005-03-20 15:31:00', 'last_review': '2017-06-06 02:39:00'}, {'purchase_id': 'purchaseid_143', 'cnt': '1', 'first_review': '2017-08-12 03:30:00', 'last_review': '2017-08-12 03:30:00'}], 'var_call_0I7tE5Cy8L4YSukfAiOrYxkX': 'file_storage/call_0I7tE5Cy8L4YSukfAiOrYxkX.json', 'var_call_WA9ZvasR1bQ4LoatRVl7cuxP': 'file_storage/call_WA9ZvasR1bQ4LoatRVl7cuxP.json', 'var_call_EksPnBh5hXxFRRXu6PJ2q2yh': 'file_storage/call_EksPnBh5hXxFRRXu6PJ2q2yh.json'}

exec(code, env_args)
