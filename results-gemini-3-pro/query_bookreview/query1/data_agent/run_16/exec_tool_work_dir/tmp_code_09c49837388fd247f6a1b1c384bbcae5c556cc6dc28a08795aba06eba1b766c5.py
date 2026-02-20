code = """import json
import re

# Load data
with open(locals()['var_function-call-376818118354549533'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-12151239307840850820'], 'r') as f:
    reviews_data = json.load(f)

print("Books Sample:")
for i, book in enumerate(books_data):
    if i >= 5: break
    print(str(book.get('book_id')) + " : " + str(book.get('details'))[:50])

print("Reviews Sample:")
for i, review in enumerate(reviews_data):
    if i >= 5: break
    print(str(review.get('purchase_id')) + " : " + str(review.get('rating')))

# Check extraction logic
count_years = 0
years_map = {}
year_pattern = re.compile(r'(\d{4})') # simpler regex

for book in books_data:
    b_id = book.get('book_id')
    details = book.get('details')
    if b_id and details:
        matches = year_pattern.findall(details)
        # Filter for 19xx or 20xx
        valid_years = [int(y) for y in matches if 1900 <= int(y) <= 2023]
        if valid_years:
            # take the first valid year
            # but wait, sometimes multiple years appear. E.g. 2004 and 1994.
            # Usually the first one mentioned with "published" or just first 4 digit year is the publication year of THAT edition.
            # I will assume first valid year found.
            y = valid_years[0]
            # parse ID
            try:
                numeric_id = int(b_id.split('_')[1])
                years_map[numeric_id] = y
                count_years += 1
            except:
                pass

print("Extracted Years Count: " + str(count_years))

# Check matching
match_count = 0
for review in reviews_data:
    p_id = review.get('purchase_id')
    if p_id:
        try:
            numeric_id = int(p_id.split('_')[1])
            if numeric_id in years_map:
                match_count += 1
        except:
            pass

print("Match Count: " + str(match_count))
print("__RESULT__:")
print(json.dumps({"match_count": match_count}))"""

env_args = {'var_function-call-517339647158260858': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-6198037707694935438': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-3868684680798016508': [{'count': '200'}], 'var_function-call-7330427797473501159': [{'count(*)': '1833'}], 'var_function-call-9503993025071520628': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_10'}, {'book_id': 'bookid_100'}, {'book_id': 'bookid_101'}, {'book_id': 'bookid_102'}], 'var_function-call-13898444909169505298': [{'purchase_id': 'purchaseid_1'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}, {'purchase_id': 'purchaseid_10'}], 'var_function-call-376818118354549533': 'file_storage/function-call-376818118354549533.json', 'var_function-call-12151239307840850820': 'file_storage/function-call-12151239307840850820.json', 'var_function-call-10387768506906315822': []}

exec(code, env_args)
