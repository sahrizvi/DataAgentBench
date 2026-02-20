code = """import json
import re

# Load books with publication years
with open('var_functions.query_db:60.json', 'r') as f:
    books = json.load(f)

# Load review averages
with open('var_functions.query_db:56.json', 'r') as f:
    reviews = json.load(f)

print("Books loaded: " + str(len(books)))
print("Review summaries loaded: " + str(len(reviews)))

# Map reviews by numeric ID
review_map = {}
purchase_pattern = re.compile(r'purchaseid_(\d+)')

for review in reviews:
    purchase_id = review['purchase_id']
    match = purchase_pattern.search(purchase_id)
    if match:
        numeric_id = int(match.group(1))
        review_map[numeric_id] = {
            'avg_rating': float(review['avg_rating']),
            'review_count': int(review['review_count'])
        }

# Filter valid books with valid publication years
valid_books = []
for book in books:
    year = int(book['pub_year'])
    # Skip years before 1900 (likely ISBN artifacts)
    if year >= 1900:
        valid_books.append(book)

print("Valid books (1900+): " + str(len(valid_books)))

# Create book_map for easier lookup
book_map = {}
for book in valid_books:
    match = re.search(r'bookid_(\d+)', book['book_id'])
    if match:
        book_id_num = int(match.group(1))
        book_map[book_id_num] = book

print("Books in map: " + str(len(book_map)))

# Join books with reviews
decade_data = {}
joined_count = 0

for book_id_num in book_map:
    if book_id_num in review_map:
        book = book_map[book_id_num]
        review = review_map[book_id_num]
        
        decade = book['decade']
        
        if decade not in decade_data:
            decade_data[decade] = {
                'books': set(),
                'sum_ratings': 0,
                'total_reviews': 0
            }
        
        decade_data[decade]['books'].add(book_id_num)
        decade_data[decade]['sum_ratings'] += review['avg_rating']
        decade_data[decade]['total_reviews'] += 1
        joined_count += 1

print("Books joined with reviews: " + str(joined_count))

# Calculate decade averages and filter by >=10 books
eligible_decades = []
for decade, data in decade_data.items():
    distinct_books = len(data['books'])
    if distinct_books >= 10:
        avg_rating = data['sum_ratings'] / data['total_reviews']
        eligible_decades.append({
            'decade': decade,
            'avg_rating': avg_rating,
            'distinct_books': distinct_books
        })

print("Decades with >=10 books: " + str(len(eligible_decades)))

# Sort by average rating
eligible_decades.sort(key=lambda x: x['avg_rating'], reverse=True)

# Display results
for d in eligible_decades:
    print(str(d['decade']) + "s: avg=" + str(round(d['avg_rating'],3)) + 
          ", books=" + str(d['distinct_books']))

# Return top decade
if eligible_decades:
    top = eligible_decades[0]
    result = {
        "decade": int(top['decade']),
        "avg_rating": round(top['avg_rating'], 3)
    }
else:
    result = {"error": "No decades meet criteria"}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:18': [{'total_reviews': '1833'}], 'var_functions.query_db:22': 'file_storage/functions.query_db:22.json', 'var_functions.query_db:24': [{'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_12', 'title': 'Heart of Silk and Shadows: A Fae Fantasy Romance (Fae Isles)', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass', 'pub_year': '2023', 'decade': '2020'}, {'book_id': 'bookid_23', 'title': 'The Promise of Love (The Book of Love)', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master', 'pub_year': '2023', 'decade': '2020'}, {'book_id': 'bookid_74', 'title': 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_83', 'title': 'Bisous and Brioche: Classic French Recipes and Family Favorites from a Life in France', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_93', 'title': 'Simantov', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_107', 'title': 'The Grim Hunt: Crown of Madness', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_184', 'title': "The Marquess' Rose: A Regency Romance (Ladies of the North)", 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_122', 'title': 'Childe Harold of Dysna', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_140', 'title': 'The Seep', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_155', 'title': 'Moon Phases 2021-2022 Planner: 2021 Planner, 24 Months Jan 2021 to Dec 2022, 2 Year Calendar 2021-2022 Monthly Planner', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_167', 'title': 'Dead Silence', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_182', 'title': 'Liza of Lambeth', 'pub_year': '2020', 'decade': '2020'}], 'var_functions.query_db:26': [{'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_12', 'title': 'Heart of Silk and Shadows: A Fae Fantasy Romance (Fae Isles)', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass', 'pub_year': '2023', 'decade': '2020'}, {'book_id': 'bookid_23', 'title': 'The Promise of Love (The Book of Love)', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master', 'pub_year': '2023', 'decade': '2020'}, {'book_id': 'bookid_74', 'title': 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_83', 'title': 'Bisous and Brioche: Classic French Recipes and Family Favorites from a Life in France', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_93', 'title': 'Simantov', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_107', 'title': 'The Grim Hunt: Crown of Madness', 'pub_year': '2022', 'decade': '2020'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_184', 'title': "The Marquess' Rose: A Regency Romance (Ladies of the North)", 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_122', 'title': 'Childe Harold of Dysna', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_140', 'title': 'The Seep', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'pub_year': '2021', 'decade': '2020'}, {'book_id': 'bookid_155', 'title': 'Moon Phases 2021-2022 Planner: 2021 Planner, 24 Months Jan 2021 to Dec 2022, 2 Year Calendar 2021-2022 Monthly Planner', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_167', 'title': 'Dead Silence', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'pub_year': '2020', 'decade': '2020'}, {'book_id': 'bookid_182', 'title': 'Liza of Lambeth', 'pub_year': '2020', 'decade': '2020'}], 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.query_db:40': 'file_storage/functions.query_db:40.json', 'var_functions.query_db:42': 'file_storage/functions.query_db:42.json', 'var_functions.query_db:44': [{'decade': '2020', 'total_books': '21', 'distinct_books': '21'}], 'var_functions.query_db:46': 'file_storage/functions.query_db:46.json', 'var_functions.query_db:48': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'first_year': '2004', 'date_year': 'None'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'first_year': '1996', 'date_year': 'None'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'first_year': '2012', 'date_year': 'None'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'first_year': '2013', 'date_year': 'None'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'first_year': '2014', 'date_year': 'None'}, {'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'first_year': '2021', 'date_year': '2021'}, {'book_id': 'bookid_7', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'first_year': '2004', 'date_year': 'None'}, {'book_id': 'bookid_8', 'title': 'Make: Electronics: Learning Through Discovery', 'first_year': '2015', 'date_year': 'None'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'first_year': '2019', 'date_year': 'None'}, {'book_id': 'bookid_10', 'title': 'Four Centuries of American Education', 'first_year': '2004', 'date_year': 'None'}, {'book_id': 'bookid_11', 'title': 'Mining Engineers and the American West: The Lace-Boot Brigarde, 1849-1933', 'first_year': '1993', 'date_year': 'None'}, {'book_id': 'bookid_12', 'title': 'Heart of Silk and Shadows: A Fae Fantasy Romance (Fae Isles)', 'first_year': '2022', 'date_year': 'None'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass', 'first_year': '2023', 'date_year': 'None'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'first_year': '2019', 'date_year': 'None'}, {'book_id': 'bookid_15', 'title': 'Japanese Girls and Women', 'first_year': '2000', 'date_year': 'None'}, {'book_id': 'bookid_16', 'title': 'Behavior Principles in Everyday Life', 'first_year': '1997', 'date_year': 'None'}, {'book_id': 'bookid_17', 'title': 'PQL 3 - Lola (Spanish Edition)', 'first_year': '1987', 'date_year': 'None'}, {'book_id': 'bookid_18', 'title': 'A sermon, preached at the execution of Moses Paul, an Indian: who was executed at New-Haven, on the 2d of September, 1772, for the murder of Mr. Moses ... 1771 : preached at the desire of said Paul.', 'first_year': '2012', 'date_year': 'None'}, {'book_id': 'bookid_19', 'title': 'Business Associations: Agency, Partnerships, LLCs, and Corporations- 2013 Statutes and Rules', 'first_year': '2013', 'date_year': 'None'}, {'book_id': 'bookid_20', 'title': 'Inspector Imanishi Investigates (Soho Crime)', 'first_year': '2003', 'date_year': 'None'}], 'var_functions.query_db:50': 'file_storage/functions.query_db:50.json', 'var_functions.query_db:56': 'file_storage/functions.query_db:56.json', 'var_functions.query_db:60': 'file_storage/functions.query_db:60.json'}

exec(code, env_args)
