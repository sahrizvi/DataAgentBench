code = """import json

# Load books (list of dicts)
books = locals()['var_function-call-11785760125649065452']

# Load reviews (from file)
with open(locals()['var_function-call-3408003054206901998'], 'r') as f:
    reviews = json.load(f)

# 1. Map book numeric IDs to titles for the filtered books
target_books = {}
for b in books:
    # book_id format: "bookid_123"
    parts = b['book_id'].split('_')
    if len(parts) > 1:
        num_id = parts[1]
        target_books[num_id] = b['title']

# 2. Aggregate ratings for these books from reviews
# review purchase_id format: "purchaseid_123"
book_ratings = {} # num_id -> [ratings]

for r in reviews:
    p_id = r['purchase_id']
    parts = p_id.split('_')
    if len(parts) > 1:
        num_id = parts[1]
        
        # Check if this review belongs to one of our target books
        if num_id in target_books:
            try:
                rt = float(r['rating'])
                if num_id not in book_ratings:
                    book_ratings[num_id] = []
                book_ratings[num_id].append(rt)
            except ValueError:
                continue

# 3. Calculate average and filter
final_titles = []
for num_id, ratings in book_ratings.items():
    if not ratings:
        continue
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 4.5:
        final_titles.append(target_books[num_id])

print("__RESULT__:")
print(json.dumps(final_titles))"""

env_args = {'var_function-call-11785760125649065452': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-3408003054206901998': 'file_storage/function-call-3408003054206901998.json'}

exec(code, env_args)
