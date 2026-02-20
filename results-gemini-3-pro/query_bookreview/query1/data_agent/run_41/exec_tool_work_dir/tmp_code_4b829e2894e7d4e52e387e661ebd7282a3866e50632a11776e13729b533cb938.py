code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-8759879918507074123']) as f:
    books_data = json.load(f)
with open(locals()['var_function-call-8759879918507075314']) as f:
    reviews_data = json.load(f)

# Process books
book_years = []
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
pattern = r'(?:' + '|'.join(months) + r')\s+\d{1,2},\s+(\d{4})'

for b in books_data:
    bid_str = b['book_id']
    if '_' in bid_str:
        bid_num = bid_str.split('_')[1]
    
    details = b.get('details', '')
    match = re.search(pattern, details)
    if match:
        year = int(match.group(1))
        # Group by decade
        decade = (year // 10) * 10
        book_years.append({'id': bid_num, 'decade': decade})

df_books = pd.DataFrame(book_years)

# Process reviews
review_list = []
for r in reviews_data:
    pid_str = r['purchase_id']
    if '_' in pid_str:
        pid_num = pid_str.split('_')[1]
        try:
            rating = float(r['rating'])
            review_list.append({'id': pid_num, 'rating': rating})
        except ValueError:
            continue

df_reviews = pd.DataFrame(review_list)

# Average per book
book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
book_ratings.columns = ['id', 'book_avg_rating']

# Join
merged = pd.merge(df_books, book_ratings, on='id')

# Group by decade
decade_stats = merged.groupby('decade').agg(
    num_books=('id', 'nunique'),
    avg_rating=('book_avg_rating', 'mean')
).reset_index()

# Filter
filtered = decade_stats[decade_stats['num_books'] >= 10].sort_values('avg_rating', ascending=False)

print("__RESULT__:")
print(filtered.to_json(orient='records'))"""

env_args = {'var_function-call-10950425838561352528': ['books_info'], 'var_function-call-10950425838561353321': ['review'], 'var_function-call-10712812817850489547': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-6482929610006440304': [{'count': '200'}], 'var_function-call-6482929610006441743': [{'COUNT(*)': '1833'}], 'var_function-call-8759879918507074123': 'file_storage/function-call-8759879918507074123.json', 'var_function-call-8759879918507075314': 'file_storage/function-call-8759879918507075314.json', 'var_function-call-10311261609066122413': '1980s'}

exec(code, env_args)
