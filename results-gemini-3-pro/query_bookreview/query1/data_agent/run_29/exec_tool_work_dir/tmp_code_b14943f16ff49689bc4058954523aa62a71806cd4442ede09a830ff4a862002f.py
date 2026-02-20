code = """import json
import re

# Access file paths from local variables
books_path = locals()['var_function-call-3643344284243386123']
reviews_path = locals()['var_function-call-5656924228622163066']

with open(books_path, 'r') as f:
    books_data = json.load(f)

with open(reviews_path, 'r') as f:
    reviews_data = json.load(f)

book_years = {}
year_pattern = re.compile(r'\b(19\d{2}|20\d{2})\b')

for book in books_data:
    b_id_str = book.get('book_id', '')
    details = book.get('details', '')
    
    if not b_id_str or not details:
        continue
    
    try:
        if '_' in b_id_str:
            b_id = int(b_id_str.split('_')[1])
        else:
            b_id = int(b_id_str)
    except:
        continue

    years = [int(y) for y in year_pattern.findall(details)]
    if not years:
        continue
    
    # Debug: store all found years to see distribution
    book_years[b_id] = years[0]

print(f"DEBUG: Processed {len(book_years)} books with years.")

decade_stats = {} 

for rev in reviews_data:
    p_id_str = rev.get('purchase_id', '')
    rating_str = rev.get('rating')
    
    if not p_id_str or rating_str is None:
        continue
        
    try:
        rating = float(rating_str)
    except:
        continue
    
    try:
        if '_' in p_id_str:
            p_id = int(p_id_str.split('_')[1])
        else:
            p_id = int(p_id_str)
    except:
        continue
        
    if p_id in book_years:
        year = book_years[p_id]
        decade = (year // 10) * 10
        decade_str = f"{decade}s"
        
        if decade_str not in decade_stats:
            decade_stats[decade_str] = {'ratings': [], 'books': set()}
        
        decade_stats[decade_str]['ratings'].append(rating)
        decade_stats[decade_str]['books'].add(p_id)

results = []
print("DEBUG: Decade stats:")
for dec, data in decade_stats.items():
    num_books = len(data['books'])
    avg_rating = sum(data['ratings']) / len(data['ratings'])
    print(f"  {dec}: {num_books} books, {len(data['ratings'])} ratings, avg {avg_rating:.2f}")
    if num_books >= 10:
        results.append({'decade': dec, 'avg_rating': avg_rating, 'num_books': num_books})

results.sort(key=lambda x: x['avg_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-13335226208161502359': 'file_storage/function-call-13335226208161502359.json', 'var_function-call-5491435565414936199': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_function-call-8109259769040236212': [{'count': '200'}], 'var_function-call-15734980832244476045': [{'COUNT(*)': '1833'}], 'var_function-call-3643344284243386123': 'file_storage/function-call-3643344284243386123.json', 'var_function-call-5656924228622163066': 'file_storage/function-call-5656924228622163066.json', 'var_function-call-10758695365230782611': []}

exec(code, env_args)
