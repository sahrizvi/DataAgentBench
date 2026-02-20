code = """import json
import re
import pandas as pd

# Load file paths
file_path_books = locals()['var_function-call-3096561497567485986']
file_path_reviews = locals()['var_function-call-5332796046984058542']

# Load data
with open(file_path_books, 'r') as f:
    books_data = json.load(f)

with open(file_path_reviews, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Extract numbers
def extract_num(s):
    if pd.isna(s): return None
    match = re.search(r'(\d+)$', str(s))
    if match:
        return int(match.group(1))
    return None

books_df['id_num'] = books_df['book_id'].apply(extract_num)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_num)

# Check overlap
book_ids = set(books_df['id_num'].dropna())
review_ids = set(reviews_df['id_num'].dropna())

overlap = book_ids.intersection(review_ids)

print("__RESULT__:")
print(json.dumps({
    "book_ids_count": len(book_ids),
    "review_ids_count": len(review_ids),
    "overlap_count": len(overlap),
    "sample_overlap": list(overlap)[:10]
}))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json', 'var_function-call-12575391759179135184': {'error': 'No decade met the criteria.'}}

exec(code, env_args)
