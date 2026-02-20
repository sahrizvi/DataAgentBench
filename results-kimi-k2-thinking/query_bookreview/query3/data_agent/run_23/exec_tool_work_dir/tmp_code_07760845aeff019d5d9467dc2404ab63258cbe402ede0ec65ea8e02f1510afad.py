code = """import json
import pandas as pd

# Load the database information
rl_books_info = var_functions.list_db:0
rl_review = var_functions.list_db:2

print('Books info tables:', rl_books_info)
print('Review tables:', rl_review)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review']}

exec(code, env_args)
