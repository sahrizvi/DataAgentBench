code = """import json
import pandas as pd
import re

# Load books data from the JSON file path stored in var_call_AgqdjLi4csioiZPzXjbMqEqC
books_path = var_call_AgqdjLi4csioiZPzXjbMqEqC
with open(books_path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# Load reviews aggregate data from var_call_kzi0CC988opqHd9LL3IDSpkl
reviews_data = var_call_kzi0CC988opqHd9LL3IDSpkl

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Normalize types
if 'avg_rating' in df_reviews.columns:
    df_reviews['avg_rating'] = pd.to_numeric(df_reviews['avg_rating'], errors='coerce')
if 'review_count' in df_reviews.columns:
    df_reviews['review_count'] = pd.to_numeric(df_reviews['review_count'], errors='coerce')

# Extract numeric id from book_id and purchase_id
def extract_number(s):
    if pd.isna(s):
        return None
    m = re.search(r"(\d+)", str(s))
    return int(m.group(1)) if m else None

if 'book_id' in df_books.columns:
    df_books['book_num'] = df_books['book_id'].apply(extract_number)
else:
    df_books['book_num'] = None

if 'purchase_id' in df_reviews.columns:
    df_reviews['book_num'] = df_reviews['purchase_id'].apply(extract_number)
else:
    df_reviews['book_num'] = None

# Merge on book_num
merged = pd.merge(df_books, df_reviews, on='book_num', how='inner', suffixes=('_book', '_rev'))

# Filter avg_rating >= 4.5
filtered = merged[merged['avg_rating'] >= 4.5]

# Prepare output list of dicts with title, book_id, purchase_id, avg_rating, review_count
output = []
for _, row in filtered.iterrows():
    output.append({
        'title': row.get('title'),
        'book_id': row.get('book_id'),
        'purchase_id': row.get('purchase_id'),
        'avg_rating': float(row.get('avg_rating')) if pd.notna(row.get('avg_rating')) else None,
        'review_count': int(row.get('review_count')) if pd.notna(row.get('review_count')) else None
    })

# Sort output by avg_rating desc then review_count desc
output = sorted(output, key=lambda x: (-(x['avg_rating'] if x['avg_rating'] is not None else 0), -(x['review_count'] if x['review_count'] is not None else 0)))

import json
print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_bKrXUWQ0xEXm9uubtfcOYPoI': ['books_info'], 'var_call_GL4qxIYE6Bj4SlMjA1UXloOA': ['review'], 'var_call_AgqdjLi4csioiZPzXjbMqEqC': 'file_storage/call_AgqdjLi4csioiZPzXjbMqEqC.json', 'var_call_kzi0CC988opqHd9LL3IDSpkl': [{'purchase_id': 'purchaseid_96', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_94', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'review_count': '14'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'review_count': '8'}, {'purchase_id': 'purchaseid_66', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_55', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_46', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_4', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_37', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_3', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_22', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_200', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_198', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_196', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_187', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_185', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_169', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_154', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_129', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_10', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_13', 'avg_rating': '4.923076923076923', 'review_count': '13'}, {'purchase_id': 'purchaseid_149', 'avg_rating': '4.9', 'review_count': '10'}, {'purchase_id': 'purchaseid_178', 'avg_rating': '4.795918367346939', 'review_count': '49'}, {'purchase_id': 'purchaseid_76', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_48', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_115', 'avg_rating': '4.75', 'review_count': '8'}, {'purchase_id': 'purchaseid_8', 'avg_rating': '4.709677419354839', 'review_count': '31'}, {'purchase_id': 'purchaseid_158', 'avg_rating': '4.708333333333333', 'review_count': '24'}, {'purchase_id': 'purchaseid_72', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_50', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_23', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_161', 'avg_rating': '4.5', 'review_count': '2'}]}

exec(code, env_args)
