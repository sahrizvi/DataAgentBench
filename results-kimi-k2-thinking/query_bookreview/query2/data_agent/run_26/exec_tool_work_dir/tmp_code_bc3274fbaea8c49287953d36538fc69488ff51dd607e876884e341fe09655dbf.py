code = """import json
import pandas as pd
import re

# Load literature books data
lit_books_path = var_functions.query_db_16
with open(lit_books_path, 'r') as f:
    lit_books = json.load(f)

# Load review data
reviews_path = var_functions.query_db_14
with open(reviews_path, 'r') as f:
    reviews = json.load(f)

# Convert to DataFrames
df_books = pd.DataFrame(lit_books)
df_reviews = pd.DataFrame(reviews)

# Extract numeric IDs
df_books['book_num_id'] = df_books['book_id'].str.extract(r'bookid_(\d+)').astype(int)
df_reviews['review_num_id'] = df_reviews['purchase_id'].str.extract(r'purchaseid_(\d+)').astype(int)

# Convert rating to float
df_reviews['rating'] = df_reviews['rating'].astype(float)

# Merge on numeric IDs
df_merged = pd.merge(df_books, df_reviews, left_on='book_num_id', right_on='review_num_id', how='inner')

# Filter for English-language books (check details field contains "English")
df_english = df_merged[df_merged['details'].str.contains('English', case=False, na=False)]

# Calculate average rating per book
df_avg_ratings = df_english.groupby(['book_id', 'title', 'author', 'categories', 'details']).agg({
    'rating': 'mean'
}).reset_index()

# Filter for perfect 5.0 average rating
df_perfect = df_avg_ratings[abs(df_avg_ratings['rating'] - 5.0) < 0.001]

# Prepare result
result = df_perfect[['title', 'author', 'categories', 'details', 'rating']].copy()

# Convert to JSON string
result_json = result.to_json(orient='records', indent=2)

print('__RESULT__:')
print(result_json)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'title': 'Chaucer', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'author': '{"avatar": "https://m.media-amazon.com/images/I/01Kv-W2ysOL._SY600_.png", "name": "Yetta M. Goodman", "about": ["Discover more of the author’s books, see similar authors, read author blogs and more"]}', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'author': '{"avatar": "https://m.media-amazon.com/images/I/31rBoNEHiFL._SY600_.jpg", "name": "Marcus Luttrell", "about": ["Petty Officer First Class Marcus Luttrell was born in Huntsville, Texas in 1975."]}', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'author': 'None', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'author': '{"avatar": "https://m.media-amazon.com/images/S/amzn-author-media-prod/p5em8p7bskq0m3fr3tncs8ghcf._SY600_.jpg", "name": "Donald Wells", "about": ["Discover more of the author’s books, see similar authors, read author blogs and more"]}', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.list_db:6': ['review'], 'var_functions.query_db:8': [{'rating': '4', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_9'}, {'book_id': 'bookid_13'}, {'book_id': 'bookid_30'}, {'book_id': 'bookid_36'}, {'book_id': 'bookid_37'}, {'book_id': 'bookid_38'}, {'book_id': 'bookid_39'}, {'book_id': 'bookid_44'}, {'book_id': 'bookid_49'}, {'book_id': 'bookid_55'}, {'book_id': 'bookid_69'}, {'book_id': 'bookid_70'}, {'book_id': 'bookid_74'}, {'book_id': 'bookid_77'}, {'book_id': 'bookid_82'}, {'book_id': 'bookid_84'}, {'book_id': 'bookid_89'}, {'book_id': 'bookid_92'}, {'book_id': 'bookid_93'}, {'book_id': 'bookid_98'}, {'book_id': 'bookid_99'}, {'book_id': 'bookid_101'}, {'book_id': 'bookid_106'}, {'book_id': 'bookid_109'}, {'book_id': 'bookid_111'}, {'book_id': 'bookid_122'}, {'book_id': 'bookid_137'}, {'book_id': 'bookid_142'}, {'book_id': 'bookid_144'}, {'book_id': 'bookid_161'}, {'book_id': 'bookid_167'}, {'book_id': 'bookid_171'}, {'book_id': 'bookid_177'}, {'book_id': 'bookid_179'}, {'book_id': 'bookid_180'}, {'book_id': 'bookid_182'}, {'book_id': 'bookid_187'}, {'book_id': 'bookid_188'}, {'book_id': 'bookid_195'}], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json'}

exec(code, env_args)
