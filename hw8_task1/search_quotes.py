from models import Quote, Author
from mongoengine import connect
import configparser

# Load MongoDB connection details from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# Connect to MongoDB
connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

def search_quotes(command):
    command_parts = command.split(':', 1)
    if len(command_parts) != 2:
        print("Invalid command format. Please use 'name:', 'tag:', or 'tags:' followed by the search term.")
        return

    search_type, search_term = command_parts[0], command_parts[1].strip()

    if search_type == 'name':
        author = Author.objects(fullname=search_term).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print(f"No quotes found for author '{search_term}'.")

    elif search_type == 'tag':
        quotes = Quote.objects(tags=search_term)
        for quote in quotes:
            print(quote.quote)

    elif search_type == 'tags':
        search_terms = search_term.split(',')
        quotes = Quote.objects(tags__in=search_terms)
        for quote in quotes:
            print(quote.quote)

    else:
        print("Invalid search type. Please use 'name:', 'tag:', or 'tags:'.")

if __name__ == "__main__":
    while True:
        command = input("Enter your search command (e.g., 'name: Author Name', 'tag: Tag Name', 'tags: Tag1,Tag2'): ")
        if command.lower() == 'exit':
            break
        search_quotes(command)
