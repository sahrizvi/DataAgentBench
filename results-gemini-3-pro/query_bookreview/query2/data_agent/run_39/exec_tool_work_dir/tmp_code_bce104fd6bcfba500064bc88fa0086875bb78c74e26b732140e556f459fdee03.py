code = """import pandas as pd
import json
import re

# Get file paths from local variables
books_file_path = locals()['var_function-call-10362978637305553853']
reviews_file_path = locals()['var_function-call-12139457111290715918']

# Load books
with open(books_file_path, 'r') as f:
    books_data = json.load(f)

# Load reviews
with open(reviews_file_path, 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrame
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Helper functions
def parse_categories(cat_str):
    try:
        # The string is like "['Books', 'Literature & Fiction', ...]"
        # It's a string representation of a list. json.loads might fail if it uses single quotes.
        # Let's inspect the sample: "[\"Books\", \"Literature & Fiction\", \"History & Criticism\"]"
        # It uses double quotes, so json.loads should work.
        return json.loads(cat_str)
    except:
        return []

def is_english(details_str):
    if not isinstance(details_str, str):
        return False
    return "English" in details_str

def extract_id(id_str):
    # Extracts number from "bookid_123" or "purchaseid_123"
    m = re.search(r'(\d+)$', id_str)
    if m:
        return int(m.group(1))
    return None

# Process Books
# Parse categories
books_df['categories_list'] = books_df['categories'].apply(parse_categories)
# Check for Literature & Fiction
books_df['is_lit_fiction'] = books_df['categories_list'].apply(lambda x: "Literature & Fiction" in x)
# Check for English
books_df['is_english'] = books_df['details'].apply(is_english)
# Extract ID
books_df['id'] = books_df['book_id'].apply(extract_id)

# Filter Books
filtered_books = books_df[books_df['is_lit_fiction'] & books_df['is_english']].copy()

# Process Reviews
# Convert rating to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'])
# Extract ID
reviews_df['id'] = reviews_df['purchase_id'].apply(extract_id)

# Calculate average rating per book
avg_ratings = reviews_df.groupby('id')['rating'].mean().reset_index()

# Filter for perfect 5.0 rating
perfect_ratings = avg_ratings[avg_ratings['rating'] == 5.0]

# Join
result_df = pd.merge(filtered_books, perfect_ratings, on='id', how='inner')

# Get titles
titles = result_df['title'].tolist()

print("__RESULT__:")
print(json.dumps(titles))"""

env_args = {'var_function-call-4147346583675466540': [{'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_function-call-11786665074539543977': [{'count': '200'}], 'var_function-call-4574657001763612032': [{'COUNT(*)': '1833'}], 'var_function-call-12715659242661395547': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17451264347564578439': {'books_query': 'SELECT book_id, title, categories, details FROM books_info', 'reviews_query': 'SELECT purchase_id, rating FROM review'}, 'var_function-call-10362978637305553853': 'file_storage/function-call-10362978637305553853.json', 'var_function-call-12139457111290715918': 'file_storage/function-call-12139457111290715918.json'}

exec(code, env_args)
