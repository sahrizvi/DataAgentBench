code = """import json
import re

books_path = locals()['var_function-call-3643344284243386123']
reviews_path = locals()['var_function-call-5656924228622163066']

with open(books_path, 'r') as f:
    books_data = json.load(f)

with open(reviews_path, 'r') as f:
    reviews_data = json.load(f)

year_pattern = re.compile(r'19\d{2}|20\d{2}')

book_years = {}
for book in books_data:
    b_id_str = book.get('book_id', '')
    details = book.get('details', '')
    if not b_id_str or not details:
        continue
    try:
        b_id = int(b_id_str.split('_')[1])
    except:
        continue
        
    years = [int(y) for y in year_pattern.findall(details)]
    if years:
        book_years[b_id] = years[0]

# Micro-average: sum of all ratings / total ratings count per decade
decade_sums = {}
decade_counts = {}
decade_books = {}

for rev in reviews_data:
    p_id_str = rev.get('purchase_id', '')
    rating_str = rev.get('rating')
    if not p_id_str or rating_str is None:
        continue
    try:
        p_id = int(p_id_str.split('_')[1])
        rating = float(rating_str)
    except:
        continue
        
    if p_id in book_years:
        year = book_years[p_id]
        decade = (year // 10) * 10
        decade_str = f"{decade}s"
        
        decade_sums[decade_str] = decade_sums.get(decade_str, 0) + rating
        decade_counts[decade_str] = decade_counts.get(decade_str, 0) + 1
        
        if decade_str not in decade_books:
            decade_books[decade_str] = set()
        decade_books[decade_str].add(p_id)

results = []
for dec, total_rating in decade_sums.items():
    num_books = len(decade_books[dec])
    if num_books >= 10:
        avg = total_rating / decade_counts[dec]
        results.append({'decade': dec, 'avg_rating': avg, 'num_books': num_books})

results.sort(key=lambda x: x['avg_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-13335226208161502359': 'file_storage/function-call-13335226208161502359.json', 'var_function-call-5491435565414936199': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_function-call-8109259769040236212': [{'count': '200'}], 'var_function-call-15734980832244476045': [{'COUNT(*)': '1833'}], 'var_function-call-3643344284243386123': 'file_storage/function-call-3643344284243386123.json', 'var_function-call-5656924228622163066': 'file_storage/function-call-5656924228622163066.json', 'var_function-call-10758695365230782611': [], 'var_function-call-16716982898394124464': [], 'var_function-call-11771623797218315282': {'num_books': 200, 'num_reviews_distinct_ids': 200, 'intersection_count': 200, 'sample_intersection': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, 'var_function-call-16420338466314326880': {}, 'var_function-call-8480335068404018563': 'DEBUG_DONE', 'var_function-call-13939793656557054356': ['Total books: 200', 'Book 0 ID: bookid_1, details: Published by Chatto & Windus, the first edition of..., Years: []', 'Book 1 ID: bookid_2, details: This book, published by Heinemann in its first edi..., Years: []', 'Book 2 ID: bookid_3, details: This book, published by Little, Brown and Company ..., Years: []', 'Book 3 ID: bookid_4, details: This book, published by Scholastic Paperbacks in a..., Years: []', 'Book 4 ID: bookid_5, details: The book was published on May 18, 2014, and is ava..., Years: []', 'Extracted years for 0 out of 5 sample books.'], 'var_function-call-6408197233294175672': ['Total books: 200', "Book 0 ID: bookid_1, details: Published by Chatto & Windus, the first edition of..., Years: ['2004', '0701', '1698', '0701', '1698']", "Book 1 ID: bookid_2, details: This book, published by Heinemann in its first edi..., Years: ['1996', '0435', '0886', '0435', '0886']", "Book 2 ID: bookid_3, details: This book, published by Little, Brown and Company ..., Years: ['2012', '9780', '3161', '8536', '0316', '1853']", "Book 3 ID: bookid_4, details: This book, published by Scholastic Paperbacks in a..., Years: ['2013', '0545', '4255', '0545', '4255']", "Book 4 ID: bookid_5, details: The book was published on May 18, 2014, and is ava..., Years: ['2014', '1542']"], 'var_function-call-12528024793707143765': [{'decade': '20s', 'avg_rating': 4.4069679168067415, 'num_books': 156}, {'decade': '10s', 'avg_rating': 4.338929557330179, 'num_books': 35}], 'var_function-call-16101239620866418313': [{'decade': '1980s', 'avg_rating': 4.5481993851559075, 'num_books': 11}, {'decade': '2020s', 'avg_rating': 4.52530525030525, 'num_books': 21}, {'decade': '2010s', 'avg_rating': 4.405139336568189, 'num_books': 88}, {'decade': '2000s', 'avg_rating': 4.357517513775337, 'num_books': 47}, {'decade': '1990s', 'avg_rating': 4.124937996031746, 'num_books': 16}]}

exec(code, env_args)
