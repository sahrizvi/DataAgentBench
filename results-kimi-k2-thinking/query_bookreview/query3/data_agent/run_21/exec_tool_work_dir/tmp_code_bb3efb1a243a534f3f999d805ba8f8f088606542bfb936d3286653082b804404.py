code = """import json

# Query to get children's books books_info
children_books_query = """SELECT book_id, title, categories FROM books_info WHERE categories LIKE '%Children%';"""
print('__RESULT__:')
print(json.dumps([children_books_query]))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': [{'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}], 'var_functions.query_db:6': [{'review_time': '2012-11-24 18:52:00'}, {'review_time': '2015-12-31 13:35:00'}, {'review_time': '2013-05-05 10:47:00'}, {'review_time': '2020-08-12 11:06:00'}, {'review_time': '2014-11-13 18:55:00'}, {'review_time': '2013-02-20 16:09:00'}, {'review_time': '2020-02-27 05:11:00'}, {'review_time': '2013-01-06 07:52:00'}, {'review_time': '2019-07-24 13:29:00'}, {'review_time': '2020-06-01 07:33:00'}]}

exec(code, env_args)
