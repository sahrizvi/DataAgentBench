code = """import json
from collections import defaultdict

print('Debug: Accessing stored results...')
# Access stored results
books_result = locals()['var_functions.query_db:16']
reviews_result = locals()['var_functions.query_db:20']

print(f'Books type: {type(books_result)}')
print(f'Reviews type: {type(reviews_result)}')
print(f'Books length: {len(books_result) if isinstance(books_result, list) else "not a list"}')
print(f'Reviews length: {len(reviews_result) if isinstance(reviews_result, list) else "not a list"}')

# Calculate average ratings for each book
book_reviews = defaultdict(list)
for review in reviews_result:
    book_reviews[review['purchase_id']].append(review['rating'])

book_avg_ratings = {}
for purchase_id, ratings in book_reviews.items():
    # Convert ratings to float
    ratings_numeric = [float(r) for r in ratings]
    avg_rating = sum(ratings_numeric) / len(ratings_numeric)
    book_avg_ratings[purchase_id] = avg_rating

print(f'Number of books with reviews: {len(book_avg_ratings)}')

# Find books with perfect 5.0 average rating
perfect_books = [pid for pid, avg in book_avg_ratings.items() if avg == 5.0]
print(f'Books with perfect 5.0 rating: {len(perfect_books)}')

# Filter Literature & Fiction books in English
lit_fiction_books = []
for book in books_result:
    categories = str(book.get('categories', ''))
    details = str(book.get('details', ''))
    
    # Check if it's Literature & Fiction and English
    if 'Literature & Fiction' in categories and 'English' in details:
        lit_fiction_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book.get('author', 'None'),
            'categories': categories,
            'details': details
        })

print(f'Total Literature & Fiction books in English: {len(lit_fiction_books)}')

# Match with perfect ratings
result_books = []
for book in lit_fiction_books:
    book_id = book['book_id']
    # Map book_id to purchase_id pattern (bookid_X -> purchaseid_X)
    purchase_id = book_id.replace('bookid_', 'purchaseid_')
    
    if purchase_id in book_avg_ratings and book_avg_ratings[purchase_id] == 5.0:
        book['average_rating'] = 5.0
        book['review_count'] = len(book_reviews[purchase_id])
        result_books.append(book)

print(f'Perfect 5.0 Literature & Fiction books: {len(result_books)}')

# Format output
output = []
for book in result_books:
    try:
        # Parse author name from the author JSON string
        author_str = str(book['author'])
        if author_str != 'None' and '"name"' in author_str:
            import ast
            author_dict = ast.literal_eval(author_str)
            author_name = author_dict.get('name', 'Unknown')
        else:
            author_name = book.get('author', 'Unknown')
    except:
        author_name = str(book.get('author', 'Unknown'))
    
    output.append({
        'title': book['title'],
        'author': author_name,
        'book_id': book['book_id'],
        'average_rating': 5.0,
        'review_count': book.get('review_count', 0)
    })

print('__RESULT__:')
print(json.dumps(output, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:9': 'file_storage/functions.query_db:9.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': [{'total_books': '200'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}

exec(code, env_args)
