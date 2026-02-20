code = """import json

# Re-run aggregation with average of averages
# Load data (using previous variable names)
with open(locals()['var_function-call-376818118354549533'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-12151239307840850820'], 'r') as f:
    reviews_data = json.load(f)

# Hardcode the mapping logic from previous successful run
import re
year_pattern = re.compile(r'(\d{4})')
book_years = {}
for book in books_data:
    try:
        numeric_id = int(book['book_id'].split('_')[1])
        matches = year_pattern.findall(book['details'])
        valid = [int(y) for y in matches if 1900 <= int(y) <= 2024]
        if valid:
            book_years[numeric_id] = valid[0]
    except:
        pass

# Group by decade -> book -> ratings
decade_book_ratings = {}

for review in reviews_data:
    try:
        numeric_id = int(review['purchase_id'].split('_')[1])
        rating = float(review['rating'])
        if numeric_id in book_years:
            year = book_years[numeric_id]
            decade = (year // 10) * 10
            d_key = f"{decade}s"
            if d_key not in decade_book_ratings:
                decade_book_ratings[d_key] = {}
            if numeric_id not in decade_book_ratings[d_key]:
                decade_book_ratings[d_key][numeric_id] = []
            decade_book_ratings[d_key][numeric_id].append(rating)
    except:
        pass

results = []
for decade, books in decade_book_ratings.items():
    if len(books) >= 10:
        # Calculate average of book averages
        book_avgs = []
        for b_id, ratings in books.items():
            book_avgs.append(sum(ratings)/len(ratings))
        
        avg_of_avgs = sum(book_avgs)/len(book_avgs)
        results.append({'decade': decade, 'avg': avg_of_avgs})

results.sort(key=lambda x: x['avg'], reverse=True)
print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-517339647158260858': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-6198037707694935438': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-3868684680798016508': [{'count': '200'}], 'var_function-call-7330427797473501159': [{'count(*)': '1833'}], 'var_function-call-9503993025071520628': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_10'}, {'book_id': 'bookid_100'}, {'book_id': 'bookid_101'}, {'book_id': 'bookid_102'}], 'var_function-call-13898444909169505298': [{'purchase_id': 'purchaseid_1'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}], 'var_function-call-376818118354549533': 'file_storage/function-call-376818118354549533.json', 'var_function-call-12151239307840850820': 'file_storage/function-call-12151239307840850820.json', 'var_function-call-10387768506906315822': [], 'var_function-call-7874784583553533931': {'match_count': 1806}, 'var_function-call-3284905331004808650': [], 'var_function-call-6237062701652751181': [], 'var_function-call-2885200148784417529': [], 'var_function-call-12337143209398467410': [{'decade': '2020s', 'avg_rating': 4.663636363636364, 'num_books': 21}, {'decade': '2010s', 'avg_rating': 4.608591885441528, 'num_books': 88}, {'decade': '2000s', 'avg_rating': 4.276223776223776, 'num_books': 47}, {'decade': '1980s', 'avg_rating': 4.208333333333333, 'num_books': 11}, {'decade': '1990s', 'avg_rating': 3.8208955223880596, 'num_books': 16}]}

exec(code, env_args)
