code = """import pandas as pd
import json
import re

# Load data
with open(locals()['var_function-call-17894281087799120001'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-10804233732653904371'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Helper function to extract year
def extract_year(text):
    if not isinstance(text, str):
        return None
    # Use negative lookbehind/lookahead to match standalone 4-digit numbers
    matches = re.findall(r'(?<!\d)(\d{4})(?!\d)', text)
    valid_years = []
    for m in matches:
        y = int(m)
        if 1900 <= y <= 2023:
            valid_years.append(y)
    
    if valid_years:
        # Prioritize finding the year near "published"
        # But for now, returning the first valid standalone year is a good heuristic
        return valid_years[0]
    
    # Fallback: simple 4 digits (might be inside ISBN)
    # This is a last resort if no standalone year found.
    # But risky. Let's stick to standalone for now.
    return None

# Helper function to extract ID
def extract_id(text):
    if not isinstance(text, str):
        return None
    nums = re.findall(r'\d+', text)
    if nums:
        return int(nums[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books['id_num'] = df_books['book_id'].apply(extract_id)
df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_id)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Drop missing year
df_books = df_books.dropna(subset=['year'])

# Convert to decade
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(int).astype(str) + 's'

# Merge
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Aggregation
decade_stats = merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    book_count=('id_num', 'nunique')
).reset_index()

filtered_decades = decade_stats[decade_stats['book_count'] >= 10].copy()

if not filtered_decades.empty:
    top_decade = filtered_decades.sort_values(by='avg_rating', ascending=False).iloc[0]
    result = top_decade['decade_str']
    print("__RESULT__:")
    print(json.dumps(result))
else:
    # Return debug info if still failing
    debug_info = {
        "error": "No matching decade found",
        "decade_stats": decade_stats.to_dict(orient='records'),
        "num_books_with_year": len(df_books),
        "num_merged": len(merged)
    }
    print("__RESULT__:")
    print(json.dumps(debug_info))"""

env_args = {'var_function-call-17059339761565009177': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_function-call-9213104948124402828': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-7911499635210337761': [{'count': '200'}], 'var_function-call-8929464142869219078': [{'count(*)': '1833'}], 'var_function-call-17894281087799120001': 'file_storage/function-call-17894281087799120001.json', 'var_function-call-10804233732653904371': 'file_storage/function-call-10804233732653904371.json', 'var_function-call-14339715515068141070': [], 'var_function-call-15495888401854620138': 'No matching decade', 'var_function-call-11996045412878413355': 'No matching decade', 'var_function-call-7799512705933983585': 'No matching decade', 'var_function-call-12733628764489441373': {'num_books_total': 200, 'num_books_with_year': 0, 'num_reviews': 1833, 'num_merged': 0, 'decades_found': []}, 'var_function-call-6438822990247770325': 'Done', 'var_function-call-15021485785679607446': {'type': "<class 'dict'>", 'keys': ['book_id', 'details'], 'details_val': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'details_type': "<class 'str'>"}, 'var_function-call-11652979756638418210': {'error': 'No matching decade found', 'decade_stats': [], 'num_books_with_year': 0, 'num_merged': 0}, 'var_function-call-3544841301047232231': 'Done', 'var_function-call-12934686643718123080': {'first_details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'matches_any_4digit': ['2004', '0701', '1698', '0701', '1698'], 'matches_b_4digit': [], 'valid_years': [2004]}}

exec(code, env_args)
