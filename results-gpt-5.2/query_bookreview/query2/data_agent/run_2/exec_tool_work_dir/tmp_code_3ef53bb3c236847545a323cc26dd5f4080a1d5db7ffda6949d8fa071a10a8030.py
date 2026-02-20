code = """import json, pandas as pd

# Load books (Lit & Fiction)
books_src = var_call_qte2P0KN26eAMIC0A3Ai815W
if isinstance(books_src, str):
    with open(books_src, 'r') as f:
        books = json.load(f)
else:
    books = books_src

# Load english details ids
eng_src = var_call_YYtqDzqkoDP21c3naPKVIwGp
if isinstance(eng_src, str):
    with open(eng_src, 'r') as f:
        eng = json.load(f)
else:
    eng = eng_src

# perfect avg rating purchase_ids
perfect = var_call_AeyGEJvEK2YmX0VJVkcMRc4x

df_books = pd.DataFrame(books)
df_eng = pd.DataFrame(eng)
df_perfect = pd.DataFrame(perfect)

# English-language: details contains 'written in English' or 'available in English'
# (already filtered by SQL ILIKE '%English%'; keep those that include english wording)
mask_eng = df_eng['details'].str.contains(r'\\bEnglish\\b', case=False, na=False)
eng_ids = set(df_eng.loc[mask_eng, 'book_id'])

# Fuzzy join: bookid_### <-> purchaseid_### by extracting trailing integer
import re

def trailing_num(s):
    if s is None:
        return None
    m = re.search(r'(\\d+)\s*$', str(s))
    return int(m.group(1)) if m else None

df_books['num'] = df_books['book_id'].map(trailing_num)
df_perfect['num'] = df_perfect['purchase_id'].map(trailing_num)

merged = df_books.merge(df_perfect[['purchase_id','avg_rating','review_count','num']], on='num', how='inner')
merged = merged[merged['book_id'].isin(eng_ids)]

# Ensure category is exactly Literature & Fiction present
merged = merged[merged['categories'].str.contains('Literature & Fiction', na=False)]

# Format output
merged['avg_rating'] = merged['avg_rating'].astype(float)
merged['review_count'] = merged['review_count'].astype(int)

out = merged.sort_values(['title','book_id'])[['book_id','title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_qte2P0KN26eAMIC0A3Ai815W': 'file_storage/call_qte2P0KN26eAMIC0A3Ai815W.json', 'var_call_AeyGEJvEK2YmX0VJVkcMRc4x': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'review_count': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'review_count': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'review_count': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'review_count': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'review_count': '1'}], 'var_call_YYtqDzqkoDP21c3naPKVIwGp': 'file_storage/call_YYtqDzqkoDP21c3naPKVIwGp.json'}

exec(code, env_args)
