code = """import json
import re

# Load data
with open(locals()['var_function-call-17651092371273879762']) as f:
    books = json.load(f)
with open(locals()['var_function-call-13505292961120283604']) as f:
    reviews = json.load(f)

# Parse books to get Year
book_years = {}
for b in books:
    bid = b['book_id'] 
    # Extract ID number from book_id (e.g. "bookid_1" -> "1")
    match_id = re.search(r'(\d+)', bid)
    if not match_id: continue
    id_num = match_id.group(1)
    
    details = b['details']
    # Regex for "Month Day, Year"
    date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', details)
    if date_match:
        date_str = date_match.group(1)
        # Extract year from the date string
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            year = int(year_match.group(1))
            book_years[id_num] = year

# Process reviews
decade_stats = {} # {decade: {'sum': 0, 'count': 0, 'books': set()}}

for r in reviews:
    pid = r['purchase_id'] # e.g. "purchaseid_186" -> "186"
    match_id = re.search(r'(\d+)', pid)
    if not match_id: continue
    id_num = match_id.group(1)
    
    if id_num in book_years:
        year = book_years[id_num]
        decade = (year // 10) * 10
        decade_str = f"{decade}s"
        
        try:
            rating = float(r['rating'])
        except:
            continue
            
        if decade_str not in decade_stats:
            decade_stats[decade_str] = {'sum': 0, 'count': 0, 'books': set()}
        
        decade_stats[decade_str]['sum'] += rating
        decade_stats[decade_str]['count'] += 1
        decade_stats[decade_str]['books'].add(id_num)

# Calculate averages
results = []
for dec, data in decade_stats.items():
    n_distinct = len(data['books'])
    if n_distinct >= 10:
        avg_rating = data['sum'] / data['count']
        results.append({'decade': dec, 'avg_rating': avg_rating, 'distinct_books': n_distinct})

# Sort by rating
results.sort(key=lambda x: x['avg_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-10955878956823461812': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-11153851190749344620': [{'COUNT(*)': '1833'}], 'var_function-call-6691633111925274378': [{'count': '200'}], 'var_function-call-17651092371273879762': 'file_storage/function-call-17651092371273879762.json', 'var_function-call-13505292961120283604': 'file_storage/function-call-13505292961120283604.json'}

exec(code, env_args)
