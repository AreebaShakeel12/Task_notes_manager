# Smart Productivity Hub (or your project name)

This is a Flask-based web application designed to help you manage your notes with AI summarization capabilities.

## Getting Started

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone [https://github.com/AreebaShakeel12/flask-task-manager.git](https://github.com/AreebaShakeel12/flask-task-manager.git)
cd flask-task-manager


### Configuration

This application relies on a `config.json` file to store various application settings, including sensitive API keys and database connection details. For security reasons, this file is **NOT** included in the repository (it's listed in `.gitignore`) and should never be committed to version control.

**Steps to create and populate your `config.json` file:**

1.  **Create the `config.json` file:**
    * In the **root directory** of your project (the same folder where `app.py` and `requirements.txt` are located), create a new file named exactly `config.json`.

2.  **Add the basic structure:**
    * Copy the following JSON structure into your newly created `config.json` file. This defines the `params` object which holds all your configuration variables:

    ```json
    {
      "params": {
        "local_server": true,
        "local_uri": "mysql+pymysql://root:@localhost/smarthub",
        "prod_uri": "mysql+pymysql://root:@localhost/smarthub",
        "gmail_user": "your_gmail_username",
        "gmail_password": "your_gmail_app_password",
        "GROQ_API_KEY": "your_groq_api_key",
        "upload_location": "path/to/your/upload/folder"
      }
    }
    ```

3.  **Populate with your specific details:**

    * **`"local_server": true/false`**:
        * Set to `true` if you are running the application on your local machine for development.
        * Set to `false` if you are deploying to a production server (though typically, this might be handled by environment variables in a production setup).

    * **`"local_uri": "mysql+pymysql://root:@localhost/smarthub"`**:
        * This is your **database connection string for local development**.
        * **`mysql+pymysql`**: Specifies the database type (MySQL) and the Python driver (`pymysql`).
        * **`root:@localhost`**: Your MySQL username (`root`) and an empty password (`:` before `@`). Replace `root` with your actual MySQL username if different. If you have a password for your MySQL user, it would be `username:password@localhost`.
        * **`/smarthub`**: The name of your database. Ensure you have a database named `smarthub` created in your MySQL server, or change this to your desired database name.

    * **`"prod_uri": "mysql+pymysql://root:@localhost/smarthub"`**:
        * This is intended for your **production database connection string**.
        * **Important:** In a real production deployment, this URI will be different (e.g., pointing to a cloud database service) and should ideally be managed via **environment variables** on your hosting platform, not hardcoded here. For a truly production setup, you would likely remove this from `config.json` and use `os.environ.get('DATABASE_URL_PROD')` in your Flask app.

    * **`"gmail_user": "your_gmail_username"`**:
        * Enter your **Gmail email address** here (e.g., `"myemail@gmail.com"`). This is likely used for sending emails (e.g., password resets).

    * **`"gmail_password": "your_gmail_app_password"`**:
        * **CRITICAL:** You should **NOT** use your main Gmail password here. You need to generate a **Gmail App Password**.
        * **How to obtain a Gmail App Password:**
            1.  Go to your Google Account (myaccount.google.com).
            2.  Navigate to "Security."
            3.  Under "How you sign in to Google," select "App passwords." (If you don't see this, you might need to enable 2-Step Verification first).
            4.  Follow the prompts to generate a new app password.
            5.  Copy the 16-character password and paste it here.
        * Example: `"gmail_password": "abcd efgh ijkl mnop"` (without spaces)

    * **`"GROQ_API_KEY": "your_groq_api_key"`**:
        * This key is essential for accessing the Groq API for AI summarization.
        * **How to obtain:**
            1.  Go to the [Groq Console](https://console.groq.com/keys).
            2.  Sign up or log in with your account.
            3.  Navigate to the "API Keys" section.
            4.  Click on "Create new API Key" (or similar button).
            5.  Copy the generated API key (it typically starts with `sk_`).
            6.  Paste this key as the value for `GROQ_API_KEY` in your `config.json`.
        * Example: `"GROQ_API_KEY": "sk_your_actual_groq_api_key_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

    * **`"upload_location": "path/to/your/upload/folder"`**:
        * Specify the **absolute or relative path** to a directory where files (if your application handles uploads) will be stored.
        * Example (relative path, within your project): `"upload_location": "static/uploads"`
        * Example (absolute path for testing, Windows): `"upload_location": "C:\\Users\\YourUser\\Desktop\\flask\\taskmanager\\uploads"` (Note the double backslashes for Windows paths in JSON).
        * Ensure this folder exists and your application has write permissions to it.

**Your final `config.json` file should look similar to this (with your actual, sensitive details):**

```json
{
  "params": {
    "local_server": true,
    "local_uri": "mysql+pymysql://root:your_mysql_password@localhost/smarthub",
    "prod_uri": "mysql+pymysql://username:password@your_production_db_host/your_prod_db",
    "gmail_user": "your_actual_email@gmail.com",
    "gmail_password": "your_generated_gmail_app_password",
    "GROQ_API_KEY": "sk_your_unique_groq_api_key_obtained_from_groq_console",
    "upload_location": "static/uploads"
  }
}