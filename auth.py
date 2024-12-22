from flask import Blueprint, request, render_template, session, redirect, url_for

from users import check_account, create_account

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        current_id = check_account(username, password)
        if not username or not password:
            error = "Please enter both a username and password."
        elif current_id:
            session['logged_in'] = True
            session['user_id'] = current_id
            print(current_id)
            return redirect(url_for('pages.home'))
        else:
            error = "Wrong username/password"
            return render_template('login.html', error=error)
    if session.get('logged_in'):
        return redirect(url_for('pages.home'))
    else:
        return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return redirect(url_for('auth.login_page'))
    else:
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm-password']

        if not username or not password:
            msg = "Not so easy, you need to fill the form."
        elif password != confirm:
            msg = "Passwords don't match"
        else:
            msg = create_account(username, password)

        return render_template('login.html', msg=msg)