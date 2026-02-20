code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-8487536808771616656'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-5723484120947342381'], 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# 1. Parse IDs
def extract_id(s):
    if pd.isna(s): return None
    match = re.search(r'(\d+)$', str(s))
    if match:
        return int(match.group(1))
    return None

books_df['id_num'] = books_df['book_id'].apply(extract_id)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_id)
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# 2. Parse Year
def extract_year(row):
    text = str(row.get('details', '')) + " " + str(row.get('subtitle', ''))
    pattern = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[a-z]*[\s\.,]+(?:\d{1,2}[\s,]+)?(\d{4})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'published.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Filter valid years
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df = books_df[(books_df['year'] >= 1800) & (books_df['year'] <= 2024)]

# 3. Create Decade
books_df['decade'] = (books_df['year'] // 10) * 10
books_df['decade_str'] = books_df['decade'].astype(str) + 's'

# 4. Join
merged_df = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# Filter for 1980s
dec_1980 = merged_df[merged_df['decade_str'] == '1980s']
print("__RESULT__:")
print(json.dumps(dec_1980.groupby('title').agg(
    avg_rating=('rating', 'mean'),
    count=('rating', 'count')
).reset_index().to_dict(orient='records')))"""

env_args = {'var_function-call-18101049058431694268': 'file_storage/function-call-18101049058431694268.json', 'var_function-call-9824219790381673383': [{'count': '200'}], 'var_function-call-11034210423185423551': [{'COUNT(*)': '1833'}], 'var_function-call-8487536808771616656': 'file_storage/function-call-8487536808771616656.json', 'var_function-call-5723484120947342381': 'file_storage/function-call-5723484120947342381.json', 'var_function-call-654814139124136116': {'decade': '2020.0s', 'avg_rating': 4.663636363636364, 'distinct_books': 21}, 'var_function-call-17923682077472991392': [{'decade_str': '2020s', 'avg_rating': 4.663636363636364, 'distinct_books': 21, 'review_count': 110}, {'decade_str': '2010s', 'avg_rating': 4.608591885441528, 'distinct_books': 88, 'review_count': 1257}, {'decade_str': '2000s', 'avg_rating': 4.276223776223776, 'distinct_books': 47, 'review_count': 286}, {'decade_str': '1980s', 'avg_rating': 4.208333333333333, 'distinct_books': 11, 'review_count': 72}, {'decade_str': '1990s', 'avg_rating': 3.823529411764706, 'distinct_books': 17, 'review_count': 68}], 'var_function-call-1529116302123987789': [{'decade_str': '1980s', 'avg_of_book_avgs': 4.5481993851559075, 'distinct_books': 11}, {'decade_str': '2020s', 'avg_of_book_avgs': 4.52530525030525, 'distinct_books': 21}, {'decade_str': '2010s', 'avg_of_book_avgs': 4.405139336568189, 'distinct_books': 88}, {'decade_str': '2000s', 'avg_of_book_avgs': 4.357517513775337, 'distinct_books': 47}, {'decade_str': '1990s', 'avg_of_book_avgs': 4.1175887021475255, 'distinct_books': 17}]}

exec(code, env_args)
