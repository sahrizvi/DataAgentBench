code = """import json
import pandas as pd

books_data_path = locals()['var_function-call-6280416549282027771']
with open(books_data_path, 'r') as f:
    english_books_info = json.load(f)

reviews_data_path = locals()['var_function-call-16317400724596862313']
with open(reviews_data_path, 'r') as f:
    reviews_info = json.load(f)

english_books_df = pd.DataFrame(english_books_info)
reviews_df = pd.DataFrame(reviews_info)

reviews_df['rating'] = reviews_df['rating'].astype(float)

merged_df = pd.merge(english_books_df, reviews_df, left_on='book_id', right_on='purchase_id', how='inner')

average_ratings = merged_df.groupby('book_id')['rating'].mean().reset_index()

perfect_rating_books = average_ratings[average_ratings['rating'] == 5.0]

final_books = pd.merge(perfect_rating_books, english_books_df, on='book_id', how='inner')

result_titles = final_books['title'].tolist()

print("__RESULT__:")
print(json.dumps(result_titles))"""

env_args = {'var_function-call-5108956238972008348': [], 'var_function-call-4891174312442297353': 'file_storage/function-call-4891174312442297353.json', 'var_function-call-6280416549282027771': 'file_storage/function-call-6280416549282027771.json', 'var_function-call-16317400724596862313': 'file_storage/function-call-16317400724596862313.json'}

exec(code, env_args)
