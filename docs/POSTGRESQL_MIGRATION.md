# PostgreSQL Migration Guide

## Step 1: Install PostgreSQL
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Install PostgreSQL with default settings
3. Remember the password you set for the 'postgres' user during installation

## Step 2: Create Database
Open PostgreSQL command line (psql) or pgAdmin and run:

```sql
CREATE DATABASE attendance_db;
```

Or use command line:
```powershell
psql -U postgres
CREATE DATABASE attendance_db;
\q
```

## Step 3: Install Python Package
```powershell
pip install psycopg2-binary
```

## Step 4: Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Update the database credentials in `.env`:
   - DB_PASSWORD: Your PostgreSQL password
   - DB_USER: Usually 'postgres' (default)
   - DB_NAME: attendance_db

## Step 5: Load Environment Variables
Add this to the top of settings.py (already done):
```python
from dotenv import load_dotenv
load_dotenv()
```

## Step 6: Export Data from SQLite (Optional)
If you want to keep existing data:

```powershell
# Export data from SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data_backup.json
```

## Step 7: Run Migrations
```powershell
# Create new tables in PostgreSQL
python manage.py makemigrations
python manage.py migrate
```

## Step 8: Import Data (Optional)
If you backed up data:
```powershell
python manage.py loaddata data_backup.json
```

## Step 9: Create Superuser
```powershell
python manage.py createsuperuser
```

## Step 10: Test
```powershell
python manage.py runserver
```

## Troubleshooting

### Error: "psycopg2 not found"
```powershell
pip install psycopg2-binary
```

### Error: "connection refused"
- Check if PostgreSQL service is running
- Verify host and port in .env file
- Check PostgreSQL pg_hba.conf for connection permissions

### Error: "password authentication failed"
- Verify DB_PASSWORD in .env matches PostgreSQL password
- Try connecting with psql to verify credentials

### Error during data import
- Create superuser first: `python manage.py createsuperuser`
- Import data: `python manage.py loaddata data_backup.json`
- If issues persist, manually re-create data through admin panel
