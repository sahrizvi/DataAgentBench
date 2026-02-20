code = """import json, re
from collections import defaultdict
with open(var_call_fDrG1sc4I2e3ps9omdd3uqCt, 'r') as f:
    books = json.load(f)
with open(var_call_y8EP5NY7Cqa0I0WOjhMv4wET, 'r') as f:
    reviews = json.load(f)

# extract first 4-digit year between 1000 and 2023 from details
year_re = re.compile(r"(\d{4})")
book_year = {}
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    found = None
    for m in year_re.finditer(details):
        try:
            y = int(m.group(1))
        except:
            continue
        if 1000 <= y <= 2023:
            found = y
            break
    if found:
        book_year[bid] = found

# process reviews and map purchaseid_N to bookid_N
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    rating = r.get('rating')
    if pid is None or rating is None:
        continue
    try:
        rv = float(rating)
    except:
        continue
    mapped = pid
    if isinstance(pid, str) and pid.startswith('purchaseid_'):
        mapped = 'bookid_' + pid.split('_',1)[1]
    if mapped in book_year:
        book_ratings[mapped].append(rv)

# per-book averages
book_avg = {bid: sum(vals)/len(vals) for bid, vals in book_ratings.items() if len(vals) > 0}

# group by decade
decade_books = defaultdict(list)
for bid, avg in book_avg.items():
    y = book_year.get(bid)
    if not y:
        continue
    decade = f"{(y//10)*10}s"
    decade_books[decade].append((bid, avg))

# compute stats for decades with at least 10 distinct books
decade_stats = {}
for dec, items in decade_books.items():
    n = len(items)
    if n >= 10:
        avg_of_avgs = sum(x[1] for x in items)/n
        decade_stats[dec] = {'num_books': n, 'average_rating': avg_of_avgs}

# find best decade
result = {'decade': None, 'average_rating': None, 'num_books': 0}
if decade_stats:
    best = max(decade_stats.items(), key=lambda x: x[1]['average_rating'])
    dec, stats = best
    result = {'decade': dec, 'average_rating': round(stats['average_rating'],4), 'num_books': stats['num_books']}

# include some diagnostics
out = {'result': result, 'decade_stats': {k: {'num_books': v['num_books'], 'average_rating': round(v['average_rating'],4)} for k,v in decade_stats.items()}, 'counts': {'total_books': len(books), 'books_with_year': len(book_year), 'books_with_ratings': len(book_ratings), 'books_with_ratings_and_year': len(book_avg)}}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_fDrG1sc4I2e3ps9omdd3uqCt': 'file_storage/call_fDrG1sc4I2e3ps9omdd3uqCt.json', 'var_call_y8EP5NY7Cqa0I0WOjhMv4wET': 'file_storage/call_y8EP5NY7Cqa0I0WOjhMv4wET.json', 'var_call_eOXevsxizXoe8OeIplYqdnjD': {'decade': None, 'average_rating': None, 'num_books': 0}, 'var_call_MImcLFzIHXYzmFzIVvR9InOa': {'total_books_in_books_table': 200, 'books_with_extracted_year': 0, 'total_review_records': 1833, 'unique_purchase_ids_in_reviews': 200, 'unique_mapped_ids_from_reviews': 200, 'matched_books_with_reviews_and_year': 0, 'decades_all': {}}, 'var_call_xDRSZ9UX9APvl6YeKI8ejSPd': [{'book_id': 'bookid_1', 'details_preview': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of', 'title': 'Chaucer'}, {'book_id': 'bookid_2', 'details_preview': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN', 'title': 'Notes from a Kidwatcher'}, {'book_id': 'bookid_3', 'details_preview': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363', 'title': 'Service: A Navy SEAL at War'}, {'book_id': 'bookid_4', 'details_preview': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_5', 'details_preview': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it s', 'title': 'Parker & Knight'}, {'book_id': 'bookid_6', 'details_preview': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience'}, {'book_id': 'bookid_7', 'details_preview': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition"}, {'book_id': 'bookid_8', 'details_preview': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-di', 'title': 'Make: Electronics: Learning Through Discovery'}, {'book_id': 'bookid_9', 'details_preview': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-16946217', 'title': 'Reunion: The Children of Lauderdale Park'}, {'book_id': 'bookid_10', 'details_preview': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 o', 'title': 'Four Centuries of American Education'}], 'var_call_3WmtFxZ5o52CifL4RSg38UP9': 'file_storage/call_3WmtFxZ5o52CifL4RSg38UP9.json', 'var_call_zweZGmWFDxpAC1NffYcvE8tc': {'total_books': 200, 'books_with_4digit': 193, 'examples': [{'book_id': 'bookid_1', 'matches': ['2004', '0701', '1698', '0701', '1698'], 'details_preview': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprisi'}, {'book_id': 'bookid_2', 'matches': ['1996', '0435', '0886', '0435', '0886'], 'details_preview': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It '}, {'book_id': 'bookid_3', 'matches': ['2012', '9780', '3161', '8536', '0316'], 'details_preview': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 p'}, {'book_id': 'bookid_4', 'matches': ['2013', '0545', '4255', '0545', '4255'], 'details_preview': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 054'}, {'book_id': 'bookid_5', 'matches': ['2014', '1542'], 'details_preview': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-s'}, {'book_id': 'bookid_6', 'matches': ['2021', '8528', '5377'], 'details_preview': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounc'}, {'book_id': 'bookid_7', 'matches': ['2004', '8082', '1994'], 'details_preview': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item '}, {'book_id': 'bookid_8', 'matches': ['2015', '9781', '6804', '5026', '1680'], 'details_preview': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It ha'}, {'book_id': 'bookid_9', 'matches': ['2019', '1694', '6217', '1694', '6217'], 'details_preview': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1'}, {'book_id': 'bookid_10', 'matches': ['2004', '1932', '2253', '1932', '2253'], 'details_preview': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has a'}, {'book_id': 'bookid_11', 'matches': ['1993', '0893', '0116', '0893', '0116'], 'details_preview': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-08930'}, {'book_id': 'bookid_12', 'matches': ['2022', '9083', '2568', '9083', '2568'], 'details_preview': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of'}, {'book_id': 'bookid_13', 'matches': ['2023', '1771', '6827', '1771', '6827'], 'details_preview': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an '}, {'book_id': 'bookid_14', 'matches': ['2019', '1087', '8485', '1087', '8485'], 'details_preview': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 o'}, {'book_id': 'bookid_15', 'matches': ['2000', '0710', '3069', '0710', '3069'], 'details_preview': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348'}, {'book_id': 'bookid_16', 'matches': ['1997', '0130', '8409', '0130', '8409'], 'details_preview': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in '}, {'book_id': 'bookid_17', 'matches': ['1987', '8477', '1101', '8477', '1101'], 'details_preview': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477'}, {'book_id': 'bookid_18', 'matches': ['2012', '1275', '6272', '1275', '6272'], 'details_preview': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an IS'}, {'book_id': 'bookid_19', 'matches': ['2013', '2013', '1609', '3036', '1609'], 'details_preview': 'The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 160930'}, {'book_id': 'bookid_20', 'matches': ['2003', '2295'], 'details_preview': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of'}]}}

exec(code, env_args)
