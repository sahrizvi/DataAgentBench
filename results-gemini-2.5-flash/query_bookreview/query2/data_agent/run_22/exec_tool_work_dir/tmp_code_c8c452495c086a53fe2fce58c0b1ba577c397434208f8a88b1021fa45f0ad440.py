code = """import pandas as pd
import json

# Load book information
with open(locals()['var_function-call-13122956751315087020'], 'r') as f:
    books_data = json.load(f)
books_df = pd.DataFrame(books_data)

# Load review information
with open(locals()['var_function-call-17820796150228834284'], 'r') as f:
    reviews_data = json.load(f)
reviews_df = pd.DataFrame(reviews_data)

# Convert 'rating' to numeric and handle potential errors
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Filter for Literature & Fiction and English language
books_df['categories_parsed'] = books_df['categories'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
literature_fiction_books = books_df[books_df['categories_parsed'].apply(lambda x: 'Literature & Fiction' in x)]
english_books = literature_fiction_books[literature_fiction_books['details'].str.contains('English', na=False)]

# Calculate average rating for each book
average_ratings = reviews_df.groupby('purchase_id')['rating'].mean().reset_index()
average_ratings.rename(columns={'purchase_id': 'book_id'}, inplace=True)

# Filter for books with a perfect average rating of 5.0
perfect_rating_books = average_ratings[average_ratings['rating'] == 5.0]

# Merge the filtered books with their perfect ratings
final_books = pd.merge(english_books, perfect_rating_books, on='book_id')

# Extract title and author
# The 'author' column is a string representation of a JSON object.
# Need to parse it to get the author's name.
def get_author_name(author_str):
    if pd.isna(author_str) or author_str == 'None':
        return None
    try:
        author_json = json.loads(author_str)
        return author_json.get('name')
    except json.JSONDecodeError:
        return None

final_books['author_name'] = final_books['author'].apply(get_author_name)

result = final_books[['title', 'author_name']].to_json(orient='records')
print('__RESULT__:')
print(result)"""

env_args = {'var_function-call-15259486126433126849': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}], 'var_function-call-13122956751315087020': 'file_storage/function-call-13122956751315087020.json', 'var_function-call-17820796150228834284': 'file_storage/function-call-17820796150228834284.json'}

exec(code, env_args)
