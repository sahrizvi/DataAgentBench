code = """import json
import re
import pandas as pd
from collections import defaultdict

# Load the full book details data
books_details_var = 'var_functions.query_db:10'
books_details_result = locals()[books_details_var]

# Load the review data
reviews_var = 'var_functions.query_db:6'
reviews_result = locals()[reviews_var]

# Handle file paths
if isinstance(books_details_result, str):
    with open(books_details_result, 'r') as f:
        book_details = json.load(f)
else:
    book_details = books_details_result

if isinstance(reviews_result, str):
    with open(reviews_result, 'r') as f:
        reviews = json.load(f)
else:
    reviews = reviews_result

# Extract publication year from details
years_by_book = {}
for book in book_details:
    book_id = book['book_id']
    details = book['details']
    
    # Look for 4-digit year in the details string
    year_match = re.search(r'(\d{4})', details)
    if year_match:
        year = int(year_match.group(1))
        years_by_book[book_id] = year
    else:
        # Skip books without a year
        continue

# Calculate average rating per purchase_id (which maps to book_id)
rating_sums = defaultdict(float)
rating_counts = defaultdict(int)

for review in reviews:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    
    # Extract the numeric part from purchase_id and map to book_id format
    match = re.search(r'purchaseid_(\d+)', purchase_id)
    if match:
        book_num = match.group(1)
        book_id = f'bookid_{book_num}'
        
        # Only count if we have publication year for this book
        if book_id in years_by_book:
            rating_sums[book_id] += rating
            rating_counts[book_id] += 1

# Calculate average rating per book
book_avg_ratings = {}
for book_id in rating_sums:
    if rating_counts[book_id] > 0:
        book_avg_ratings[book_id] = rating_sums[book_id] / rating_counts[book_id]

# Group books by decade and calculate metrics
decade_stats = defaultdict(lambda: {'total_rating': 0.0, 'book_count': 0, 'book_ids': set()})

for book_id, avg_rating in book_avg_ratings.items():
    if book_id in years_by_book:
        year = years_by_book[book_id]
        decade = (year // 10) * 10  # e.g., 2004 -> 2000
        
        decade_stats[decade]['total_rating'] += avg_rating
        decade_stats[decade]['book_count'] += 1
        decade_stats[decade]['book_ids'].add(book_id)

# Filter decades with at least 10 distinct books and calculate average
valid_decades = []
for decade, stats in decade_stats.items():
    if stats['book_count'] >= 10:
        avg_rating = stats['total_rating'] / stats['book_count']
        valid_decades.append({
            'decade': f"{decade}s",
            'average_rating': round(avg_rating, 3),
            'book_count': stats['book_count']
        })

# Sort by average rating descending
valid_decades.sort(key=lambda x: x['average_rating'], reverse=True)

print('__RESULT__:')
print(json.dumps({
    'total_books_with_ratings': len(book_avg_ratings),
    'total_books_with_years': len(years_by_book),
    'decades_analyzed': len(decade_stats),
    'valid_decades': valid_decades[:10],  # Top 10 for preview
    'best_decade': valid_decades[0] if valid_decades else None
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:11': {'total_books': 5, 'sample_books': [{'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'subtitle': 'First Edition', 'author': '{"avatar": "https://m.media-amazon.com/images/I/01Kv-W2ysOL._SY600_.png", "name": "Yetta M. Goodman", "about": ["Discover more of the author’s books, see similar authors, read author blogs and more"]}', 'rating_number': '1', 'features': '["Contains 23 selected articles by this influential writer, researcher, educator, and speaker. They\'re grouped around six major themes inherent in teacher education: culture and community; miscue analysis, reading strategies and comprehension; print awareness and the roots of literacy; the writing process; kidwatching; and whole language theory. No index. Annotation c. by Book News, Inc., Portland, Or."]', 'description': '["About the Author", "SANDRA WILDE, Ph.D., is widely recognized for her expertise in developmental spelling and her advocacy of holistic approaches to spelling and phonics. She is Professor of Curriculum and Instruction at Portland State University in Oregon. She is best known for her work in invented spelling, phonics and miscue analysis. She specializes in showing teachers how kids\' invented spellings and miscues can help us work with them in more sophisticated and learner-centered ways. Looking at what kids do as they read and write is at the heart of Sandra\'s presentations and workshops. She can do lively keynote presentations that highlight the interesting things that we can learn by paying close attention to students\' invented spellings and miscues, as well as workshops of varying lengths that focus on student-centered teaching of spelling and phonics. She has recently begun offering workshops that focus on understanding students\' miscues as a guide to appropriate instruction, p"]', 'price': '3.52', 'store': 'Sandra Wilde (Editor)', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'subtitle': 'Hardcover – May 8, 2012', 'author': '{"avatar": "https://m.media-amazon.com/images/I/31rBoNEHiFL._SY600_.jpg", "name": "Marcus Luttrell", "about": ["Petty Officer First Class Marcus Luttrell was born in Huntsville, Texas in 1975."]}', 'rating_number': '3421', 'features': '["Marcus Luttrell, author of the #1 bestseller", "Lone Survivor", ", share war stories about true American heroism from himself and other soldiers who bravely fought alongside him.", "Navy SEAL Marcus Luttrell returned from his star-crossed mission in Afghanistan with his bones shattered and his heart broken. So many had given their lives to save him -- and he would have readily done the same for them. As he recuperated, he wondered why he and others, from America\'s founding to today, had been willing to sacrifice everything-including themselves-for the sake of family, nation, and freedom.  In", "Service", ", we follow Marcus Luttrell to Iraq, where he returns to the battlefield as a member of SEAL Team 5 to help take on the most dangerous city in the world: Ramadi, the capital of war-torn Al Anbar Province. There, in six months of high-intensity urban combat, he would be part of what has been called the greatest victory in the history of U.S. Special Operations forces. We also return to Afghanistan and Operation Redwing, where Luttrell offers powerful new details about his miraculous rescue. Throughout, he reflects on what it really means to take on a higher calling, about the men he\'s seen lose their lives for their country, and the legacy of those who came and bled before.  A thrilling war story,", "Service", "is also a profoundly moving tribute to the warrior brotherhood, to the belief that nobody goes it alone, and no one will be left behind."]', 'description': '["Review", "Praise for SERVICE\\"An action-packed...reflective saga of contemporary military service.\\"―", "Kirkus Reviews", "\\"Marcus Luttrell, with James D. Hornfischer, has written another emotional story that the reader will not want to put down.\\"―", "American Thinker", "About the Author", "Marcus Luttrell", "became a combat-trained Navy SEAL in 2002 and served in many dangerous Special Operations assignments around the world. He is the author of the", "New York Times", "bestseller", "Lone Survivor", ", and is a popular corporate and organizational speaker. He lives near Houston, Texas.\xa0James D. Hornfischer\xa0is the author of four bestselling books on the U.S. Navy in World War II,", "The Fleet at Flood", "Tide", ",", "Neptune\'s", "Inferno, Ship of Ghosts,", "and", "The Last Stand of the Tin Can Sailors,", "winner of the Samuel Eliot Morison Award. He lives in Austin, Texas."]', 'price': '17.17', 'store': 'Marcus Luttrell (Author),  James D. Hornfischer', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}], 'book_id_patterns': ['bookid_2', 'bookid_5', 'bookid_1', 'bookid_4', 'bookid_3']}, 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.execute_python:12': {'books_count': 5, 'book_details_count': 200, 'sample_books': [{'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'subtitle': 'First Edition', 'author': '{"avatar": "https://m.media-amazon.com/images/I/01Kv-W2ysOL._SY600_.png", "name": "Yetta M. Goodman", "about": ["Discover more of the author’s books, see similar authors, read author blogs and more"]}', 'rating_number': '1', 'features': '["Contains 23 selected articles by this influential writer, researcher, educator, and speaker. They\'re grouped around six major themes inherent in teacher education: culture and community; miscue analysis, reading strategies and comprehension; print awareness and the roots of literacy; the writing process; kidwatching; and whole language theory. No index. Annotation c. by Book News, Inc., Portland, Or."]', 'description': '["About the Author", "SANDRA WILDE, Ph.D., is widely recognized for her expertise in developmental spelling and her advocacy of holistic approaches to spelling and phonics. She is Professor of Curriculum and Instruction at Portland State University in Oregon. She is best known for her work in invented spelling, phonics and miscue analysis. She specializes in showing teachers how kids\' invented spellings and miscues can help us work with them in more sophisticated and learner-centered ways. Looking at what kids do as they read and write is at the heart of Sandra\'s presentations and workshops. She can do lively keynote presentations that highlight the interesting things that we can learn by paying close attention to students\' invented spellings and miscues, as well as workshops of varying lengths that focus on student-centered teaching of spelling and phonics. She has recently begun offering workshops that focus on understanding students\' miscues as a guide to appropriate instruction, p"]', 'price': '3.52', 'store': 'Sandra Wilde (Editor)', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}], 'sample_details': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}]}}

exec(code, env_args)
