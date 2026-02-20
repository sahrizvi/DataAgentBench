code = """import pandas as pd
import re
import json

# Load the full data from the file path
with open(locals()['var_function-call-6008838561389752942'], 'r') as f:
    books_info = json.load(f)

df_books = pd.DataFrame(books_info)

def extract_year(details):
    # Try to find a 4-digit number that looks like a year, specifically after "published on" or "released on" or "edition on" or "in"
    match_published = re.search(r'(?:published on|released on|edition on|in) (?:January|February|March|April|May|June|July|August|September|October|November|December)?(?: \d{1,2},)? (\d{4})', details)
    if match_published: # If a date is explicitly mentioned with a month and day, use the year from there
        return int(match_published.group(1))

    match_year_in_details = re.search(r'\b(19|20)\d{2}\b', details)
    if match_year_in_details:
        return int(match_year_in_details.group(0))

    return None

df_books['publication_year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['publication_year'])
df_books['publication_year'] = df_books['publication_year'].astype(int)
df_books['publication_decade'] = (df_books['publication_year'] // 10 * 10).astype(str) + "s"

# Select relevant columns
df_books_processed = df_books[['book_id', 'publication_decade']]

print("__RESULT__:")
print(df_books_processed.to_json(orient='records'))"""

env_args = {'var_function-call-6008838561389752942': 'file_storage/function-call-6008838561389752942.json'}

exec(code, env_args)
