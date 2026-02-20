code = """import json
import pandas as pd
# Load review results from storage
reviews = var_call_WZ0tJcOgqQ6JH0SYEy5rjTcp

# Load books_info filtered results from JSON file path provided
books_file = var_call_OTD7Lr6CMqipL9C1R3DEz02E
with open(books_file, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Create DataFrames
df_reviews = pd.DataFrame(reviews)
# Ensure strings
if not df_reviews.empty:
    df_reviews['purchase_id'] = df_reviews['purchase_id'].astype(str)

# Extract numeric id from purchase_id (e.g., 'purchaseid_101' -> '101')
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r"(\d+)$")

df_books = pd.DataFrame(books)
# Ensure book_id is string
if not df_books.empty:
    df_books['book_id'] = df_books['book_id'].astype(str)

# Extract numeric id from book_id (e.g., 'bookid_101' -> '101')
df_books['id_num'] = df_books['book_id'].str.extract(r"(\d+)$")

# Merge on numeric id
merged = pd.merge(df_books, df_reviews, on='id_num', how='inner')

# Prepare output list of dicts with relevant fields
output = []
for _, row in merged.iterrows():
    output.append({
        'purchase_id': row['purchase_id'],
        'book_id': row['book_id'],
        'title': row.get('title', None),
        'categories': row.get('categories', None),
        'details': row.get('details', None),
        'avg_rating': float(row.get('avg_rating')) if row.get('avg_rating') is not None else None,
        'n_reviews': int(row.get('n_reviews')) if row.get('n_reviews') is not None else None
    })

# Sort output by purchase_id for consistency
output = sorted(output, key=lambda x: x['purchase_id'])

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_faAR3C8VfZbJDvgPLKNpQsKq': ['books_info'], 'var_call_chR7RlGNiZbOLvSLxZVY66sD': ['review'], 'var_call_WZ0tJcOgqQ6JH0SYEy5rjTcp': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'n_reviews': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'n_reviews': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'n_reviews': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'n_reviews': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'n_reviews': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'n_reviews': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'n_reviews': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'n_reviews': '1'}], 'var_call_G0H0udD2ER98B941TnUkHHnC': [], 'var_call_s2zRlEGOjniqRkCfucv8Jegj': 'file_storage/call_s2zRlEGOjniqRkCfucv8Jegj.json', 'var_call_OTD7Lr6CMqipL9C1R3DEz02E': 'file_storage/call_OTD7Lr6CMqipL9C1R3DEz02E.json'}

exec(code, env_args)
