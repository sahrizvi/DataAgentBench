code = """import json
import pandas as pd

# Load books
books = locals()['var_function-call-4878923825151006451']
# Create a dict mapping book_id to title
book_map = {b['book_id']: b['title'] for b in books}

# Load reviews
with open(locals()['var_function-call-12426343001213376417'], 'r') as f:
    reviews = json.load(f)

# Aggregate ratings
book_ratings = {} # book_id -> list of ratings

for r in reviews:
    pid = r['purchase_id']
    rating = float(r['rating'])
    
    # Transform purchase_id to book_id
    # Assuming purchaseid_X maps to bookid_X
    if pid.startswith('purchaseid_'):
        bid = pid.replace('purchaseid_', 'bookid_')
    else:
        continue # Should not happen based on inspection, but good to be safe
    
    if bid in book_map:
        if bid not in book_ratings:
            book_ratings[bid] = []
        book_ratings[bid].append(rating)

# Calculate average and filter
result_titles = []
for bid, ratings in book_ratings.items():
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 4.5:
        result_titles.append(book_map[bid])

print("__RESULT__:")
print(json.dumps(result_titles))"""

env_args = {'var_function-call-4878923825151006451': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-16026717946873242670': [{'review_time': '2012-11-24 18:52:00'}], 'var_function-call-12426343001213376417': 'file_storage/function-call-12426343001213376417.json'}

exec(code, env_args)
