code = """import json
import re
import pandas as pd

# Load books data
with open(var_function_call_3096561497567485986, 'r') as f:
    books_data = json.load(f)

# Load reviews data
with open(var_function_call_5332796046984058542, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Function to extract year
def extract_year(row):
    text_details = str(row.get('details', ''))
    text_subtitle = str(row.get('subtitle', ''))
    
    # Try to find a year in details
    # Look for 4 digits (19xx or 20xx)
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text_details)
    if years:
        # If multiple, take the last one usually (e.g., "published ... 2004")
        return int(years[-1])
    
    # If not found, try subtitle
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text_subtitle)
    if years:
        return int(years[-1])
        
    return None

# Apply extraction
books_df['year'] = books_df.apply(extract_year, axis=1)

# Function to extract ID number
def extract_id_num(s):
    if pd.isna(s): return None
    # Extracts the number from strings like "bookid_123" or "purchaseid_123"
    match = re.search(r'(\d+)$', str(s))
    if match:
        return int(match.group(1))
    return None

books_df['id_num'] = books_df['book_id'].apply(extract_id_num)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_id_num)

# Merge on id_num
merged_df = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# Filter out rows with no year
merged_df = merged_df.dropna(subset=['year'])

# Calculate decade
merged_df['decade'] = (merged_df['year'] // 10) * 10

# Convert rating to numeric
merged_df['rating'] = pd.to_numeric(merged_df['rating'], errors='coerce')

# Group by decade
# We need distinct books count >= 10
# So first group by decade and count unique book_id
decade_stats = merged_df.groupby('decade').agg(
    unique_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
qualified_decades = decade_stats[decade_stats['unique_books'] >= 10].copy()

# Find max avg rating
if not qualified_decades.empty:
    best_decade_row = qualified_decades.loc[qualified_decades['avg_rating'].idxmax()]
    result = {
        "decade": int(best_decade_row['decade']),
        "avg_rating": float(best_decade_row['avg_rating']),
        "unique_books": int(best_decade_row['unique_books'])
    }
else:
    result = "No decade met the criteria."

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json'}

exec(code, env_args)
