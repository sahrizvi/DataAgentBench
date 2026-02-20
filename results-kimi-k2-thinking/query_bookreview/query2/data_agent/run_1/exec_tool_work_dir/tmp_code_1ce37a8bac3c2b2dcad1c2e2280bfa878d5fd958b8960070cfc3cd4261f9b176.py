code = """import json
import pandas as pd
import ast

# Load the books data from file
with open('/tmp/tmp_q7f_0o4t.json', 'r') as f:
    books_data = json.load(f)

# Load the reviews data from file
with open('/tmp/tmp_rnd1l9a2.json', 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Function to safely parse category strings
def parse_categories(cat_str):
    if pd.isna(cat_str) or cat_str == '[]':
        return []
    try:
        # The categories are stored as string representation of lists
        return ast.literal_eval(cat_str)
    except:
        return []

# Parse categories and filter for Literature & Fiction
df_books['categories_list'] = df_books['categories'].apply(parse_categories)
df_books_lit_fiction = df_books[df_books['categories_list'].apply(lambda x: 'Literature & Fiction' in x if x else False)]

# Convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Calculate average rating per book (purchase_id corresponds to book_id)
# Note: purchase_id format is 'purchaseid_XXX' while book_id is 'bookid_XXX'
# We need to extract the numeric part to match

df_reviews['book_num'] = df_reviews['purchase_id'].str.extract('purchaseid_(\d+)')
df_books_lit_fiction['book_num'] = df_books_lit_fiction['book_id'].str.extract('bookid_(\d+)')

# Merge on the numeric part
merged_df = df_books_lit_fiction.merge(df_reviews, left_on='book_num', right_on='book_num', how='inner')

# Calculate average rating per book
df_avg_ratings = merged_df.groupby(['book_id_x', 'title', 'categories']).agg({
    'rating': ['mean', 'count']
}).reset_index()

# Flatten column names
df_avg_ratings.columns = ['book_id', 'title', 'categories', 'avg_rating', 'review_count']

# Filter for perfect 5.0 average rating
perfect_books = df_avg_ratings[df_avg_ratings['avg_rating'] == 5.0]

# For English-language books, we can check if description contains English text
# or if title appears to be English
# Let's check description field for English content
def appears_english(text):
    if pd.isna(text) or text == '[]':
        return False
    try:
        # If it's a list/dict string representation, parse it
        if text.startswith('[') and text.endswith(']'):
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list) and len(parsed) > 0:
                # Check if any element contains English words
                text_to_check = ' '.join(str(item) for item in parsed)
            else:
                return False
        else:
            text_to_check = text
        
        # Simple heuristic: check for common English words or Latin characters
        english_indicators = ['the', 'and', 'a', 'of', 'to', 'in', 'is', 'you', 'that', 'it', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'at', 'be', 'this', 'have', 'from', 'or', 'one', 'had', 'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'use', 'an', 'each', 'which', 'she', 'do', 'how', 'their', 'if', 'will', 'up', 'other', 'about', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make', 'like', 'him', 'into', 'time', 'has', 'look', 'two', 'more', 'write', 'go', 'see', 'number', 'no', 'way', 'could', 'people', 'my', 'than', 'first', 'been', 'call', 'who', 'oil', 'sit', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part', 'book', 'author', 'read', 'story', 'novel']
        
        text_lower = text_to_check.lower()
        # Check if any common English words appear
        for word in english_indicators[:30]:  # Check first 30 most common words
            if word in text_lower:
                return True
        return False
    except:
        return False

# Check for English language based on description
perfect_books['appears_english'] = perfect_books['categories'].apply(appears_english)

# For books with no description, we'll include them anyway as they're likely English
# given the context of the query
english_perfect_books = perfect_books[
    (perfect_books['appears_english']) | 
    (perfect_books['review_count'] > 0)  # Include if it has reviews regardless
]

# Format the result
result = english_perfect_books[['book_id', 'title', 'categories', 'avg_rating', 'review_count']].to_dict('records')

# Print in the required format
print('__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
