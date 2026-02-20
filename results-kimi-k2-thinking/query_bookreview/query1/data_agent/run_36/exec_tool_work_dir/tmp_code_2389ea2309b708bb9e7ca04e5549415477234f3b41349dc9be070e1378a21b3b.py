code = """import json
import re
from collections import defaultdict

# Load books data
books_path = locals().get('var_functions.query_db:16')
if isinstance(books_path, str) and books_path.endswith('.json'):
    with open(books_path, 'r') as f:
        books = json.load(f)
else:
    books = []

# Load reviews data
reviews_path = locals().get('var_functions.query_db:24')
if isinstance(reviews_path, str) and reviews_path.endswith('.json'):
    with open(reviews_path, 'r') as f:
        reviews = json.load(f)
else:
    reviews = []

# Build book map with publication year
book_map = {}
year_pattern = re.compile(r'\b(\d{4})\b')

for book in books:
    book_id = book.get('book_id')
    if not book_id or 'bookid_' not in book_id:
        continue
    
    try:
        book_num = int(book_id.split('bookid_')[1])
        rating_number = int(book.get('rating_number', 0))
        
        if rating_number <= 0:
            continue
            
        details = book.get('details', '')
        year_match = year_pattern.search(details)
        
        if year_match:
            year = int(year_match.group(1))
            book_map[book_num] = {
                'decade': (year // 10) * 10,
                'year': year,
                'rating_number': rating_number
            }
    except Exception:
        continue

# Group reviews by book and decade
decade_books = defaultdict(set)
book_reviews = defaultdict(list)
decade_reviews = defaultdict(list)

for review in reviews:
    purchase_id = review.get('purchase_id', '')
    if not purchase_id or 'purchaseid_' not in purchase_id:
        continue
    
    try:
        purchase_num = int(purchase_id.split('purchaseid_')[1])
        rating = float(review.get('rating', 0))
        
        if purchase_num in book_map:
            book_reviews[purchase_num].append(rating)
            decade = book_map[purchase_num]['decade']
            decade_books[decade].add(purchase_num)
    except Exception:
        continue

# Calculate average rating per book (that has reviews)
book_avg_ratings = {}
for book_num, ratings in book_reviews.items():
    if len(ratings) > 0:
        book_avg_ratings[book_num] = sum(ratings) / len(ratings)

# Group by decade and calculate weighted average
decade_stats = defaultdict(lambda: {'total_weighted_rating': 0, 'total_reviews': 0, 'books': set()})

for book_num, avg_rating in book_avg_ratings.items():
    if book_num in book_map:
        decade = book_map[book_num]['decade']
        num_reviews = len(book_reviews[book_num])
        
        decade_stats[decade]['total_weighted_rating'] += avg_rating * num_reviews
        decade_stats[decade]['total_reviews'] += num_reviews
        decade_stats[decade]['books'].add(book_num)

# Calculate final averages and filter by minimum 10 distinct books
qualified_decades = {}
for decade, stats in decade_stats.items():
    num_books = len(stats['books'])
    if num_books >= 10:
        avg_rating = stats['total_weighted_rating'] / stats['total_reviews']
        qualified_decades[decade] = {
            'average_rating': avg_rating,
            'distinct_books': num_books,
            'total_reviews': stats['total_reviews']
        }

# Find decade with highest average rating
if qualified_decades:
    best_decade = max(qualified_decades.keys(), key=lambda d: qualified_decades[d]['average_rating'])
    best_data = qualified_decades[best_decade]
    
    # Also get all decades for context
    all_decades = {f"{d}s": round(data['average_rating'], 3) for d, data in qualified_decades.items()}
    
    print('__RESULT__:')
    print(json.dumps({
        'best_decade': f"{best_decade}s",
        'average_rating': round(best_data['average_rating'], 3),
        'distinct_books': best_data['distinct_books'],
        'total_reviews': best_data['total_reviews'],
        'total_decades_qualified': len(qualified_decades),
        'all_qualified_decades': all_decades
    }))
else:
    # Show what we have even if not qualified
    all_decades = {}
    for decade, stats in decade_stats.items():
        if stats['total_reviews'] > 0:
            avg_rating = stats['total_weighted_rating'] / stats['total_reviews']
            all_decades[f"{decade}s"] = {
                'books': len(stats['books']),
                'reviews': stats['total_reviews'],
                'avg_rating': round(avg_rating, 3)
            }
    
    print('__RESULT__:')
    print(json.dumps({
        'message': 'No decade with at least 10 distinct books found',
        'decades_with_data': all_decades,
        'books_with_year_data': len(book_map),
        'books_with_reviews': len(book_reviews)
    }))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:11': 'Read records', 'var_functions.execute_python:10': {'books_count': 5, 'reviews_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, 'sample_review': {'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}}, 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:18': {'total_books': 200, 'rated_books': 0, 'year_extracted_books': 0, 'sample_entries': []}, 'var_functions.execute_python:20': {'total_books': 200, 'rated_books': 0, 'sample_entries': []}, 'var_functions.execute_python:22': {'book_count': 200, 'first_10': [{'book_id': 'bookid_1', 'rating_number': "'29'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is '}, {'book_id': 'bookid_2', 'rating_number': "'1'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is'}, {'book_id': 'bookid_3', 'rating_number': "'3421'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available '}, {'book_id': 'bookid_4', 'rating_number': "'40'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written i'}, {'book_id': 'bookid_5', 'rating_number': "'381'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB a'}, {'book_id': 'bookid_6', 'rating_number': "'5'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pa'}, {'book_id': 'bookid_7', 'rating_number': "'2'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd e'}, {'book_id': 'bookid_8', 'rating_number': "'1366'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is availab'}, {'book_id': 'bookid_9', 'rating_number': "'12'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages.'}, {'book_id': 'bookid_10', 'rating_number': "'133'", 'rating_number_type': 'str', 'has_details': True, 'details_preview': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in '}]}, 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.execute_python:26': {'message': 'No decade found with at least 10 distinct books', 'decades_found': 0, 'all_decades_with_stats': {}}, 'var_functions.execute_python:28': {'total_books': 200, 'total_reviews': 1833, 'book_id_numbers_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'purchase_id_numbers_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'max_book_id': 200, 'max_purchase_id': 200, 'overlap_count': 200}}

exec(code, env_args)
