## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/wilfex81/Openai_Project
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Set up PostgreSQL:

    - Install PostgreSQL on your system.
    - Create a new database for the project.

2. Update Django settings and .env file to store credentials:

    - In `settings.py`, configure the database settings to use PostgreSQL.

    - Create a `.env` file and add the following:

    ```
    OPENAI_KEY = 'openai api key'
    DB_NAME = 'your db name'
    DB_USER = 'db username'
    DB_PASSWORD = 'db passowrd'
    ```

## Usage

1. Apply migrations:

    ```bash
    python3 manage.py makemigrations

    &&

    python3 manage.py migrate
    ```

2. Run the development server:

    ```bash
    python3 manage.py runserver
    ```

3. Access the web application:

    Open your web browser and navigate to `http://localhost:8000/`.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch from the `main` branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push the branch to your fork: `git push origin feature/my-feature`.
5. Create a pull request against the `main` branch.

## License
