
# Maredipudi Nagalakshmi Beauty Lounge

A beauty salon website built using HTML, CSS, JavaScript and Python Flask.

## Features

- Beauty salon homepage
- About section
- Beauty services
- Makeup packages
- Appointment booking form
- Python Flask backend
- SQLite booking storage
- Admin appointment dashboard

## Technologies

- HTML
- CSS
- JavaScript
- Python
- Flask
- SQLite
- Render

## Run Locally

1. Install Python 3.10 or newer.
2. Open the project folder in a terminal.
3. Create a virtual environment:

   python -m venv .venv

4. Activate it on Windows:

   .venv\Scripts\activate

5. Install dependencies:

   pip install -r requirements.txt

6. Start the application:

   python app.py

7. Open this address in your browser:

   http://127.0.0.1:5000

## Deployment

This project includes render.yaml for deployment on Render.

Connect your GitHub repository to Render and deploy the application.

## Important Notes

- SQLite data on Render's free service may not persist after restarts or redeployments.
- Use persistent PostgreSQL storage for reliable bookings.
- Add password protection to the admin dashboard before public use.
- SAP integration is not included yet.
