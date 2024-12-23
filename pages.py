from connection import get_db
from flask import Flask, Blueprint, render_template, redirect, session, url_for, request
from fics import get_posts, get_user_posts, find_post, find_post1, insert_post, delete_post, update_post
import pandas as pd
from fic import blog_posts
from datetime import date

pages_bp = Blueprint('pages', __name__)

@pages_bp.route("/home")
@pages_bp.route("/")
def home():
    if session.get("logged_in"):
        posts = get_user_posts(session["user_id"])
        session["PostId"] = None
        return render_template('index.html', posts=posts, id=session["user_id"])
    else:
        return redirect(url_for('auth.login_page'))

@pages_bp.route("/welcome")
def welcome():
    if session.get("logged_in"):
        return render_template('enter.html')
    else:
        return redirect(url_for('auth.login_page'))

@pages_bp.route("/profile")
def profile():
    if session.get("logged_in"):
        return render_template('profile.html')
    else:
        return redirect(url_for('auth.login_page'))
    
@pages_bp.route("/addpost", methods=['GET', 'POST'])
def addpost():
    if session.get("logged_in"):
        if request.method == 'GET':
            return render_template('addpost.html', post_data={})
        else:
            post_data = {
                'UserID': session['user_id'],
                'Title': request.form['post-title'],
                'Author': request.form['post-author'],
                'Content': request.form['post-content'],
                'Tags': request.form['post-tags'],
                'Permalink': request.form['post-link'],
                'published_on': date.today()
            }
            existing_post = find_post(post_data['Permalink'])
            if existing_post:
                error = "This link already exists!"
                return render_template('addpost.html', post_data=post_data, error=error)
            else:
                insert_post(post_data) 
                return redirect(url_for('pages.home'))
    else:
        return redirect(url_for('auth.login_page'))

@pages_bp.route("/editpost", methods=['GET', 'POST'])
def editpost():
    if session.get("logged_in"):
        if request.method == 'GET':
            return render_template('editpost.html', post_data={})
        else:
            post_data = {
                'UserID': session['user_id'],
                'Title': request.form['post-title'],
                'Author': request.form['post-author'],
                'Content': request.form['post-content'],
                'Permalink': request.form['post-link'],
                'Tags:': request.form['post-tags'],
            }
            existing_post = find_post(post_data['Permalink'])
            if existing_post:
                post_data.update({'PostId': existing_post['PostId']})
                update_post(post_data) 
                return redirect(url_for('pages.home'))
            else:
                error1 = 'Link does not exist.'
                return render_template('editpost.html', post_data={}, error1=error1)
    else:
        return redirect(url_for('auth.login_page'))

@pages_bp.route("/deletepost", methods=['GET', 'POST'])
def deletepost():
    if session.get("logged_in"):
        if request.method == 'GET':
            return render_template('deletepost.html')
        else:
            post_data = {
                'Permalink': request.form["Link"],
            }
            existing_post = find_post(post_data['Permalink'])
            if existing_post:
                delete_post(existing_post['PostID'])
                return redirect(url_for('pages.home'))
            redirect(url_for('pages.home'))
    else:
        return redirect(url_for('auth.login_page'))