code = """import json
import re
import pandas as pd
from datetime import datetime

# Load data
books = pd.read_json(locals()['var_function-call-13031625442222991424'])
reviews = pd.read_json(locals()['var_function-call-3241637180014007920'])

# Function to extract year
def extract_year(details):
    if not isinstance(details, str):
        return None
    # Pattern for "on Month Day, Year"
    match = re.search(r"on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", details)
    if match:
        date_str = match.group(1)
        try:
            dt = datetime.strptime(date_str, "%B %d, %Y")
            return dt.year
        except ValueError:
            pass
    return None

books['year'] = books['details'].apply(extract_year)

# Drop books without year
books_with_year = books.dropna(subset=['year']).copy()
books_with_year['decade'] = (books_with_year['year'] // 10 * 10).astype(int)
books_with_year['decade_str'] = books_with_year['decade'].astype(str) + "s"

# Merge with reviews
# reviews has purchase_id, books has book_id
merged = pd.merge(reviews, books_with_year, left_on='purchase_id', right_on='book_id', how='inner')

# Convert rating to float
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
merged = merged.dropna(subset=['rating'])

# Group by decade
stats = merged.groupby('decade_str').agg(
    num_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
filtered_stats = stats[stats['num_books'] >= 10].sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(filtered_stats.to_json(orient='records'))"""

env_args = {'var_function-call-6240078878666439792': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-16420436372098634934': [{'count': '200'}], 'var_function-call-7158374868136901473': [{'COUNT(*)': '1833'}], 'var_function-call-13031625442222991424': 'file_storage/function-call-13031625442222991424.json', 'var_function-call-3241637180014007920': 'file_storage/function-call-3241637180014007920.json'}

exec(code, env_args)
