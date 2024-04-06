# spreadsheet-sql-mapper

!["Application Screenshot"](screenshot.png)

A Django RESTful API application capable of processing requests containing spreadsheet files along with corresponding table names. If the specified table does not exist, the application dynamically creates a new table and imports the data from the spreadsheet. The application strictly accepts spreadsheet files in .xls and .xlsx formats. Furthermore, the uploaded spreadsheets must be free of any blank cells to ensure accurate data ingestion.

### Project Prerequisites
- Python 3.12.2
- Django 5.0.2
- Django REST Framework
- Pandas

### Setting up the Repository
1. Clone the repository.
```
git clone https://github.com/johnfritzel/spreadsheet-sql-mapper.git
```

2. Navigate to the project directory.
```
cd spreadsheet-sql-mapper
cd myproject
```

3. Create a virtual environment and activate it.
```
python -m venv <name of virtual environment>
venv\Scripts\activate
```

4. Install the required packages.
```
pip install -r requirements.txt
```

5. Apply migrations to set up the database.
```
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server.
```
python manage.py runserver
```
