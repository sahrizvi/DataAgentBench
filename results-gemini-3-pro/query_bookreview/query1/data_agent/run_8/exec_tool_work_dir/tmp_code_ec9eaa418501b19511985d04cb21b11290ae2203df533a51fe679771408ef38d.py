code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
    books_data = json.load(f)
    
with open(locals()['var_function-call-13869118034911199914'], 'r') as f:
    reviews_data = json.load(f)

# Process Books
books = []
for b in books_data:
    book_id_raw = b.get('book_id', '')
    details = b.get('details', '')
    
    # Extract ID number
    # Assuming format bookid_X
    m_id = re.search(r'bookid_(\d+)', book_id_raw)
    if m_id:
        id_num = int(m_id.group(1))
    else:
        continue

    # Extract Year
    # Look for patterns like "published ... on ... 2004" or just find the year 19xx/20xx
    # Many formats: "January 1, 2004", "May 20, 1996", "January 2004", "1987 edition"
    # Let's try to find a 4 digit year 1900-2023.
    # To avoid extracting ISBN parts or other numbers, we can look for specific context or just all years and pick the most plausible one (usually the first one mentioned in context of publication).
    
    # Priority: "published ... YEAR"
    # Regex for year: 19\d{2}|20\d{2}
    
    # Simplified approach: Find all years. Use the first one that seems to be part of a date.
    # Or just the first year found in the string? 
    # details string usually starts with "This book, published by ... on [Date]..."
    
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    
    # Filter out years that might be ISBNs (though ISBNs usually don't look like standalone 4-digit years, they are part of longer strings).
    # But sometimes ISBN-10 might contain a year-like sequence? Unlikely to be standalone \b.
    
    pub_year = None
    if years:
        # Heuristic: The first year mentioned is often the publication year in these descriptions.
        # But sometimes it mentions "reprint edition 2013... original 19xx".
        # The prompt asks for "decade of publication". I should probably use the main publication date listed.
        pub_year = int(years[0])
    
    if pub_year:
        books.append({'id': id_num, 'year': pub_year})

df_books = pd.DataFrame(books)

# Process Reviews
reviews = []
for r in reviews_data:
    pid_raw = r.get('purchase_id', '')
    rating = r.get('rating')
    
    # Extract ID number
    m_id = re.search(r'purchaseid_(\d+)', pid_raw)
    if m_id:
        id_num = int(m_id.group(1))
        try:
            r_val = float(rating)
            reviews.append({'id': id_num, 'rating': r_val})
        except:
            continue

df_reviews = pd.DataFrame(reviews)

# Aggregate ratings by book
# We want the average rating per book first.
book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

# Merge
df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')

# Calculate Decade
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(str) + 's'

# Group by Decade
decade_stats = df_merged.groupby('decade_str').agg(
    num_books=('id', 'nunique'),
    avg_rating_of_books=('avg_rating', 'mean')
).reset_index()

# Filter for at least 10 distinct books
qualified_decades = decade_stats[decade_stats['num_books'] >= 10].copy()

# Sort by highest average rating
qualified_decades.sort_values(by='avg_rating_of_books', ascending=False, inplace=True)

print("__RESULT__:")
print(qualified_decades.to_json(orient='records'))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json'}

exec(code, env_args)
