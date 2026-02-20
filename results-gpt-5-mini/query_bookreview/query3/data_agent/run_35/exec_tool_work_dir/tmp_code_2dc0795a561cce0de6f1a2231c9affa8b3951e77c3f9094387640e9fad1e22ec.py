code = """import json
import pandas as pd

# Load reviews result from earlier query
reviews = var_call_ff9OeC20xSPWAqjQLEVnT1RG
# Convert types
for r in reviews:
    r['avg_rating'] = float(r['avg_rating'])
    r['review_count'] = int(r['review_count'])

# Create corresponding book_ids by replacing prefix
bookids = set([r['purchase_id'].replace('purchaseid_', 'bookid_') for r in reviews])

# Load books data from file path
with open(var_call_af1nrptxPZKP337Vyj5zp4zU, 'r') as f:
    books = json.load(f)

df_books = pd.DataFrame(books)
# Ensure columns exist
if 'book_id' not in df_books.columns:
    df_books['book_id'] = df_books.get('bookid', None)

# Filter books that match our bookids
df_match = df_books[df_books['book_id'].isin(bookids)].copy()

# Map reviews to bookids
map_review = {r['purchase_id'].replace('purchaseid_', 'bookid_'):{'avg_rating':r['avg_rating'],'review_count':r['review_count'],'purchase_id':r['purchase_id']} for r in reviews}

result = []
for _, row in df_match.iterrows():
    bid = row['book_id']
    rev = map_review.get(bid, {})
    entry = {
        'book_id': bid,
        'title': row.get('title'),
        'purchase_id': rev.get('purchase_id'),
        'avg_rating': rev.get('avg_rating'),
        'review_count': rev.get('review_count'),
        'categories': row.get('categories'),
        'details': row.get('details')
    }
    result.append(entry)

# Sort results
result_sorted = sorted(result, key=lambda x: (-x['avg_rating'] if x['avg_rating'] is not None else 0, -x['review_count'] if x['review_count'] is not None else 0, x.get('title') or ''))

# Output as JSON string
print("__RESULT__:")
print(json.dumps(result_sorted))"""

env_args = {'var_call_ff9OeC20xSPWAqjQLEVnT1RG': [{'purchase_id': 'purchaseid_10', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_115', 'avg_rating': '4.75', 'review_count': '8'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_129', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_13', 'avg_rating': '4.923076923076923', 'review_count': '13'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_149', 'avg_rating': '4.9', 'review_count': '10'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_154', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_158', 'avg_rating': '4.708333333333333', 'review_count': '24'}, {'purchase_id': 'purchaseid_161', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_169', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_178', 'avg_rating': '4.795918367346939', 'review_count': '49'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_185', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_187', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_196', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_198', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_200', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_22', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_23', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_3', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_37', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_4', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_46', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_48', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_50', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_55', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_66', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_72', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'review_count': '8'}, {'purchase_id': 'purchaseid_76', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_8', 'avg_rating': '4.709677419354839', 'review_count': '31'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'review_count': '14'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_94', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_96', 'avg_rating': '5.0', 'review_count': '1'}], 'var_call_jSfqwcnzB7YyUgDb4Ha1FtA4': [], 'var_call_af1nrptxPZKP337Vyj5zp4zU': 'file_storage/call_af1nrptxPZKP337Vyj5zp4zU.json'}

exec(code, env_args)
