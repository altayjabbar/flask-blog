from flaskblog import db, bcrypt


def handle_hashed_password_generate(entered_password):
    return bcrypt.generate_password_hash(entered_password).decode("utf-8")
