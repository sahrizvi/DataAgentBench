code = """import json
import pandas as pd

# Load data
books = locals()['var_function-call-6915360791737479134']
# Since books is a file path, I need to read it. Wait, the previous message says it's stored in a file.
# The `execute_python` instruction says: "If a tool result is large, the next message will include a preview... and the storage entry will be the .json file path..."
# So I should check if it's a list or a string (file path).
# However, the previous tool output for books_info says "The result is too large, so it is stored in a file."
# So `books` variable holds the file path.

with open(books, 'r') as f:
    books_data = json.load(f)

# Ratings data might be small enough to be a list directly, or a file path.
# The tool output for review query says "The result is stored under key... The result is: [...]"
# It shows the list directly in the output preview, and it's small (83 items in preview, total rows likely small).
# Actually, the preview shows the whole list ending with `]`. Let's check the variable type.
# But just in case, I'll handle both.

ratings_raw = locals()['var_function-call-6915360791737478129']
if isinstance(ratings_raw, str) and not ratings_raw.startswith('['):
     with open(ratings_raw, 'r') as f:
        ratings_data = json.load(f)
else:
    ratings_data = ratings_raw

# Create set of purchase_ids with 5.0 rating
# purchase_id format: "purchaseid_123" -> extract 123
perfect_rating_ids = set()
for r in ratings_data:
    pid = r['purchase_id']
    # assume format purchaseid_X
    if '_' in pid:
        num_part = pid.split('_')[1]
        perfect_rating_ids.add(num_part)

final_books = []

for book in books_data:
    # 1. Check ID match
    bid = book['book_id']
    if '_' in bid:
        b_num = bid.split('_')[1]
    else:
        continue # or handle differently
    
    if b_num not in perfect_rating_ids:
        continue

    # 2. Check Category
    cats_str = book['categories']
    try:
        cats_list = json.loads(cats_str)
    except:
        cats_list = []
    
    if "Literature & Fiction" not in cats_list:
        continue

    # 3. Check Language
    details = book['details']
    # Simple check for English
    if "English" not in details:
        continue
    
    final_books.append(book['title'])

print("__RESULT__:")
print(json.dumps(final_books))"""

env_args = {'var_function-call-17090427449786345988': ['books_info'], 'var_function-call-17090427449786346681': ['review'], 'var_function-call-736845554872240804': 'file_storage/function-call-736845554872240804.json', 'var_function-call-736845554872238177': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_function-call-3013423314734406473': [{'count': '200'}], 'var_function-call-8048450402547404679': [{'COUNT(*)': '1833'}], 'var_function-call-6915360791737479134': 'file_storage/function-call-6915360791737479134.json', 'var_function-call-6915360791737478129': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0'}]}

exec(code, env_args)
