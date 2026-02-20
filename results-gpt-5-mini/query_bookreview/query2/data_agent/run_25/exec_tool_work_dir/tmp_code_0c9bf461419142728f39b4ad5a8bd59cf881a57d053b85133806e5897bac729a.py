code = """import json,re
import pandas as pd

# Load the books data from the stored JSON file path
books_file_path = var_call_RKLyW9yeHfq3pGs9l7t8qAMn
with open(books_file_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Load reviews result directly from storage variable
reviews = var_call_r3JVcCpPXhEr3RyEP1auoD4t

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize column types
if 'book_id' not in df_books.columns:
    df_books['book_id'] = df_books.get('bookid', None)

# Extract numeric suffix for fuzzy join
def extract_num(s):
    if not isinstance(s, str):
        return None
    nums = re.findall(r"\d+", s)
    return int(nums[-1]) if nums else None

df_books['num_id'] = df_books['book_id'].apply(extract_num)
df_reviews['num_id'] = df_reviews['purchase_id'].apply(extract_num)

# Convert avg_rating and cnt to numeric
df_reviews['avg_rating'] = pd.to_numeric(df_reviews['avg_rating'], errors='coerce')
df_reviews['cnt'] = pd.to_numeric(df_reviews['cnt'], errors='coerce')

# Filter books for English language in details (case-insensitive)
df_books['is_english'] = df_books['details'].fillna('').str.lower().str.contains('english')

# Merge on numeric id
merged = pd.merge(df_books, df_reviews, on='num_id', how='inner', suffixes=('_book','_rev'))

# Filter for English language and avg_rating == 5.0
merged_filtered = merged[(merged['is_english']) & (merged['avg_rating'] == 5.0)]

# Prepare output
output = []
for _, row in merged_filtered.iterrows():
    output.append({
        'title': row['title'],
        'book_id': row['book_id'],
        'purchase_id': row['purchase_id'],
        'avg_rating': float(row['avg_rating']),
        'review_count': int(row['cnt'])
    })

# If no matches via numeric id, try a looser match: check if book_id numeric is substring of purchase_id or vice versa
if not output:
    # attempt substring match
    book_map = {str(extract_num(b)): b for b in df_books['book_id'].dropna().unique()}
    for _, r in df_reviews.iterrows():
        pnum = r['num_id']
        if pnum is None:
            continue
        key = str(pnum)
        if key in book_map:
            b = df_books[df_books['book_id']==book_map[key]].iloc[0]
            if 'english' in b['details'].lower() and float(r['avg_rating'])==5.0:
                output.append({
                    'title': b['title'],
                    'book_id': b['book_id'],
                    'purchase_id': r['purchase_id'],
                    'avg_rating': float(r['avg_rating']),
                    'review_count': int(r['cnt'])
                })

# Final JSON string
result_str = json.dumps(output)
print("__RESULT__:")
print(result_str)"""

env_args = {'var_call_RKLyW9yeHfq3pGs9l7t8qAMn': 'file_storage/call_RKLyW9yeHfq3pGs9l7t8qAMn.json', 'var_call_r3JVcCpPXhEr3RyEP1auoD4t': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'cnt': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'cnt': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'cnt': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'cnt': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'cnt': '1'}]}

exec(code, env_args)
