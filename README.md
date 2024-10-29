# cmpe273-book-reader-django
```
smartcity-backend/
├── ai_lambda/ (All AI related APIs or lambda)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all AI/lambda APIs)
├── authentication/ (Google OAuth2 and our own authentication system)
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
│   ├── views.py  (all google_book_test APIs will be in this views.py)
├── list_history/  (Reading list page and reading history page)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all list_history APIs will be in this views.py)
├── main_search_single/  (Main page, search page and single book information page)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all main_search_single APIs will be in this views.py)
├── reading_page/  (book content reading page)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py  (all reading_page APIs will be in this views.py)
├── static/
├── gitignore
├── manage.py
├── README.md
├── requirements.txt
```

## To run our Django backend locally:
- Create a python virtual environment and activate it:
For Windows:
```bash 
python -m venv venv
```
```bash
venv\Scripts\activate
```
For Mac:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
- Download .env file from the link and replace any id or secret with your own, remember to rename this to ".env": 
https://drive.google.com/file/d/1Zq3CLyC3t8XmZef8mMqHE_euytEeyMye/view?usp=sharing
- Install all packages with:
```bash
pip install -r requirements.txt
```
- In order to use the Django migration (optional) on our AWS RDS MySQL DB (let Django create database tables for you according to your models.py), you will need to install mysql and mysql-connector-c. - Here's an introduction of Django migration: https://www.youtube.com/watch?v=aOLrEkpGWDg


