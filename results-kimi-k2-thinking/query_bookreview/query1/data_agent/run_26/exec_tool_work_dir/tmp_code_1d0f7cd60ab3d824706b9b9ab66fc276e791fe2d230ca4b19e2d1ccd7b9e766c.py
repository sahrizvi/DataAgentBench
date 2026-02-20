code = """import json
import re
from collections import defaultdict, Counter

# Load data
books_file = locals()['var_functions.query_db:14']
reviews_file = locals()['var_functions.query_db:16']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Extract publication year from details
book_years = {}
for book in books_data:
    book_id = book['book_id']
    details = book.get('details', '')
    
    # Look for 4-digit year in details
    year_match = re.search(r'(\b19\d{2}\b|\b20\d{2}\b)', details)
    if year_match:
        year = int(year_match.group(1))
        book_years[book_id] = year

print(f'Extracted years for {len(book_years)} books')

# Map purchase_id to ratings (convert to int/float)
purchase_ratings = {}
for review in reviews_data:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    if purchase_id not in purchase_ratings:
        purchase_ratings[purchase_id] = []
    purchase_ratings[purchase_id].append(rating)

print(f'Found ratings for {len(purchase_ratings)} purchase_ids')

# Map book_id to purchase_id (they're the same format)
# bookid_X -> purchaseid_X
book_to_purchase = {}
for book in books_data:
    book_id = book['book_id']
    # Extract number from book_id
    num_match = re.search(r'bookid_(\d+)', book_id)
    if num_match:
        purchase_id = f'purchaseid_{num_match.group(1)}'
        book_to_purchase[book_id] = purchase_id

print(f'Mapped {len(book_to_purchase)} books to purchase_ids')

# Calculate average rating per book
book_avg_ratings = {}
books_with_ratings = 0
for book_id, purchase_id in book_to_purchase.items():
    if book_id in book_years and purchase_id in purchase_ratings:
        ratings = purchase_ratings[purchase_id]
        avg_rating = sum(ratings) / len(ratings)
        book_avg_ratings[book_id] = {
            'year': book_years[book_id],
            'avg_rating': avg_rating,
            'rating_count': len(ratings)
        }
        books_with_ratings += 1

print(f'Books with both year and ratings: {books_with_ratings}')

# Group by decade
decade_stats = defaultdict(lambda: {'total_rating': 0, 'book_count': 0, 'books': []})
for book_id, data in book_avg_ratings.items():
    year = data['year']
    decade = (year // 10) * 10
    decade_stats[decade]['total_rating'] += data['avg_rating']
    decade_stats[decade]['book_count'] += 1
    decade_stats[decade]['books'].append({
        'book_id': book_id,
        'year': year,
        'avg_rating': data['avg_rating']
    })

print(f'Books grouped into {len(decade_stats)} decades')

# Filter decades with at least 10 books and calculate average
valid_decades = []
for decade, stats in decade_stats.items():
    if stats['book_count'] >= 10:
        avg_rating = stats['total_rating'] / stats['book_count']
        valid_decades.append({
            'decade': decade,
            'avg_rating': avg_rating,
            'book_count': stats['book_count']
        })

# Sort by avg_rating descending
valid_decades.sort(key=lambda x: x['avg_rating'], reverse=True)

print(f'\nDecades with >= 10 books: {len(valid_decades)}')
for d in valid_decades[:10]:
    print(f"{d['decade']}s: {d['avg_rating']:.3f} ({d['book_count']} books)")

if valid_decades:
    best_decade = valid_decades[0]
    result = f"{best_decade['decade']}s"
else:
    result = "No decades found with at least 10 books"

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:10': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}], 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:20': 'Data loading completed'}

exec(code, env_args)
