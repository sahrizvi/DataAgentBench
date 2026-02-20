code = """import json
import pandas as pd

# Load Literature & Fiction books
books_file_path = locals()['var_functions.query_db:16']
with open(books_file_path, 'r') as f:
    books_data = json.load(f)

# Load all reviews
reviews_file_path = locals()['var_functions.query_db:20']
with open(reviews_file_path, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract numeric ID from book_id (bookid_X -> X) and purchase_id (purchaseid_X -> X)
df_books['numeric_id'] = df_books['book_id'].str.extract('bookid_(\d+)').astype(int)
df_reviews['numeric_id'] = df_reviews['purchase_id'].str.extract('purchaseid_(\d+)').astype(int)

# Convert rating to float
df_reviews['rating'] = df_reviews['rating'].astype(float)

# Calculate average rating per book
avg_ratings = df_reviews.groupby('numeric_id')['rating'].agg(['mean', 'count']).reset_index()
avg_ratings = avg_ratings.rename(columns={'mean': 'avg_rating', 'count': 'review_count'})

# Find books with perfect 5.0 average rating
perfect_books = avg_ratings[avg_ratings['avg_rating'] == 5.0]

# Join with books to get Literature & Fiction books with perfect rating
result = pd.merge(df_books, perfect_books, on='numeric_id', how='inner')

# Filter to ensure we only get books with rating_number > 0 (books that have ratings)
if 'rating_number' in df_books.columns:
    result = result[result['rating_number'] > 0]

# Prepare output
output_books = []
for _, row in result.iterrows():
    # Extract author name from the JSON string if available
    author_name = "Unknown"
    if row['author'] and row['author'] != 'None':
        try:
            author_info = json.loads(row['author'].replace("'", '"'))
            author_name = author_info.get('name', 'Unknown')
        except:
            author_name = str(row['author'])
    
    output_books.append({
        'title': row['title'],
        'author': author_name,
        'book_id': row['book_id'],
        'average_rating': row['avg_rating'],
        'review_count': row['review_count']
    })

print("__RESULT__:")
print(json.dumps(output_books, indent=2))"""

env_args = {'var_functions.query_db:0': [], 'var_functions.query_db:2': [{'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'book_id': 'bookid_5'}, {'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'categories': '["Books", "Arts & Photography", "History & Criticism"]', 'book_id': 'bookid_6'}, {'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'categories': '["Books", "Parenting & Relationships", "Parenting"]', 'book_id': 'bookid_7'}, {'title': 'Make: Electronics: Learning Through Discovery', 'categories': '["Books", "Engineering & Transportation", "Engineering"]', 'book_id': 'bookid_8'}, {'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'book_id': 'bookid_9'}, {'title': 'Four Centuries of American Education', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]', 'book_id': 'bookid_10'}], 'var_functions.query_db:5': [{'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_23', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_190', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_169', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_81', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_96', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_148', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}], 'var_functions.execute_python:8': [{'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'book_id': 'bookid_5'}, {'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'categories': '["Books", "Arts & Photography", "History & Criticism"]', 'book_id': 'bookid_6'}, {'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'categories': '["Books", "Parenting & Relationships", "Parenting"]', 'book_id': 'bookid_7'}, {'title': 'Make: Electronics: Learning Through Discovery', 'categories': '["Books", "Engineering & Transportation", "Engineering"]', 'book_id': 'bookid_8'}, {'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'book_id': 'bookid_9'}, {'title': 'Four Centuries of American Education', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]', 'book_id': 'bookid_10'}], 'var_functions.query_db:11': 'file_storage/functions.query_db:11.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:18': {'book_count': 40, 'sample_ids': ['bookid_1', 'bookid_9', 'bookid_13', 'bookid_30', 'bookid_36', 'bookid_37', 'bookid_38', 'bookid_39', 'bookid_44', 'bookid_49']}, 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}

exec(code, env_args)
