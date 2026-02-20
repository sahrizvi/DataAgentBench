code = """import pandas as pd
import json
import re

# Load data
file_path_books = locals()['var_function-call-5338804074318671779']
with open(file_path_books, 'r') as f:
    books_data = json.load(f)

df_books = pd.DataFrame(books_data)
sample_detail = df_books['details'].iloc[0]

print(f"Sample detail repr: {repr(sample_detail)}")
matches = re.findall(r'\d+', sample_detail)
print(f"All digits found: {matches}")

match = re.search(r'2004', sample_detail)
if match:
    print("Found 2004")
else:
    print("Did not find 2004")

match_b = re.search(r'\b2004\b', sample_detail)
if match_b:
    print("Found 2004 with boundary")
else:
    print("Did not find 2004 with boundary")

print("__RESULT__:")
print(json.dumps({"matches": matches}))"""

env_args = {'var_function-call-7216776813414452879': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7216776813414449292': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5360091024620676715': [{'book_id': 'bookid_186'}], 'var_function-call-5360091024620677050': [{'count': '200'}], 'var_function-call-5360091024620677385': [{'count(*)': '1833'}], 'var_function-call-5338804074318671779': 'file_storage/function-call-5338804074318671779.json', 'var_function-call-5338804074318669420': 'file_storage/function-call-5338804074318669420.json', 'var_function-call-9132499516586371892': [{'decade': '1980s', 'average_rating': 4.5481993851559075, 'book_count': 11}], 'var_function-call-4965347378229887521': {'status': 'debug complete'}, 'var_function-call-2448011590975388297': {'books_count': 200, 'reviews_count': 1833, 'overlap_count': 200, 'books_with_year': 0, 'merged_rows': 1833, 'decade_counts': {}, 'decade_avg_rating': {}}, 'var_function-call-3343962849344017994': {'sample': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'count': 0}}

exec(code, env_args)
