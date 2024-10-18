# cmpe273-book-reader-django
```
smartcity-backend/
├── authentication/ (Google OAuth2 combine with Django's own authentication)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all authentication APIs)
├── book_reader_django/ (Main project's app folder)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py  (all configuration goes in here)
│   ├── urls.py  (all app-specific paths goes in here)
│   ├── wsgi.py
├── google_book_test/  (Google Books API tests)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all test APIs will be in this views.py)
├── static/
├── gitignore
├── manage.py
├── README.md
├── requirements.txt
```

## To run our Django backend locally:
### 1. Create a python virtual environment and activate it:
#### Windows:
```bash 
python -m venv venv
```
```bash
venv\Scripts\activate
```
#### Mac:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
### 2. Download .env file from the link: 
https://drive.google.com/file/d/1Zq3CLyC3t8XmZef8mMqHE_euytEeyMye/view?usp=sharing
### 3. install all packages with:
```bash
pip install -r requirements.txt
```
### 4. Install mysql and mysql-connector-c.


## All our test API routes (for localhost just add http://127.0.0.1:8000/ in front)
### To retrive book title search results:
#### api/get-books/ 
### To retrive book title search results with pagination: 
#### api/get-books-paginated/
### To retrive book from specific genre: 
#### api/get-specific-books/
### To retrive user book ratings:
#### api/get-book-reviews/
### To retrive user book reading lists:
#### api/google-books/
### To use Google OAuth2's authorizaion code to exchange for access token from Google:
#### api/exchange-code/