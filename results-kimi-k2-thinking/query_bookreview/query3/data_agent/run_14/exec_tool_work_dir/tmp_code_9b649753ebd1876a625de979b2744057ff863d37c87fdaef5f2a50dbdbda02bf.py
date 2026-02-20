code = """import json

# Load books data
books_path = var_functions.query_db:14
reviews_path = var_functions.query_db:18

with open(books_path) as f:
    books_data = json.load(f)

with open(reviews_path) as f:
    reviews_data = json.load(f)

# Filter children's books
children_books = {}
for book in books_data:
    categories = book.get('categories', '')
    if categories and "Children's Books" in categories:
        book_id = book.get('book_id')
        numeric_id = book_id.split('_')[1]  # assumes bookid_XX
        children_books[numeric_id] = {
            'book_id': book_id,
            'title': book.get('title'),
            'categories': categories,
            'total_ratings': int(book.get('rating_number', 0)),
        }

# Process reviews from 2020+
reviews_2020 = {}
for review in reviews_data:
    review_time = review.get('review_time', '')
    if review_time >= '2020-01-01':
        purchase_id = review.get('purchase_id', '')
        numeric_id = purchase_id.split('_')[1]  # assumes purchaseid_XX
        if numeric_id in children_books:
            rating = float(review.get('rating', 0))
            if numeric_id not in reviews_2020:
                reviews_2020[numeric_id] = []
            reviews_2020[numeric_id].append(rating)

# Compute average ratings and filter
result = []
for numeric_id, ratings in reviews_2020.items():
    if len(ratings) >= 1:
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating >= 4.5:
            book = children_books[numeric_id]
            result.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'average_rating': round(avg_rating, 2),
                'num_reviews_2020': len(ratings),
            })

# Sort by average rating desc
result = sorted(result, key=lambda x: x['average_rating'], reverse=True)

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'rating_number': '40'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'rating_number': '5'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]', 'rating_number': '294'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]', 'rating_number': '3'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '447'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]', 'rating_number': '61'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]', 'rating_number': '10'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]', 'rating_number': '12'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '2'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]', 'rating_number': '51'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]', 'rating_number': '100'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]', 'rating_number': '5'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]', 'rating_number': '17'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'rating_number': '418'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '2'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]', 'rating_number': '28'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '2'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '4'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]', 'rating_number': '123'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '26'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'rating_number': '20'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]', 'rating_number': '234'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'rating_number': '188'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]', 'rating_number': '7'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]', 'rating_number': '182'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}

exec(code, env_args)
