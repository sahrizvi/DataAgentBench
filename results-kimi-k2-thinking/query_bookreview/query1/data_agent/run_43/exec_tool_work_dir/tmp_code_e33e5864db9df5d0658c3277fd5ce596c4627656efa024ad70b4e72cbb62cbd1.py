code = """import json
import re
from collections import defaultdict

# Load books data
books_data = json.load(open(locals()['var_functions.query_db:24']))

# Load reviews data
reviews_data = json.load(open(locals()['var_functions.query_db:20']))

print(f'Total books: {len(books_data)}, Total reviews: {len(reviews_data)}')

# Create a mapping from the number in book_id to actual book_id
book_map = {}
for book in books_data:
    book_id = book['book_id']
    if '_' in book_id:
        num = book_id.split('_')[1]
        book_map[num] = book_id

# Extract year from details
def extract_year(details_text):
    patterns = [
        r'[^\d](\d{4})[^\d]',
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})',
        r'\b\d{4}\b'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, details_text)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    for element in match:
                        if element.isdigit() and 1900 <= int(element) <= 2023:
                            return int(element)
                elif match.isdigit() and 1900 <= int(match) <= 2023:
                    return int(match)
    return None

# Build book info
book_info = {}
for book in books_data:
    year = extract_year(book['details'])
    if year:
        book_info[book['book_id']] = {
            'year': year,
            'decade': (year // 10) * 10,
            'rating_number': int(book['rating_number']) if book['rating_number'].isdigit() else 0
        }

# Build reviews by book number
book_ratings = defaultdict(list)
for review in reviews_data:
    purchase_id = review['purchase_id']
    if '_' in purchase_id:
        num = purchase_id.split('_')[1]
        if num in book_map:
            book_id = book_map[num]
            book_ratings[book_id].append(float(review['rating']))

print(f'Books with reviews: {len(book_ratings)}')
print(f'Books with publication year: {len(book_info)}')

# Calculate stats by decade
decade_stats = defaultdict(lambda: {'total_rating': 0, 'book_count': 0, 'ratings': []})

for book_id, ratings in book_ratings.items():
    if book_id in book_info and len(ratings) >= 10 and book_info[book_id]['rating_number'] >= 10:
        decade = book_info[book_id]['decade']
        avg_rating = sum(ratings) / len(ratings)
        decade_stats[decade]['total_rating'] += avg_rating
        decade_stats[decade]['book_count'] += 1
        decade_stats[decade]['ratings'].append(avg_rating)

# Filter decades with at least 10 books and calculate average
valid_decades = {}
for decade, stats in decade_stats.items():
    if stats['book_count'] >= 10:
        valid_decades[decade] = {
            'avg_rating': stats['total_rating'] / stats['book_count'],
            'book_count': stats['book_count']
        }

# Find best decade
best_decade = None
max_rating = 0
for decade, info in valid_decades.items():
    if info['avg_rating'] > max_rating:
        max_rating = info['avg_rating']
        best_decade = (decade, info)

print(f'Decades with >=10 books: {len(valid_decades)}')
if best_decade:
    decade, info = best_decade
    print(f'Best decade: {decade}s with avg rating {info["avg_rating"]:.2f} ({info["book_count"]} books)')
    final_result = {'decade': f'{decade}s', 'average_rating': round(info['avg_rating'], 2)}
else:
    final_result = {'error': 'No valid data'}

# Export using proper format
output = json.dumps(final_result)
print('----BEGIN PRINT FORMAT----')
print('__RESULT__:')
print(output)
print('----END PRINT FORMAT----')"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.list_db:6': ['review'], 'var_functions.query_db:8': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}

exec(code, env_args)
