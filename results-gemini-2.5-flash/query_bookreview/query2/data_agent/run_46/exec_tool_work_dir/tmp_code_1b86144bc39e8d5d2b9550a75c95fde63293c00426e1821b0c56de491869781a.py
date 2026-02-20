code = """import json
import pandas as pd

books_data_path = locals()['var_function-call-4891174312442297353']
with open(books_data_path, 'r') as f:
    books_info = json.load(f)

english_books = []
for book in books_info:
    details_str = book['details']
    if "English" in details_str:
        english_books.append(book)

english_books_df = pd.DataFrame(english_books)

print("__RESULT__:")
print(english_books_df.to_json(orient='records'))"""

env_args = {'var_function-call-5108956238972008348': [], 'var_function-call-4891174312442297353': 'file_storage/function-call-4891174312442297353.json'}

exec(code, env_args)
