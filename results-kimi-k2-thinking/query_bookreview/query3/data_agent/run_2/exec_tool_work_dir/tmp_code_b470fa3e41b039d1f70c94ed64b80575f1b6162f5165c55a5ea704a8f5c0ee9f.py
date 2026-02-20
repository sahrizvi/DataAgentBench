code = """import json
import re
from collections import defaultdict

# Read the full data from the files
# The children's books data is in var_functions.query_db:14 (already a list)
# The reviews data is in var_functions.query_db:18 (file path)

# Read children's books data (this is already filtered)
children_books = var_functions.query_db_14

# Read reviews data from 2020 onwards
with open('/tmp/tmpr8s80_46.json', 'r') as f:
    reviews = json.load(f)

# Extract book IDs from children_books
children_book_ids = {book['book_id'] for book in children_books}

# Create mapping from purchase_id to numeric ID
def extract_numeric_id(book_id_str):
    """Extract numeric part from bookid_X or purchaseid_X"""
    match = re.search(r'(book|purchase)id_(\d+)', str(book_id_str))
    if match:
        return int(match.group(2))
    return None

# Map numeric IDs to book info for children's books
children_books_numeric = {}
for book in children_books:
    numeric_id = extract_numeric_id(book['book_id'])
    if numeric_id is not None:
        children_books_numeric[numeric_id] = book

print('__RESULT__:')
print(json.dumps({
    'children_books_count': len(children_books),
    'children_books_ids_sample': list(children_book_ids)[:5],
    'reviews_count': len(reviews),
    'children_books_numeric_keys_sample': list(children_books_numeric.keys())[:5]
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}], 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:10': [{'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2020-02-27 05:11:00'}, {'purchase_id': 'purchaseid_167', 'rating': '2', 'review_time': '2020-06-01 07:33:00'}, {'purchase_id': 'purchaseid_23', 'rating': '5', 'review_time': '2021-07-31 18:34:00'}, {'purchase_id': 'purchaseid_99', 'rating': '2', 'review_time': '2021-01-27 07:08:00'}, {'purchase_id': 'purchaseid_167', 'rating': '4', 'review_time': '2020-06-14 11:52:00'}, {'purchase_id': 'purchaseid_20', 'rating': '5', 'review_time': '2021-10-31 19:46:00'}, {'purchase_id': 'purchaseid_83', 'rating': '5', 'review_time': '2021-06-22 12:04:00'}, {'purchase_id': 'purchaseid_67', 'rating': '3', 'review_time': '2021-02-10 16:28:00'}, {'purchase_id': 'purchaseid_62', 'rating': '5', 'review_time': '2020-04-16 04:41:00'}], 'var_functions.query_db:14': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}

exec(code, env_args)
