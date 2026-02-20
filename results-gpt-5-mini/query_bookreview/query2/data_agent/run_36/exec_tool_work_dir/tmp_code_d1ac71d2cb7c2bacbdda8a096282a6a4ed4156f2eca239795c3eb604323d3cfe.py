code = """import json
import re
import pandas as pd

# Load books_info result from file path stored in var_call_PD9yoSoDykFAhkL2kOZsqvLk
with open(var_call_PD9yoSoDykFAhkL2kOZsqvLk, 'r') as f:
    books = json.load(f)

reviews = var_call_Unnb2Yq7sGiFLA7Q1iiYIAIG

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize types
if 'book_id' not in df_books.columns:
    df_books['book_id'] = df_books.get('bookid', None)

# Extract numeric suffix
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

if 'book_id' in df_books.columns:
    df_books['num_id'] = df_books['book_id'].apply(extract_num)
else:
    df_books['num_id'] = None

if 'purchase_id' in df_reviews.columns:
    df_reviews['num_id'] = df_reviews['purchase_id'].apply(extract_num)
else:
    df_reviews['num_id'] = None

# Convert avg_rating and rating_count to numeric
df_reviews['avg_rating'] = pd.to_numeric(df_reviews['avg_rating'], errors='coerce')
df_reviews['rating_count'] = pd.to_numeric(df_reviews['rating_count'], errors='coerce')

# Filter reviews with avg_rating == 5.0
df_reviews_5 = df_reviews[df_reviews['avg_rating'] == 5.0]

# Merge on numeric id
merged = pd.merge(df_books, df_reviews_5, on='num_id', how='inner', suffixes=('_book','_review'))

# Filter for Literature & Fiction in categories and English in details
def contains_lit(cat):
    if not isinstance(cat, str):
        return False
    return 'literature & fiction' in cat.lower() or 'literature' in cat.lower()

def contains_english(details):
    if not isinstance(details, str):
        return False
    return 'english' in details.lower()

merged['is_lit'] = merged['categories'].apply(contains_lit)
merged['is_english'] = merged['details'].apply(contains_english)

final = merged[merged['is_lit'] & merged['is_english']]

# Prepare output
output = []
for _, row in final.iterrows():
    entry = {
        'title': row.get('title'),
        'book_id': row.get('book_id'),
        'purchase_id': row.get('purchase_id'),
        'avg_rating': float(row.get('avg_rating')) if pd.notnull(row.get('avg_rating')) else None,
        'rating_count': int(row.get('rating_count')) if pd.notnull(row.get('rating_count')) else None,
        'categories': row.get('categories'),
        'details': row.get('details')
    }
    output.append(entry)

# If none found, return empty list
result_str = json.dumps(output)
print("__RESULT__:")
print(result_str)"""

env_args = {'var_call_PD9yoSoDykFAhkL2kOZsqvLk': 'file_storage/call_PD9yoSoDykFAhkL2kOZsqvLk.json', 'var_call_Unnb2Yq7sGiFLA7Q1iiYIAIG': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'rating_count': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'rating_count': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'rating_count': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'rating_count': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'rating_count': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'rating_count': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'rating_count': '1'}]}

exec(code, env_args)
