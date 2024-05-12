import json
from models import Author, Quote
import connect
import os

print("Current directory:", os.getcwd())

# Load authors from JSON
with open('data/authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

# Load quotes from JSON
with open('data/quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Save authors to database
for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

# Save quotes to database
for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data['author']).first()
    if author:
        quote = Quote(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote']
        )
        quote.save()
    else:
        print(f"Author '{quote_data['author']}' not found. Skipping quote.")

print("Data loaded successfully.")

