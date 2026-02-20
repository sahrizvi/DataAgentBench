code = """import json
import pandas as pd

# Load books
books = locals()['var_function-call-9058295328667650429']

# Load reviews from file
with open(locals()['var_function-call-9058295328667648074'], 'r') as f:
    reviews = json.load(f)

# Process books
book_map = {}
for b in books:
    # book_id format: "bookid_N"
    try:
        bid_str = b['book_id']
        bid_num = int(bid_str.split('_')[1])
        book_map[bid_num] = b['title']
    except:
        continue

# Process reviews
review_data = []
for r in reviews:
    try:
        pid_str = r['purchase_id']
        pid_num = int(pid_str.split('_')[1])
        
        # Only keep reviews for relevant books
        if pid_num in book_map:
            review_data.append({
                'id': pid_num,
                'rating': float(r['rating'])
            })
    except:
        continue

# Calculate averages
if not review_data:
    print("__RESULT__:")
    print("[]")
else:
    df = pd.DataFrame(review_data)
    avg_ratings = df.groupby('id')['rating'].mean()
    
    # Filter >= 4.5
    high_rated_ids = avg_ratings[avg_ratings >= 4.5].index.tolist()
    
    # Get titles
    result_titles = [book_map[i] for i in high_rated_ids]
    
    print("__RESULT__:")
    print(json.dumps(result_titles))"""

env_args = {'var_function-call-11179986791659107585': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}], 'var_function-call-11179986791659106342': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}], 'var_function-call-12570210148830229772': [{'book_id': 'bookid_186', 'title': 'Meat Eater: Adventures from the Life of an American Hunter'}], 'var_function-call-9058295328667650429': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-9058295328667648074': 'file_storage/function-call-9058295328667648074.json'}

exec(code, env_args)
