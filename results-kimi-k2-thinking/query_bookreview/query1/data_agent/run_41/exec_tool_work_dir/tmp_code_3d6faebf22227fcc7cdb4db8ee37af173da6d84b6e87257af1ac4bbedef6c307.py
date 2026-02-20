code = """import json
import re

# Read books data
books_file_path = locals()['var_functions.query_db:6']
with open(books_file_path, 'r') as f:
    books = json.load(f)

# Extract publication year from details
year_pattern = r'(\d{4})'
books_with_years = []

for book in books:
    details = book.get('details', '')
    years = re.findall(year_pattern, details)
    
    pub_year = None
    for year in years:
        year_int = int(year)
        if 1900 <= year_int <= 2023:
            pub_year = year_int
            break
    
    if pub_year:
        decade = f"{pub_year//10*10}s"
        books_with_years.append({
            'book_id': book['book_id'],
            'pub_year': pub_year,
            'decade': decade
        })

print('__RESULT__:')
print(json.dumps(books_with_years))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'book_id': 'bookid_5'}], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:10': {'total_books': 200, 'books_with_years': 190, 'sample_books': [{'book_id': 'bookid_1', 'pub_year': 2004, 'decade': '2000s'}, {'book_id': 'bookid_2', 'pub_year': 1996, 'decade': '1990s'}, {'book_id': 'bookid_3', 'pub_year': 2012, 'decade': '2010s'}, {'book_id': 'bookid_4', 'pub_year': 2013, 'decade': '2010s'}, {'book_id': 'bookid_5', 'pub_year': 2014, 'decade': '2010s'}, {'book_id': 'bookid_6', 'pub_year': 2021, 'decade': '2020s'}, {'book_id': 'bookid_7', 'pub_year': 2004, 'decade': '2000s'}, {'book_id': 'bookid_8', 'pub_year': 2015, 'decade': '2010s'}, {'book_id': 'bookid_9', 'pub_year': 2019, 'decade': '2010s'}, {'book_id': 'bookid_10', 'pub_year': 2004, 'decade': '2000s'}]}, 'var_functions.list_db:12': ['review'], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
