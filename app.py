from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

from users import create_table
from user import setup_profile
from auth import auth_bp
from pages import pages_bp
from fics import create_post_table

app = Flask(__name__)

app.secret_key = "14DFJDH@*hJdvkjkSF939EEBCE"

with app.app_context():
    create_table()
    setup_profile()
    create_post_table()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pages_bp, url_prefix="/pages")

@app.route("/")
def base():
    return redirect(url_for('auth.login_page'))

if __name__ == "__main__":
    app.run(debug=True)