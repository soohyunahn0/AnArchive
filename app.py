from flask import Flask, render_template, request, redirect, url_for
from users import create_table
from user import setup_profile
from auth import auth_bp
from pages import pages_bp
from fics import create_post_table

app = Flask(__name__)
app.secret_key = "ha9sh(HF*(2))"

with app.app_context():
    create_table()
    setup_profile()
    create_post_table()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pages_bp, url_prefix="/pages")

@app.route("/")
def base():
    return redirect(url_for('auth.login_page'))

@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
