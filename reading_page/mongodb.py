from pymongo import MongoClient
from mysql_models.models import Book
import os
import dotenv

dotenv.load_dotenv()

username = os.getenv('AWS_DOCUMENT_DB_MONGO_USERNAME')
password = os.getenv('AWS_DOCUMENT_DB_MONGO_PASSWORD')
host = os.getenv('AWS_DOCUMENT_DB_MONGO_ENDPOINT')
port = os.getenv('AWS_DOCUMENT_DB_MONGO_PORT')
url = f'mongodb://{username}:{password}@{host}:{port}/bookReader?authSource=admin'
mongo_client = MongoClient(url)

db = mongo_client['bookReader']
table = db['Books']


class MongoDBFunctions():
    def getChapter(self, book_name, chapter_number):
        object = table.find_one({'book_name': book_name, 'chapter_number': chapter_number})
        if object:
            o = Book.objects.get(book_name=book_name)
            object['book_cover'] = o.book_cover if o.book_cover else None
            return object
        else:
            return None
    
    def getBook(self, book_name):
        object = table.find({'book_name': book_name})
        document = list(object) if object else None
        if document and len(document) > 0:
            return document
        else:
            return None
        
    def getTableOfContents(self, book_name):
        object = table.find({'book_name': book_name})
        document = list(object) if object else None
        chapter_titles = []
        if document and len(document) > 0:
            chapter_titles = [doc['chapter_title'] for doc in document]
            return chapter_titles
        else:
            return None


if __name__ == '__main__':
    mongo = MongoDBFunctions()
    ## check if connected
    print(mongo.getChapter(1, 1))
