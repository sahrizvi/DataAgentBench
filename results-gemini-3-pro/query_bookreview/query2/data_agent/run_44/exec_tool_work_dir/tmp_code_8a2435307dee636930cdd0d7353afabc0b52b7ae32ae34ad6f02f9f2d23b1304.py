code = """import json
import pandas as pd

# Access the file paths from the previous tool results
books_file = locals()['var_function-call-16095753841730177593']
reviews_file = locals()['var_function-call-16095753841730175994']

# Load data
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Process books
valid_books = {} # key: common_id, value: title
for book in books_data:
    try:
        # The categories field is a string representation of a list
        cats = json.loads(book['categories'])
    except Exception as e:
        # Fallback if json.loads fails (e.g. single quotes)
        # But based on sample it looks like standard JSON string
        continue
    
    if "Literature & Fiction" in cats:
        details = book.get('details', '')
        if 'English' in details:
            bid = book['book_id']
            # extract id, assuming format "bookid_X"
            if bid.startswith("bookid_"):
                common_id = bid.split('_')[1]
                valid_books[common_id] = book['title']

# Process reviews
book_ratings = {} # key: common_id, value: list of ratings
for review in reviews_data:
    pid = review['purchase_id']
    if pid.startswith("purchaseid_"):
        common_id = pid.split('_')[1]
        
        # Only care if it's a valid book (English & Literature & Fiction)
        if common_id in valid_books:
            if common_id not in book_ratings:
                book_ratings[common_id] = []
            try:
                book_ratings[common_id].append(float(review['rating']))
            except:
                pass

# Calculate averages and filter
result_titles = []
for cid, ratings in book_ratings.items():
    if not ratings:
        continue
    avg = sum(ratings) / len(ratings)
    if abs(avg - 5.0) < 1e-9: # float comparison for perfect 5.0
        result_titles.append(valid_books[cid])

print("__RESULT__:")
print(json.dumps(result_titles))"""

env_args = {'var_function-call-3846895235627032233': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-3846895235627029356': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-8347230730248741581': [{'count': '200'}], 'var_function-call-8347230730248743536': [{'COUNT(*)': '1833'}], 'var_function-call-16095753841730177593': 'file_storage/function-call-16095753841730177593.json', 'var_function-call-16095753841730175994': 'file_storage/function-call-16095753841730175994.json'}

exec(code, env_args)
