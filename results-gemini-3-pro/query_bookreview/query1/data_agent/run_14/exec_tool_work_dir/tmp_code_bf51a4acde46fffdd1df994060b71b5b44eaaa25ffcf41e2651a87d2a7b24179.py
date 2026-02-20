code = """import json
import re
import pandas as pd

# Load data (using file paths)
with open('var_function-call-5211450942838871426', 'r') as f:
    books_data = json.load(f)

with open('var_function-call-5211450942838872577', 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract integer ID
def extract_id(s):
    if not s: return None
    match = re.search(r'(\d+)', str(s)) # Search anywhere for digits
    if match:
        return int(match.group(1))
    return None

df_books['id'] = df_books['book_id'].apply(extract_id)
df_reviews['id'] = df_reviews['purchase_id'].apply(extract_id)

# Extract year
def extract_year(s):
    if not s: return None
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', str(s))
    if years:
        return int(years[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Filter valid years
valid_books = df_books.dropna(subset=['year']).copy()
valid_books['decade'] = (valid_books['year'] // 10) * 10
valid_books['decade_str'] = valid_books['decade'].astype(int).astype(str) + 's'

# Calculate average rating per book
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()

# Merge
merged = pd.merge(valid_books, book_ratings, on='id', how='inner')

# Stats
decade_stats = merged.groupby('decade_str').agg(
    num_books=('id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

print("Books with year extracted:", len(valid_books))
print("Sample years:", valid_books['year'].head().tolist())
print("Books with ratings:", len(book_ratings))
print("Merged records:", len(merged))
print("Decade stats:\n", decade_stats)

# Check distinct books count per decade
print("Distinct books per decade:\n", decade_stats[['decade_str', 'num_books']])

result = "Debug output printed"
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-15022840946230034989': ['books_info'], 'var_function-call-15022840946230034796': ['review'], 'var_function-call-13134580431996322376': 'file_storage/function-call-13134580431996322376.json', 'var_function-call-13134580431996323685': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_function-call-4303025065553681561': [{'count': '200'}], 'var_function-call-4303025065553680718': [{'COUNT(*)': '1833'}], 'var_function-call-5211450942838871426': 'file_storage/function-call-5211450942838871426.json', 'var_function-call-5211450942838872577': 'file_storage/function-call-5211450942838872577.json', 'var_function-call-11608517781291732052': 'No decade met the criteria'}

exec(code, env_args)
