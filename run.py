from flaskblog import create_app

app = create_app()

if __name__ == "__main__":
    """
    Entry point for running the Flask application.

    Starts the Flask application using the create_app() function from the Flaskblog package.

    Usage:
        python app.py

    """
    app.run()
