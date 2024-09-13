# PujoAtlasKol-Backend

# Running a Python Project After Forking

Follow these steps to set up and run your Python project:

## 1. Clone the Repository

First, clone the repository from GitHub (or another source control system):

```bash
git clone https://github.com/your-username/your-repository.git
```

## 2. Navigate to the Project Directory

Change to the project directory:

```bash
cd your-repository
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

## 4. Activate the Virtual Environment

on windows:

```bash
venv\Scripts\activate
```

on linux/mac

```bash
source venv/bin/activate
```

## 5. Install requirements

```bash
pip install -r requirements.txt
```

## 6. Run Migrations (if applicable)

If your project uses a database and requires migrations, apply them:

```bash
python manage.py migrate
```

## 7. Run Server

```bash
python manage.py runserver
```
