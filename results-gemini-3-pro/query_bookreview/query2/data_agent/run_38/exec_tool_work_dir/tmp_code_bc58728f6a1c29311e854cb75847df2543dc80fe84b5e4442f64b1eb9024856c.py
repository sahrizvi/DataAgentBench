code = """import json

# Load books from the new file
books_file_path = locals()['var_function-call-8935132443050667402']
with open(books_file_path, 'r') as f:
    books = json.load(f)

# Load reviews
reviews_file_path = locals()['var_function-call-7740972093692093602']
with open(reviews_file_path, 'r') as f:
    reviews = json.load(f)

# Build ratings map
ratings_map = {}
for r in reviews:
    pid = r['purchase_id']
    rating = float(r['rating'])
    
    if '_' in pid:
        num_id = pid.split('_')[1]
    else:
        continue
        
    if num_id not in ratings_map:
        ratings_map[num_id] = []
    ratings_map[num_id].append(rating)

# Filter books
perfect_books = []
for b in books:
    bid = b['book_id']
    title = b['title']
    
    if '_' in bid:
        num_id = bid.split('_')[1]
    else:
        continue

    if num_id in ratings_map:
        book_ratings = ratings_map[num_id]
        if not book_ratings:
            continue
            
        avg_rating = sum(book_ratings) / len(book_ratings)
        
        if abs(avg_rating - 5.0) < 0.001:
            perfect_books.append(title)

print("__RESULT__:")
print(json.dumps(perfect_books))"""

env_args = {'var_function-call-1703301963755244241': ['books_info'], 'var_function-call-1703301963755242306': ['review'], 'var_function-call-5757682197458839298': [{'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_function-call-2548075812352903264': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-8744837410383458383': 'file_storage/function-call-8744837410383458383.json', 'var_function-call-8460885777306543081': [{'COUNT(*)': '1833'}], 'var_function-call-7740972093692093602': 'file_storage/function-call-7740972093692093602.json', 'var_function-call-1652021002116636854': ['Reunion: The Children of Lauderdale Park', 'The Prophet: With Original 1923 Illustrations by the Author', 'The Melancholy Strumpet Master', 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message', 'Fire Cracker', 'Local Honey', 'Hollywood Confessions: Hollywood Headlines Book #3 (Hollywood Headlines Mysteries)', 'Knowing When To Die: Uncollected Stories', 'Childe Harold of Dysna', 'Forged in Blood (Freehold)', 'Exits, Desires, & Slow Fires', 'Kennebago Moments', 'The Sludge', 'Liza of Lambeth', 'Something That Feels Like Truth (Switchgrass Books)'], 'var_function-call-8935132443050667402': 'file_storage/function-call-8935132443050667402.json'}

exec(code, env_args)
