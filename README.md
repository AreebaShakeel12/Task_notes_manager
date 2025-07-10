Smart Productivity Hub: Tasks + AI Notes
Project Overview
This is a comprehensive web application built with Flask that helps users manage their tasks and notes efficiently. It includes robust user authentication, a dynamic task manager with filtering and sorting capabilities, and a notes section powered by Groq AI for intelligent summarization.
This project was developed to showcase full-stack web development skills, combining a Python backend with a responsive frontend.

Features
User Authentication: Secure registration and login system, ensuring personalized access for each user.
Task Management:
Add, edit, and delete tasks with ease.
Mark tasks as complete or incomplete, providing a clear overview of your progress.
Assign due dates and set task priorities (Normal, High, Low) to keep organized.
Filter tasks by status (All, Completed, Active, Has Due Date) and sort them by creation date or due date.
A dashboard provides a quick glance at today's and upcoming tasks, along with overall completion progress.
Notes Section:
Create, view, edit, and delete personal notes.
AI Notes Summarizer: Leveraging the Groq API (specifically the Llama 3 model), this feature generates concise summaries of your longer notes, saving you time and highlighting key information.
Responsive Design: Built with Bootstrap 5, ensuring a clean, modern, and mobile-friendly user interface that looks great on any device.
Tech Stack
Backend: Python, Flask, Flask-SQLAlchemy
Database: PostgreSQL (for production deployment), SQLite (for local development)
Frontend: HTML, CSS (Bootstrap 5), JavaScript
Authentication: Flask-Login, Werkzeug (for password hashing)
Email: Flask-Mail (for potential future features like password reset or notifications)
AI Integration: Groq API (for notes summarization)
Deployment: Render (recommended for ease of use and free tier options)
Dependency Management: pip, requirements.txt
Version Control: Git, GitHub
Setup & Local Development
To get a copy of this project up and running on your local machine, follow these steps.

Prerequisites
Python 3.8+ installed on your system.
pip (Python package installer), usually comes with Python.
vrtualenv or venv (Python's built-in virtual environment module).

Installation Steps
Clone the repository:
Bash
git clone https://github.com/AreebaShakeel12/Task_notes_manager.git
cd Task_notes_manager
Create and activate a virtual environment:
Bash
python -m venv venv
# On Windows (Command Prompt/Git Bash):
# .\venv\Scripts\activate
# On Windows (PowerShell):
# . .\venv\Scripts\Activate.ps1
# On macOS/Linux:
# source venv/bin/activate
Install project dependencies:
Bash
pip install -r requirements.txt
Set up Environment Variables for Local Development:
Create a file named .env in the root of your project directory (the same place as task.py). This .env file should NEVER be committed to Git.

Here's an example of what your .env file might contain for local testing:

Code snippet
# .env - For LOCAL DEVELOPMENT ONLY. Do NOT commit to Git.
SECRET_KEY=your_super_strong_and_random_secret_key_for_dev
MAIL_USERNAME=your_gmail_email@example.com
MAIL_PASSWORD=your_gmail_app_password # Use an App Password if you have 2FA enabled
GROQ_API_KEY=your_groq_api_key_from_dashboard
DATABASE_URL=sqlite:///site.db # Using SQLite for simple local testing
UPLOAD_FOLDER=static/uploads # Relative path for file uploads (if implemented)
SECRET_KEY: Generate a long, random string.
MAIL_USERNAME / MAIL_PASSWORD: Your Gmail credentials for sending emails (consider using an App Password if you have 2-Factor Authentication enabled).
GROQ_API_KEY: Get this from your Groq Console.
DATABASE_URL: For local development, sqlite:///site.db is easy. For local PostgreSQL, it would be postgresql://user:password@localhost:5432/your_database_name.

Initialize the Database:
With your virtual environment activated, run your main application file once. This will create the site.db file (if using SQLite) and necessary database tables.

Bash
python task.py
You can press Ctrl+C to stop the development server after it starts.
Run the application:

Bash
flask run
Your Smart Productivity Hub should now be running locally, typically accessible at http://127.0.0.1:5000/.

How to Use the App
Register: Head to the registration page (/register) to create a new user account.
Login: Log in with your newly created credentials.
Dashboard: Your personalized dashboard gives you a quick overview of today's and upcoming tasks, along with your overall task completion progress.
Tasks: Navigate to the "Tasks" page to manage your to-do list. Here you can add new tasks, mark them as complete, edit their details (title, due date, priority), or delete them. Use the intuitive filter and sort options to organize your view.
Notes: Visit the "Notes" section to create and manage your personal notes. For longer notes, simply click the "Summarize" button to get a concise, AI-generated summary.
Deployment
This application is configured for easy deployment on cloud platforms like  or . These platforms offer robust infrastructure and free tiers suitable for showcasing your project.

Key Deployment Considerations:
Database: You'll need to provision a PostgreSQL database on your chosen hosting platform (e.g., Render's managed PostgreSQL service). Your DATABASE_URL environment variable will then be set to the connection string provided by the platform.

Environment Variables: All sensitive keys (like SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD, GROQ_API_KEY) and dynamic paths (UPLOAD_FOLDER) must be configured as environment variables directly in your hosting platform's dashboard.

Start Command: On Render, your start command will be gunicorn task:app

Contributing
Contributions are welcome! If you find bugs, have feature requests, or want to improve the code, please feel free to fork the repository, create a feature branch, and submit a pull request.

Author
Areeba Shakeel

