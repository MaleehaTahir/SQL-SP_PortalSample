## Report Generation using SQL Stored Procedures

### Basic Setup

1) Clone the repo

2) Create virtual environment (Use either virtualevn or virtualenvwrapper- depending on preference)

3) `pip install -r requirements.txt` (Install all the requirements the project needed)

4) The report detail logic in views.py is able to dynamically support connections with MSSQL and MySQL.

If using MySQL:
a) `pip install "PyMySQL==0.7.10"`
If using Azure:
a) 'pip install "django-pyodbc-azure==1.10.4.0"'

4) Create superuser `python manage.py createsuperuser`

5) Run the server. `python manage.py runserver`