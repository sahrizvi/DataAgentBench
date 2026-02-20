code = """import json
import re
import pandas as pd

try:
    with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
        books_data = json.load(f)
    print(f"Loaded {len(books_data)} books")
except Exception as e:
    print(f"Error loading books: {e}")
    books_data = []

try:
    with open(locals()['var_function-call-13869118034911199914'], 'r') as f:
        reviews_data = json.load(f)
    print(f"Loaded {len(reviews_data)} reviews")
except Exception as e:
    print(f"Error loading reviews: {e}")
    reviews_data = []

# Process Books
book_records = []
for b in books_data:
    bid = b.get('book_id', '')
    details = b.get('details', '')
    
    # Extract numeric ID
    m = re.search(r'bookid_(\d+)', str(bid))
    if not m:
        continue
    book_num = int(m.group(1))
    
    # Extract Year
    # Look for 4 digits in range 1900-2023
    # Use the first valid year found in the text
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', str(details))
    if years:
        year = int(years[0])
        book_records.append({'id': book_num, 'year': year})

df_books = pd.DataFrame(book_records)
print(f"df_books shape: {df_books.shape}")
if not df_books.empty:
    print(f"df_books columns: {df_books.columns.tolist()}")
    print(df_books.head(2))

# Process Reviews
review_records = []
for r in reviews_data:
    pid = r.get('purchase_id', '')
    rating = r.get('rating')
    
    m = re.search(r'purchaseid_(\d+)', str(pid))
    if not m:
        continue
    book_num = int(m.group(1))
    
    try:
        val = float(rating)
        review_records.append({'id': book_num, 'rating': val})
    except:
        pass

df_reviews = pd.DataFrame(review_records)
print(f"df_reviews shape: {df_reviews.shape}")
if not df_reviews.empty:
    print(f"df_reviews columns: {df_reviews.columns.tolist()}")
    print(df_reviews.head(2))

# Aggregate Ratings
if not df_reviews.empty:
    book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
    book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)
else:
    book_ratings = pd.DataFrame(columns=['id', 'avg_rating'])

# Merge
df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')
print(f"df_merged shape: {df_merged.shape}")

if df_merged.empty:
    print("__RESULT__:")
    print("[]")
else:
    # Calculate Decade
    df_merged['decade'] = (df_merged['year'] // 10) * 10
    
    # Group by Decade
    # We want average rating of the decade.
    # The prompt says: "highest average rating among decades with at least 10 distinct books".
    # We should calculate the average of the average ratings of the books.
    
    decade_stats = df_merged.groupby('decade').agg(
        num_books=('id', 'nunique'),
        avg_rating=('avg_rating', 'mean')
    ).reset_index()
    
    # Filter >= 10 books
    qualified = decade_stats[decade_stats['num_books'] >= 10].copy()
    
    # Sort
    qualified.sort_values(by='avg_rating', ascending=False, inplace=True)
    
    print("Qualified Decades:")
    print(qualified)
    
    # Format result
    # Return the decade (e.g. "1980s")
    if not qualified.empty:
        best_decade = qualified.iloc[0]
        decade_val = int(best_decade['decade'])
        decade_str = f"{decade_val}s"
        
        result_str = json.dumps(decade_str)
        print("__RESULT__:")
        print(result_str)
    else:
        print("__RESULT__:")
        print(json.dumps("None"))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json'}

exec(code, env_args)
