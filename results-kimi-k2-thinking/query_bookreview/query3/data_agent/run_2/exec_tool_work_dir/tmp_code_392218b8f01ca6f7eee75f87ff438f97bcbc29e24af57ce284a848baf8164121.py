code = """import json
import pandas as pd

# Read the full books data from the file
books_file_path = "/tmp/tmp2d2egn1w.json"
with open(books_file_path, 'r') as f:
    books_data = json.load(f)

# Convert to DataFrame
df_books = pd.DataFrame(books_data)

# Filter for children's books
childrens_books = df_books[df_books['categories'].str.contains("Children's Books", na=False)]

# Get the list of book_ids for children's books
childrens_book_ids = childrens_books['book_id'].tolist()

print('__RESULT__:')
print(json.dumps({
    'childrens_book_ids': childrens_book_ids,
    'total_childrens_books': len(childrens_book_ids)
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}], 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json'}

exec(code, env_args)
