code = """import json
import re
from collections import defaultdict

# Access the stored results directly
reviews_data = var_functions.query_db:6
books_data = var_functions.query_db:9

# Parse reviews - extract rating and purchase_id
reviews = []
for review in reviews_data:
    try:
        rating = float(review.get('rating', 0))
        purchase_id = review.get('purchase_id', '')
        if purchase_id and rating > 0:
            reviews.append({
                'purchase_id': purchase_id,
                'rating': rating
            })
    except (ValueError, TypeError):
        continue

# Parse books and extract publication year from details
books = {}  # book_id -> {book_id, publication_year, decade}
year_pattern = r'(\d{4})'

for book in books_data:
    book_id = book.get('book_id', '')
    details = book.get('details', '')
    
    # Find first 4-digit year in details string
    year_match = re.search(year_pattern, details)
    if year_match:
        try:
            year = int(year_match.group(1))
            if 1800 <= year <= 2025:  # Reasonable publication year range
                decade = (year // 10) * 10
                books[book_id] = {
                    'book_id': book_id,
                    'publication_year': year,
                    'decade': f"{decade}s"
                }
        except (ValueError, TypeError):
            continue

# Map purchase_id to book_id and group ratings by book
# purchase_id format: "purchaseid_X" -> book_id: "bookid_X"
book_ratings = defaultdict(list)  # book_id -> list of ratings

for review in reviews:
    purchase_id = review['purchase_id']
    if purchase_id.startswith('purchaseid_'):
        # Extract the number and map to book_id
        book_num = purchase_id.replace('purchaseid_', '')
        book_id = f'bookid_{book_num}'
        
        if book_id in books:
            book_ratings[book_id].append(review['rating'])

# Calculate average rating for each book
book_avg_ratings = {}
for book_id, ratings in book_ratings.items():
    if ratings:
        book_avg_ratings[book_id] = sum(ratings) / len(ratings)

# Group books by decade and calculate decade-level statistics
decade_stats = defaultdict(lambda: {'total_rating': 0, 'book_count': 0, 'book_ids': []})

for book_id, avg_rating in book_avg_ratings.items():
    if book_id in books:
        decade = books[book_id]['decade']
        decade_stats[decade]['total_rating'] += avg_rating
        decade_stats[decade]['book_count'] += 1
        decade_stats[decade]['book_ids'].append(book_id)

# Filter decades with at least 10 distinct books and calculate average rating
eligible_decades = []
for decade, stats in decade_stats.items():
    if stats['book_count'] >= 10:
        avg_rating = stats['total_rating'] / stats['book_count']
        eligible_decades.append({
            'decade': decade,
            'average_rating': round(avg_rating, 3),
            'book_count': stats['book_count']
        })

# Sort by average rating (descending)
eligible_decades.sort(key=lambda x: x['average_rating'], reverse=True)

# Prepare final result with the top decade
result = {
    'top_decade': eligible_decades[0] if eligible_decades else None,
    'total_decades_eligible': len(eligible_decades),
    'all_eligible_decades': eligible_decades
}

print('__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:4': ['review'], 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:9': 'file_storage/functions.query_db:9.json'}

exec(code, env_args)
