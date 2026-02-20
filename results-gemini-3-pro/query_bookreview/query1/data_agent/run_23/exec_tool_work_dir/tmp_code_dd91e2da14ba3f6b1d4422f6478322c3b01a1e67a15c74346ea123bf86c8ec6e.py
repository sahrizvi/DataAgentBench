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

# 2. Parse Year
def extract_year(row):
    text = str(row.get('details', '')) + " " + str(row.get('subtitle', ''))
    # Regex for Month Day, Year or Month Year
    pattern = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[a-z]*[\s\.,]+(?:\d{1,2}[\s,]+)?(\d{4})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Fallback: look for "published ... 19xx/20xx"
    match = re.search(r'published.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
        
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Filter valid years (reasonable range, e.g., 1800-2024)
books_df = books_df[(books_df['year'] >= 1800) & (books_df['year'] <= 2024)].copy()

# 3. Create Decade
books_df['decade'] = (books_df['year'] // 10) * 10
# Convert to string decade format (e.g., 1980s)
books_df['decade_str'] = books_df['decade'].astype(str) + 's'

# 4. Convert rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# 5. Join
merged_df = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# 6. Group by Decade
decade_stats = merged_df.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    distinct_books=('id_num', 'nunique'),
    review_count=('rating', 'count')
).reset_index()

# 7. Filter
qualified_decades = decade_stats[decade_stats['distinct_books'] >= 10].copy()

# 8. Find Max
if not qualified_decades.empty:
    best_decade = qualified_decades.loc[qualified_decades['avg_rating'].idxmax()]
    result = {
        "decade": best_decade['decade_str'],
        "avg_rating": float(best_decade['avg_rating']),
        "distinct_books": int(best_decade['distinct_books'])
    }
else:
    result = "No decade meets the criteria."

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-18101049058431694268': 'file_storage/function-call-18101049058431694268.json', 'var_function-call-9824219790381673383': [{'count': '200'}], 'var_function-call-11034210423185423551': [{'COUNT(*)': '1833'}], 'var_function-call-8487536808771616656': 'file_storage/function-call-8487536808771616656.json', 'var_function-call-5723484120947342381': 'file_storage/function-call-5723484120947342381.json'}

exec(code, env_args)
