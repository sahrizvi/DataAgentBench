code = """import json
import re

# Load children's books
books_data = locals()['var_functions.query_db:12']
childrens_books = []
for book in books_data:
    try:
        # Parse categories string to list
        categories_str = book['categories']
        # Extract list using regex in case it's a string representation
        categories_match = re.search(r'\[(.*?)\]', categories_str)
        if categories_match:
            categories_list = json.loads(categories_str)
            # Check if any category contains "Children" (case-insensitive)
            if any('children' in cat.lower() for cat in categories_list):
                childrens_books.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'categories': categories_list
                })
    except:
        # Fallback: check raw string
        if 'children' in book['categories'].lower():
            childrens_books.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'categories': book['categories']
            })

# Load reviews from 2020 onwards (file path)
reviews_file_path = locals()['var_functions.query_db:8']
if isinstance(reviews_file_path, str):
    with open(reviews_file_path, 'r') as f:
        import json
        reviews_2020 = json.load(f)
else:
    reviews_2020 = reviews_file_path

# Extract book_id from purchase_id (remove 'purchaseid_' prefix)
for review in reviews_2020:
    review['book_id'] = review['purchase_id'].replace('purchaseid_', 'bookid_')

# Create mappings
childrens_book_ids = {book['book_id'] for book in childrens_books}
book_titles = {book['book_id']: book['title'] for book in childrens_books}

# Filter reviews for children's books only
childrens_reviews = [r for r in reviews_2020 if r['book_id'] in childrens_book_ids]

# Calculate average rating per book
from collections import defaultdict
book_ratings = defaultdict(list)
for review in childrens_reviews:
    book_id = review['book_id']
    rating = float(review['rating'])
    book_ratings[book_id].append(rating)

# Calculate averages
book_avg_ratings = {}
for book_id, ratings in book_ratings.items():
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 4.5:
        book_avg_ratings[book_id] = {
            'title': book_titles.get(book_id, 'Unknown'),
            'avg_rating': round(avg_rating, 2),
            'review_count': len(ratings)
        }

# Sort by average rating descending
sorted_books = sorted(book_avg_ratings.items(), key=lambda x: x[1]['avg_rating'], reverse=True)

# Format results
result_books = [
    {
        'title': book_data['title'],
        'average_rating': book_data['avg_rating'],
        'review_count': book_data['review_count']
    }
    for book_id, book_data in sorted_books
]

__RESULT__ = json.dumps(result_books, ensure_ascii=False)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}], 'var_functions.query_db:3': [{'purchase_id': 'purchaseid_186', 'review_time': '2012-11-24 18:52:00', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'review_time': '2015-12-31 13:35:00', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'review_time': '2013-05-05 10:47:00', 'rating': '4'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}], 'var_functions.query_db:12': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}]}

exec(code, env_args)
