code = """import json
import re
import pandas as pd

# Load file paths
file_path_books = locals()['var_function-call-3096561497567485986']
file_path_reviews = locals()['var_function-call-5332796046984058542']

# Load books data
with open(file_path_books, 'r') as f:
    books_data = json.load(f)

# Load reviews data
with open(file_path_reviews, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Function to extract year from details
def extract_year(row):
    text = str(row.get('details', ''))
    # Look for a 4-digit year 19xx or 20xx
    # Prioritize years appearing near "published" or month names
    # "published ... on [Month] [Day], [Year]"
    # "published ... in [Year]"
    
    # Try specific pattern first: "published ... on ... \d{4}"
    # Example: "Published by ... on January 1, 2004."
    # Regex: published.*?on\s+[A-Za-z]+\s+\d{1,2},?\s+(\d{4})
    match = re.search(r'published.*?on\s+[A-Za-z]+\s+\d{1,2},?\s+(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try "published ... in ... \d{4}"
    match = re.search(r'published.*?in\s+[A-Za-z]+\s+(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # If not found, look for any 4-digit year in details
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    if years:
        return int(years[0]) # Take the first year found if specific pattern fails
        
    # If not found in details, try subtitle
    text_sub = str(row.get('subtitle', ''))
    # "Hardcover – Import, January 1, 2004"
    match = re.search(r'\b(19\d{2}|20\d{2})\b', text_sub)
    if match:
        return int(match.group(1))
        
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Extract numeric ID for joining
# books: bookid_X
# reviews: purchaseid_X
def extract_id_num(s):
    if pd.isna(s): return None
    match = re.search(r'(\d+)$', str(s))
    if match:
        return int(match.group(1))
    return None

books_df['id_num'] = books_df['book_id'].apply(extract_id_num)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_id_num)

# Merge
merged_df = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# Filter valid year
merged_df = merged_df.dropna(subset=['year'])
merged_df['year'] = merged_df['year'].astype(int)

# Calculate decade (e.g. 1980)
merged_df['decade'] = (merged_df['year'] // 10) * 10

# Filter out books with no ratings? No, we have inner join with reviews, so they have ratings.
# But we need "decades with at least 10 distinct books that have been rated".
# Distinct books per decade.

decade_counts = merged_df.groupby('decade')['book_id'].nunique().reset_index(name='unique_books')
qualified_decades_list = decade_counts[decade_counts['unique_books'] >= 10]['decade'].tolist()

# Filter original merged_df for only qualified decades
qualified_df = merged_df[merged_df['decade'].isin(qualified_decades_list)]

if not qualified_df.empty:
    # Calculate average rating per decade
    # Average of all reviews in that decade?
    # "highest average rating among decades..." usually implies average of all individual review ratings.
    decade_avg = qualified_df.groupby('decade')['rating'].mean().reset_index(name='avg_rating')
    
    best_decade_row = decade_avg.loc[decade_avg['avg_rating'].idxmax()]
    result = {
        "decade": int(best_decade_row['decade']),
        "avg_rating": float(best_decade_row['avg_rating']),
        "unique_books": int(decade_counts[decade_counts['decade'] == best_decade_row['decade']]['unique_books'].iloc[0])
    }
else:
    result = {"error": "No decade met the criteria."}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json'}

exec(code, env_args)
