code = """import json
import pandas as pd

# Load the book information
books_info_file = open(locals()['var_function-call-8645819040871599000'])
books_info = json.load(books_info_file)
books_info_file.close()

# Extract book_ids
book_ids = [book["book_id"] for book in books_info]

# Create a dictionary to store book_id and title
book_data = {book["book_id"]: {"title": book["title"], "categories": book["categories"], "details": book["details"]} for book in books_info}

print("__RESULT__:")
print(json.dumps(book_ids))"""

env_args = {'var_function-call-8645819040871599000': 'file_storage/function-call-8645819040871599000.json'}

exec(code, env_args)
