code = """import json
import pandas as pd
# Load review aggregates from storage
reviews = var_call_yVmYizuMroNQUrFDdgMR0wr0
# Load books_info results from JSON file path stored in var_call_pMzup00cJgwgrzd5iyvLnWVn
books_file_path = var_call_pMzup00cJgwgrzd5iyvLnWVn
with open(books_file_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Convert to DataFrames
df_reviews = pd.DataFrame(reviews)
# Convert types
if not df_reviews.empty:
    df_reviews['avg_rating'] = df_reviews['avg_rating'].astype(float)
    df_reviews['n_reviews'] = df_reviews['n_reviews'].astype(int)

# Build mapping from purchaseid_X -> bookid_X
# Create a column book_id by replacing 'purchaseid_' with 'bookid_'
if not df_reviews.empty:
    df_reviews['book_id'] = df_reviews['purchase_id'].str.replace('purchaseid_', 'bookid_')

# Books dataframe
df_books = pd.DataFrame(books)
# Normalize categories (they are string representations of lists)
import ast

def parse_categories(cat_str):
    try:
        parsed = ast.literal_eval(cat_str)
        return parsed
    except Exception:
        return []

if not df_books.empty and 'categories' in df_books.columns:
    df_books['categories_parsed'] = df_books['categories'].apply(parse_categories)
else:
    df_books['categories_parsed'] = [[] for _ in range(len(df_books))]

# Merge reviews with books on book_id
if not df_reviews.empty:
    merged = pd.merge(df_reviews, df_books, on='book_id', how='inner')
else:
    merged = pd.DataFrame()

# Filter to ensure categories contain "Children's Books" (case-insensitive)
def is_childrens(cats):
    if not isinstance(cats, list):
        return False
    return any((('children' in str(c).lower()) or ("children's books" in str(c).lower())) for c in cats)

if not merged.empty:
    merged['is_children'] = merged['categories_parsed'].apply(is_childrens)
    merged = merged[merged['is_children']]

# Prepare final output: list of dicts with book_id, title, author, avg_rating, n_reviews, categories
result = []
if not merged.empty:
    merged_sorted = merged.sort_values(by=['avg_rating','n_reviews'], ascending=[False, False])
    for _, row in merged_sorted.iterrows():
        result.append({
            'book_id': row.get('book_id'),
            'title': row.get('title'),
            'author': row.get('author'),
            'avg_rating': float(row.get('avg_rating')),
            'n_reviews': int(row.get('n_reviews')),
            'categories': row.get('categories_parsed')
        })

# Print result in required format as JSON string
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_Tng5mCe3ePl7vmyoS8qy1i9d': ['books_info'], 'var_call_hqtPEL2s4qggFdG4s5Lo6amG': ['review'], 'var_call_yVmYizuMroNQUrFDdgMR0wr0': [{'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'n_reviews': '14'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'n_reviews': '8'}, {'purchase_id': 'purchaseid_10', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_154', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_3', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_66', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_129', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_169', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_185', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_187', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_196', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_198', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_200', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_22', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_37', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_4', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_46', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_55', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_94', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_96', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_13', 'avg_rating': '4.923076923076923', 'n_reviews': '13'}, {'purchase_id': 'purchaseid_149', 'avg_rating': '4.9', 'n_reviews': '10'}, {'purchase_id': 'purchaseid_178', 'avg_rating': '4.795918367346939', 'n_reviews': '49'}, {'purchase_id': 'purchaseid_115', 'avg_rating': '4.75', 'n_reviews': '8'}, {'purchase_id': 'purchaseid_48', 'avg_rating': '4.75', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_76', 'avg_rating': '4.75', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_8', 'avg_rating': '4.709677419354839', 'n_reviews': '31'}, {'purchase_id': 'purchaseid_158', 'avg_rating': '4.708333333333333', 'n_reviews': '24'}, {'purchase_id': 'purchaseid_161', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_23', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_50', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_72', 'avg_rating': '4.5', 'n_reviews': '2'}], 'var_call_pMzup00cJgwgrzd5iyvLnWVn': 'file_storage/call_pMzup00cJgwgrzd5iyvLnWVn.json'}

exec(code, env_args)
