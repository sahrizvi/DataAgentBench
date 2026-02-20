code = """import json
import pandas as pd
# load the large books query result from file path stored in var_call_awyTttC9uudk2I5u4L1JPS7A
path = var_call_awyTttC9uudk2I5u4L1JPS7A
with open(path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# load reviews result (already a list variable)
reviews_data = var_call_rCdfvdn49R4T52iqAo28hPOp

# create dataframes
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# normalize types
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# compute average rating per purchase_id and counts
grp = df_reviews.groupby('purchase_id').agg(avg_rating=('rating','mean'), count=('rating','size')).reset_index()
# select those with perfect average 5.0
perfect = grp[grp['avg_rating']==5.0].copy()

# map purchase_id -> book_id by replacing prefix
perfect['book_id'] = perfect['purchase_id'].str.replace('purchaseid_','bookid_')

# filter books for Literature & Fiction and English language in details
def is_lit_and_english(cat, details):
    try:
        if pd.isna(cat):
            return False
        if 'Literature & Fiction' not in cat:
            return False
        if pd.isna(details):
            return False
        return 'english' in details.lower()
    except Exception:
        return False

books_map = df_books.copy()
books_map['is_lit_eng'] = books_map.apply(lambda r: is_lit_and_english(r.get('categories',''), r.get('details','')), axis=1)

# join
matched = pd.merge(perfect, books_map, on='book_id', how='left')
matched = matched[matched['is_lit_eng']==True]

# prepare output list
output = []
for _, row in matched.iterrows():
    output.append({
        'book_id': row.get('book_id'),
        'title': row.get('title'),
        'categories': row.get('categories'),
        'details': row.get('details'),
        'avg_rating': float(row.get('avg_rating')),
        'rating_count_in_reviews_table': int(row.get('count'))
    })

# remove duplicates
# convert to JSON
result_json = json.dumps(output)
print("__RESULT__:")
print(result_json)"""

env_args = {'var_call_awyTttC9uudk2I5u4L1JPS7A': 'file_storage/call_awyTttC9uudk2I5u4L1JPS7A.json', 'var_call_rCdfvdn49R4T52iqAo28hPOp': [{'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_23', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_190', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_169', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_81', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_96', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_148', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_200', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_20', 'rating': '5'}, {'purchase_id': 'purchaseid_52', 'rating': '5'}, {'purchase_id': 'purchaseid_83', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_95', 'rating': '5'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_10', 'rating': '5'}, {'purchase_id': 'purchaseid_10', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_46', 'rating': '5'}, {'purchase_id': 'purchaseid_38', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_10', 'rating': '5'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_7', 'rating': '5'}, {'purchase_id': 'purchaseid_4', 'rating': '5'}, {'purchase_id': 'purchaseid_162', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_5', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_6', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_5', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_46', 'rating': '5'}, {'purchase_id': 'purchaseid_83', 'rating': '5'}, {'purchase_id': 'purchaseid_86', 'rating': '5'}, {'purchase_id': 'purchaseid_174', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_177', 'rating': '5'}, {'purchase_id': 'purchaseid_187', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_33', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_10', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_157', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_187', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_13', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_42', 'rating': '5'}, {'purchase_id': 'purchaseid_96', 'rating': '5'}, {'purchase_id': 'purchaseid_73', 'rating': '5'}, {'purchase_id': 'purchaseid_188', 'rating': '5'}, {'purchase_id': 'purchaseid_97', 'rating': '5'}, {'purchase_id': 'purchaseid_59', 'rating': '5'}, {'purchase_id': 'purchaseid_192', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_99', 'rating': '5'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_163', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_52', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_106', 'rating': '5'}, {'purchase_id': 'purchaseid_130', 'rating': '5'}, {'purchase_id': 'purchaseid_118', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_5', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_154', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_32', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_41', 'rating': '5'}, {'purchase_id': 'purchaseid_36', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_124', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_32', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_148', 'rating': '5'}, {'purchase_id': 'purchaseid_197', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_41', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_5', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_83', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_12', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_46', 'rating': '5'}, {'purchase_id': 'purchaseid_140', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_166', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_85', 'rating': '5'}, {'purchase_id': 'purchaseid_94', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_194', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_187', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_90', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_133', 'rating': '5'}, {'purchase_id': 'purchaseid_160', 'rating': '5'}, {'purchase_id': 'purchaseid_20', 'rating': '5'}, {'purchase_id': 'purchaseid_148', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_161', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_181', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_185', 'rating': '5'}, {'purchase_id': 'purchaseid_195', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}, {'purchase_id': 'purchaseid_129', 'rating': '5'}, {'purchase_id': 'purchaseid_190', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_46', 'rating': '5'}, {'purchase_id': 'purchaseid_154', 'rating': '5'}, {'purchase_id': 'purchaseid_10', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_84', 'rating': '5'}, {'purchase_id': 'purchaseid_32', 'rating': '5'}, {'purchase_id': 'purchaseid_20', 'rating': '5'}, {'purchase_id': 'purchaseid_170', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '5'}, {'purchase_id': 'purchaseid_53', 'rating': '5'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '5'}]}

exec(code, env_args)
