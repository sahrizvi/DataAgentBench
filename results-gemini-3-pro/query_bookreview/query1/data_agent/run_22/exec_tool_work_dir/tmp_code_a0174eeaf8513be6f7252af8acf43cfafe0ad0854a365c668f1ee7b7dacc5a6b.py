code = """import json
import re

# Load data
with open(locals()['var_function-call-3584235163383529166'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-11281961708852073426'], 'r') as f:
    reviews_data = json.load(f)

# Regex for date extraction
date_pattern = re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(?:\d{1,2},?\s+)?(\d{4})', re.IGNORECASE)

book_years = {}
for book in books_data:
    b_id_str = book.get('book_id', '')
    if not b_id_str:
        continue
    m = re.search(r'(\d+)', b_id_str)
    if not m:
        continue
    b_id = int(m.group(1))
    
    details = book.get('details') or ''
    subtitle = book.get('subtitle') or ''
    
    year = None
    matches = date_pattern.findall(details)
    if matches:
        year = int(matches[0])
            
    if year is None:
        matches = date_pattern.findall(subtitle)
        if matches:
            year = int(matches[0])
            
    if year:
        book_years[b_id] = year

# Process reviews
book_ratings = {} # book_id -> list of ratings

for review in reviews_data:
    p_id_str = review.get('purchase_id', '')
    rating_str = review.get('rating')
    
    if not p_id_str or rating_str is None:
        continue
        
    m = re.search(r'(\d+)', p_id_str)
    if not m:
        continue
    p_id = int(m.group(1))
    
    if p_id in book_years:
        if p_id not in book_ratings:
            book_ratings[p_id] = []
        book_ratings[p_id].append(float(rating_str))

decade_book_avgs = {} # decade -> list of book_avgs

for b_id, ratings in book_ratings.items():
    avg = sum(ratings) / len(ratings)
    year = book_years[b_id]
    decade_val = (year // 10) * 10
    decade_str = f"{decade_val}s"
    
    if decade_str not in decade_book_avgs:
        decade_book_avgs[decade_str] = []
    decade_book_avgs[decade_str].append(avg)

results = []
for decade, avgs in decade_book_avgs.items():
    if len(avgs) >= 10:
        decade_avg = sum(avgs) / len(avgs)
        results.append({'decade': decade, 'decade_avg': decade_avg, 'num_books': len(avgs)})

results.sort(key=lambda x: x['decade_avg'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-11182770986839170833': ['books_info'], 'var_function-call-775582157750101986': 'file_storage/function-call-775582157750101986.json', 'var_function-call-7631044117126092351': ['review'], 'var_function-call-14911875712140264538': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_function-call-3584235163383529166': 'file_storage/function-call-3584235163383529166.json', 'var_function-call-11281961708852073426': 'file_storage/function-call-11281961708852073426.json', 'var_function-call-4477002312610133791': [{'decade': '2020s', 'avg_rating': 4.663636363636364, 'num_books': 21}, {'decade': '2010s', 'avg_rating': 4.608591885441528, 'num_books': 88}, {'decade': '2000s', 'avg_rating': 4.276223776223776, 'num_books': 47}, {'decade': '1980s', 'avg_rating': 4.208333333333333, 'num_books': 11}, {'decade': '1990s', 'avg_rating': 3.823529411764706, 'num_books': 17}], 'var_function-call-12347635403078611279': [{'count': '200'}], 'var_function-call-665172939754764108': {'qualified_decades': [{'decade': '2020s', 'avg_rating': 4.663636363636364, 'num_books': 21}, {'decade': '2010s', 'avg_rating': 4.608591885441528, 'num_books': 88}, {'decade': '2000s', 'avg_rating': 4.276223776223776, 'num_books': 47}, {'decade': '1980s', 'avg_rating': 4.208333333333333, 'num_books': 11}, {'decade': '1990s', 'avg_rating': 3.823529411764706, 'num_books': 17}], 'all_decades': [{'decade': '2010s', 'avg_rating': 4.608591885441528, 'num_books': 88}, {'decade': '2020s', 'avg_rating': 4.663636363636364, 'num_books': 21}, {'decade': '2000s', 'avg_rating': 4.276223776223776, 'num_books': 47}, {'decade': '1990s', 'avg_rating': 3.823529411764706, 'num_books': 17}, {'decade': '1980s', 'avg_rating': 4.208333333333333, 'num_books': 11}, {'decade': '1970s', 'avg_rating': 4.285714285714286, 'num_books': 2}, {'decade': '1940s', 'avg_rating': 5.0, 'num_books': 1}, {'decade': '1880s', 'avg_rating': 4.25, 'num_books': 1}, {'decade': '1930s', 'avg_rating': 5.0, 'num_books': 2}], 'failed_books_count': 10, 'failed_books_sample': [{'book_id': 27, 'details': 'This book is written in English and has an ISBN-10 of 0553819399 and an ISBN-13 of 978-0553819397. It weighs 1.06 pounds and has dimensions of 5 inches in width, 1.65 inches in depth, and 7.8 inches in height.', 'subtitle': 'Paperback'}, {'book_id': 90, 'details': '', 'subtitle': 'Unknown Binding'}, {'book_id': 97, 'details': 'This book is written in English and has an ISBN 10 of 1938923391 and an ISBN 13 of 978-1938923395. It weighs 14.4 ounces.', 'subtitle': 'Hardcover'}, {'book_id': 102, 'details': 'This book has an ISBN-10 number of 1925849058 and an ISBN-13 number of 978-1925849059. It weighs 1.06 pounds and has dimensions of 9.13 inches in width, 0.35 inches in depth, and 11.93 inches in height.', 'subtitle': 'Hardcover'}, {'book_id': 103, 'details': '', 'subtitle': 'None'}]}}

exec(code, env_args)
