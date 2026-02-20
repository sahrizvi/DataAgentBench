code = """import json
import os

# Load the final results
results_file = "file_storage/functions.execute_python:46.json"
with open(results_file, 'r') as f:
    results = json.load(f)

# Clean up author names and format the final list
formatted_results = []
for book in results:
    author_name = book['author']
    if author_name != 'Unknown' and author_name.startswith('{'):
        # Try to extract author name from JSON string
        try:
            author_data = json.loads(author_name.replace("'", '"'))
            if isinstance(author_data, dict) and 'name' in author_data:
                author_name = author_data['name']
        except:
            # If parsing fails, keep original but truncate if too long
            if len(author_name) > 100:
                author_name = author_name[:100] + "..."
    
    formatted_results.append({
        'title': book['title'],
        'author': author_name,
        'average_rating': book['average_rating'],
        'review_count': book['review_count']
    })

# Format as plain text for the final answer
output_lines = []
output_lines.append("Books categorized as 'Children's Books' with average rating >= 4.5 (2020 onwards):")
output_lines.append("")

if not formatted_results:
    output_lines.append("No books found matching the criteria.")
else:
    for i, book in enumerate(formatted_results, 1):
        output_lines.append(f"{i}. {book['title']}")
        output_lines.append(f"   Author: {book['author']}")
        output_lines.append(f"   Average Rating: {book['average_rating']} (based on {book['review_count']} reviews)")
        output_lines.append("")

print('__RESULT__:')
print(json.dumps("\n".join(output_lines)))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': [], 'var_functions.execute_python:12': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.list_db:5', 'var_functions.query_db:7'], 'var_functions.query_db:14': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:30': ['var_functions.query_db:2', 'var_functions.query_db:7', 'var_functions.query_db:14', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28'], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:33': 'file_storage/functions.query_db:33.json', 'var_functions.execute_python:36': {'books_key': 'var_functions.query_db:32', 'reviews_key': 'var_functions.query_db:33', 'all_keys': [{'var_functions.query_db:2': 'file_storage/functions.query_db:2.json'}, {'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}, {'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}, {'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}, {'var_functions.query_db:26': 'file_storage/functions.query_db:26.json'}]}, 'var_functions.execute_python:38': ['var_functions.query_db:2', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28', 'var_functions.query_db:32', 'var_functions.query_db:33'], 'var_functions.execute_python:40': {'books_count': 25, 'reviews_count': 329, 'sample_book': {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'author': 'None'}, 'sample_review': {'rating': '5', 'purchase_id': 'purchaseid_8'}}, 'var_functions.execute_python:42': 'file_storage/functions.execute_python:42.json', 'var_functions.execute_python:46': 'file_storage/functions.execute_python:46.json'}

exec(code, env_args)
