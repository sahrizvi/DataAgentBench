code = """import json

# Get the five-star ratings list (direct variable)
five_star_list = var_functions.query_db:5

# Get the English Literature & Fiction books file path
books_file = var_functions.query_db:24

# Load the books from the JSON file
with open(books_file, 'r') as f:
    books_list = json.load(f)

# Create a dictionary mapping book numbers to their 5-star rating info
five_star_dict = {}
for row in five_star_list:
    # Parse purchase_id like "purchaseid_101" to extract number
    parts = row['purchase_id'].split('_')
    if len(parts) == 2:
        book_num = int(parts[1])
        five_star_dict[book_num] = row

# Find books that are in Literature & Fiction AND have a 5.0 average rating
results = []
for book in books_list:
    # Parse book_id like "bookid_101" to extract number
    parts = book['book_id'].split('_')
    if len(parts) == 2:
        book_num = int(parts[1])
        
        # Check if this book has a 5-star rating
        if book_num in five_star_dict:
            rating_info = five_star_dict[book_num]
            
            # Extract author name - handle both string and dictionary formats
            author = "Unknown Author"
            author_data = book.get('author', 'Unknown Author')
            if author_data == 'None' or author_data is None:
                author = "Unknown Author"
            else:
                # For complex author data, just use a simplified name if available
                author_str = str(author_data)
                if '"name"' in author_str and ':' in author_str:
                    try:
                        # Simple extraction of name from JSON-like string
                        start = author_str.find('"name"')
                        if start >= 0:
                            start = author_str.find(':', start)
                            if start >= 0:
                                start = author_str.find('"', start)
                                if start >= 0:
                                    end = author_str.find('"', start + 1)
                                    if end >= 0:
                                        author = author_str[start + 1:end]
                    except:
                        author = "Unknown Author"
            
            # Add the matching book to results
            results.append({
                'title': book['title'],
                'author': author,
                'average_rating': float(rating_info['avg_rating']),
                'total_reviews': int(rating_info['rating_count']),
                'details': book['details']
            })

# Output the results in JSON format
output = json.dumps(results, indent=2)
print('__RESULT__:')
print(output)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'rating_count': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'rating_count': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'rating_count': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'rating_count': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'rating_count': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'rating_count': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'rating_count': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'rating_count': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'rating_count': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'rating_count': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'rating_count': '1'}], 'var_functions.query_db:10': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'categories': '["Books", "Arts & Photography", "History & Criticism"]', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'categories': '["Books", "Parenting & Relationships", "Parenting"]', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'title': 'Make: Electronics: Learning Through Discovery', 'categories': '["Books", "Engineering & Transportation", "Engineering"]', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'title': 'Four Centuries of American Education', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}

exec(code, env_args)
