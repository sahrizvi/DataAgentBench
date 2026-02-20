code = """import json
import re
import pandas as pd

# Load books data
with open('var_function-call-3096561497567485986.json', 'r') as f:
    books_data = json.load(f)

# Load reviews data
with open('var_function-call-5332796046984058542.json', 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Function to extract year
def extract_year(row):
    # Try details first
    text = str(row.get('details', ''))
    matches = re.findall(r'\b(18|19|20)\d{2}\b', text)
    if matches:
        # Return the last match as it's often part of the full date at the end of the phrase "published on..."
        # But wait, sometimes there are ISBNs or other numbers.
        # Let's look for the specific pattern "published ... on ... year"
        # Or look for a year near a month name.
        # Let's try simple regex for now: 4 digits starting with 18, 19, 20.
        # Often the publication year is the one associated with the "published on" date.
        # Let's find all years.
        all_years = [int(m) for m in re.findall(r'\b(18|19|20)\d{2}\b', text)]
        # Filter for valid range? 
        valid_years = [y for y in all_years if 1800 <= y <= 2023]
        if valid_years:
            # If multiple, which one?
            # "published by ... on January 1, 2004" -> 2004 comes after month.
            # "8082nd edition from January 1, 1994" -> 1994.
            # Usually the publication date year is what we want.
            # Let's take the one that seems to be part of a date.
            date_matches = re.findall(r'[A-Za-z]+\s+\d{1,2},?\s+((?:19|20)\d{2})', text)
            if date_matches:
                return int(date_matches[0])
            return valid_years[0]
            
    # Try subtitle
    text = str(row.get('subtitle', ''))
    matches = re.findall(r'\b(18|19|20)\d{2}\b', text)
    if matches:
        valid_years = [int(y) for y in matches if 1800 <= y <= 2023]
        if valid_years:
             # Look for date pattern
            date_matches = re.findall(r'[A-Za-z]+\s+\d{1,2},?\s+((?:19|20)\d{2})', text)
            if date_matches:
                return int(date_matches[0])
            return valid_years[0]
            
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Extract IDs
# book_id is "bookid_X"
# purchase_id is "purchaseid_X"
def extract_id(s):
    if not s: return None
    parts = s.split('_')
    if len(parts) > 1:
        return parts[1]
    return None

books_df['join_id'] = books_df['book_id'].apply(extract_id)
reviews_df['join_id'] = reviews_df['purchase_id'].apply(extract_id)

# Convert rating to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Merge
merged_df = pd.merge(reviews_df, books_df, on='join_id', how='inner')

# Filter rows with valid year
merged_df = merged_df.dropna(subset=['year'])
merged_df['year'] = merged_df['year'].astype(int)

# Create decade column
merged_df['decade'] = (merged_df['year'] // 10) * 10

# Group by decade
decade_stats = merged_df.groupby('decade').agg(
    unique_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
qualified_decades = decade_stats[decade_stats['unique_books'] >= 10]

# Find the decade with highest average rating
if not qualified_decades.empty:
    best_decade = qualified_decades.loc[qualified_decades['avg_rating'].idxmax()]
    result = {
        "decade": int(best_decade['decade']),
        "avg_rating": best_decade['avg_rating'],
        "unique_books": int(best_decade['unique_books'])
    }
else:
    result = "No decade met the criteria."

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json'}

exec(code, env_args)
