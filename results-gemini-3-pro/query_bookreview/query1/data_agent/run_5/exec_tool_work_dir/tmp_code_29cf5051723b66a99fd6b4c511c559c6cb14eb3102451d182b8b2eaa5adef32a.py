code = """import json
import re

with open(locals()['var_function-call-2311230859303334761'], 'r') as f:
    books = json.load(f)
with open(locals()['var_function-call-2311230859303334210'], 'r') as f:
    reviews = json.load(f)

# Parse years
book_years = {}
year_pattern = re.compile(r'\b(19\d{2}|20\d{2})\b')

for b in books:
    bid_str = b['book_id']
    try:
        bid = int(bid_str.split('_')[-1])
    except:
        continue
    details = b['details']
    matches = year_pattern.findall(details)
    if matches:
        book_years[bid] = int(matches[0]) 

# Aggregate
decade_stats = {} 
count = 0

for r in reviews:
    pid_str = r['purchase_id']
    try:
        pid = int(pid_str.split('_')[-1])
    except:
        continue
        
    if pid in book_years:
        year = book_years[pid]
        decade = (year // 10) * 10
        decade_key = f"{decade}s"
        
        try:
            rating = float(r['rating'])
        except:
            continue
            
        if decade_key not in decade_stats:
            decade_stats[decade_key] = {'ratings': [], 'books': set()}
            
        decade_stats[decade_key]['ratings'].append(rating)
        decade_stats[decade_key]['books'].add(pid)
        
        if count < 10:
            count += 1

# Calculate averages
qualifying_decades = []
for dec, data in decade_stats.items():
    if len(data['books']) >= 10:
        avg = sum(data['ratings']) / len(data['ratings'])
        qualifying_decades.append({
            "decade": dec,
            "avg": avg,
            "book_count": len(data['books'])
        })

if qualifying_decades:
    best_decade = max(qualifying_decades, key=lambda x: x['avg'])
    print("__RESULT__:")
    print(json.dumps(best_decade['decade']))
else:
    print("__RESULT__:")
    print(json.dumps("None"))"""

env_args = {'var_function-call-6260492085605663425': ['books_info'], 'var_function-call-6260492085605666322': ['review'], 'var_function-call-6260492085605665123': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-2251594135074204042': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17579650686641542669': [{'count': '200'}], 'var_function-call-17579650686641541368': [{'COUNT(*)': '1833'}], 'var_function-call-2311230859303334761': 'file_storage/function-call-2311230859303334761.json', 'var_function-call-2311230859303334210': 'file_storage/function-call-2311230859303334210.json', 'var_function-call-6427252765627234448': [], 'var_function-call-7998034209941558743': [], 'var_function-call-6477357492917874183': 'done', 'var_function-call-3319331179169629068': 'debug done', 'var_function-call-14564568857472799261': 'No matching decade', 'var_function-call-11041369729645761503': 'debug2 done', 'var_function-call-14473951367100814099': 'debug3 done', 'var_function-call-446765211654582787': 'debug4 done', 'var_function-call-4331110729388066165': 'None', 'var_function-call-9524703216429997667': 'None', 'var_function-call-12532257327439469728': 'None', 'var_function-call-13403321478236274990': 'None'}

exec(code, env_args)
