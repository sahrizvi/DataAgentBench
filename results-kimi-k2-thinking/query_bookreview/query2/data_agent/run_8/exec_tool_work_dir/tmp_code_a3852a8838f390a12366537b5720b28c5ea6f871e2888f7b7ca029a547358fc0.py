code = """import json
from collections import defaultdict
import ast
import os

# Load data (they might be file paths or lists)
books_data = locals()['var_functions.query_db:30']
reviews_data = locals()['var_functions.query_db:20']

# Check if they're file paths
if isinstance(books_data, str) and '.json' in books_data and os.path.exists(books_data):
    with open(books_data, 'r') as f:
        books_list = json.load(f)
else:
    books_list = books_data

if isinstance(reviews_data, str) and '.json' in reviews_data and os.path.exists(reviews_data):
    with open(reviews_data, 'r') as f:
        reviews_list = json.load(f)
else:
    reviews_list = reviews_data

# Process reviews - calculate average rating per book
book_ratings = defaultdict(list)
for review in reviews_list:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])  # Convert string to float
    book_ratings[purchase_id].append(rating)

# Find books with perfect 5.0 average rating
perfect_rating_books = {}
for pid, ratings in book_ratings.items():
    if len(ratings) > 0:  # Only consider books with reviews
        avg = sum(ratings) / len(ratings)
        if avg == 5.0:
            perfect_rating_books[pid] = len(ratings)

# Filter Literature & Fiction books in English with perfect 5.0 rating
result_books = []
for book in books_list:
    # Check category
    categories = str(book.get('categories', ''))
    if 'Literature & Fiction' not in categories:
        continue
    
    # Check language
    details = str(book.get('details', ''))
    if 'English' not in details:
        continue
    
    # Map book_id to purchase_id
    book_id = book['book_id']
    purchase_id = book_id.replace('bookid_', 'purchaseid_')
    
    # Check if it has perfect rating
    if purchase_id in perfect_rating_books:
        # Extract author name
        author_raw = book.get('author', 'Unknown')
        author_name = 'Unknown'
        
        if author_raw and author_raw != 'None':
            try:
                author_dict = ast.literal_eval(author_raw)
                if isinstance(author_dict, dict) and 'name' in author_dict:
                    author_name = author_dict.get('name')
                else:
                    author_name = str(author_raw)
            except:
                author_name = str(author_raw)
        
        result_books.append({
            'title': book['title'],
            'author': author_name,
            'book_id': book_id,
            'average_rating': 5.0,
            'review_count': perfect_rating_books[purchase_id]
        })

# Sort by review count (most reviewed first)
result_books.sort(key=lambda x: x['review_count'], reverse=True)

print('__RESULT__:')
print(json.dumps(result_books, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:9': 'file_storage/functions.query_db:9.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': [{'total_books': '200'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:30': 'file_storage/functions.query_db:30.json', 'var_functions.query_db:32': [{'book_id': 'bookid_89'}, {'book_id': 'bookid_69'}, {'book_id': 'bookid_195'}, {'book_id': 'bookid_1'}, {'book_id': 'bookid_167'}, {'book_id': 'bookid_180'}, {'book_id': 'bookid_98'}, {'book_id': 'bookid_122'}, {'book_id': 'bookid_111'}, {'book_id': 'bookid_106'}, {'book_id': 'bookid_99'}, {'book_id': 'bookid_30'}, {'book_id': 'bookid_13'}, {'book_id': 'bookid_109'}, {'book_id': 'bookid_84'}, {'book_id': 'bookid_188'}, {'book_id': 'bookid_177'}, {'book_id': 'bookid_182'}, {'book_id': 'bookid_92'}, {'book_id': 'bookid_49'}, {'book_id': 'bookid_38'}, {'book_id': 'bookid_93'}, {'book_id': 'bookid_142'}, {'book_id': 'bookid_36'}, {'book_id': 'bookid_77'}, {'book_id': 'bookid_179'}, {'book_id': 'bookid_171'}, {'book_id': 'bookid_39'}, {'book_id': 'bookid_187'}, {'book_id': 'bookid_137'}, {'book_id': 'bookid_74'}, {'book_id': 'bookid_82'}, {'book_id': 'bookid_70'}, {'book_id': 'bookid_44'}, {'book_id': 'bookid_55'}, {'book_id': 'bookid_9'}, {'book_id': 'bookid_161'}, {'book_id': 'bookid_144'}, {'book_id': 'bookid_37'}, {'book_id': 'bookid_101'}], 'var_functions.query_db:34': 'file_storage/functions.query_db:34.json', 'var_functions.execute_python:38': {'books_type': "<class 'list'>", 'reviews_type': "<class 'list'>", 'books_count': 40, 'reviews_count': 1833}, 'var_functions.execute_python:44': {'books_count': 40, 'reviews_count': 1833, 'books_preview': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'author': 'None', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}], 'reviews_preview': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}]}}

exec(code, env_args)
