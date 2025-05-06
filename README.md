# ORIGINAL PYTHON APP I MADE (Console Program)
https://github.com/DanjoBanjo03/pythonJobTrackerApp

# Job Application Tracker

A simple web application to track job applications built with Flask.

## Features

- Track job applications with company, position, date applied, and status
- Search for applications by company name
- Add, edit, and delete job applications
- Visual status indicators (Applied, Interview, Offer, Rejected)

## Installation

1. Clone the repository
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, use the Flask command:

```
flask run
```

The application will be available at http://127.0.0.1:5000/

## Project Structure

- `app.py`: Main application file with routes
- `models.py`: Database models
- `forms.py`: Form definitions using Flask-WTF
- `templates/`: HTML templates
  - `base.html`: Base template with navigation
  - `index.html`: Job listing page
  - `form.html`: Add/edit job form