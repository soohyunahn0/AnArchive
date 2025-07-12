from connection import get_db
from flask import Flask, Blueprint, render_template, redirect, session, url_for, request
from fics import get_posts, get_user_posts, find_post, find_post1, insert_post, delete_post, update_post
from user import get_profile, update_profile
from scrape import Scraper
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

@pages_bp.route("/profile", methods=['GET', 'POST'])
def profile():
    if session.get("logged_in"):
        profile = get_profile(session['user_id'])
        if request.method == 'GET':
            return render_template('profile.html', profile_data={}, profile=profile)
        else:
            profile_data = {
                'UserID': session['user_id'],
                'FirstName': request.form['FirstName'],
                'LastName': request.form['LastName'],
                'Email': request.form['Email'],
                'Bio': request.form['Bio'],
            }
            update_profile(profile_data['UserID'], 
                           profile_data['FirstName'], 
                           profile_data['LastName'], 
                           profile_data['Email'], 
                           profile_data['Bio'])
            return render_template('profile.html', profile_data=profile_data, profile=profile, msg="Your Profile Was Updated!")
    else:
        return redirect(url_for('auth.login_page'))
    
@pages_bp.route("/addpost", methods=['GET', 'POST'])
def addpost():
    if session.get("logged_in"):
        if request.method == 'GET':
            return render_template('addpost.html', post_data={})
        else:
            permalink = request.form['post-link']
            existing_post = find_post(permalink)
            if existing_post:
                error = "This link already exists!"
                return render_template('addpost.html', post_data={}, error=error)
            
            scraper = Scraper()
            scraped_data = scraper.scrape_work(permalink)
            if scraped_data is None:
                error = "Failed to scrape data from the provided link. Please check the URL and try again."
                return render_template('addpost.html', post_data={'Permalink': permalink}, error=error)
            
            post_data = {
                'UserID': session['user_id'],
                'Title': str(scraped_data.get('title', 'No title found')),
                'Author': str(scraped_data.get('author', 'No author found')),
                'Content': str(scraped_data.get('summary', 'No summary found')),
                'Tags': str(scraped_data.get('tags', {})),
                'Permalink': permalink,
                'published_on': date.today(),
            }
            
            try:
                insert_post(post_data)
                return redirect(url_for('pages.home'))
            except Exception as e:
                error = f"Error saving post: {str(e)}"
                return render_template('addpost.html', post_data=post_data, error=error)
    else:
        return redirect(url_for('auth.login_page'))

@pages_bp.route("/editpost", methods=['GET', 'POST'])
def editpost():
    if session.get("logged_in"):
        if request.method == 'GET':
            permalink = request.args.get('post-link')
            if permalink:
                existing_post = find_post(permalink)
                if existing_post:
                    return render_template('editpost.html', post_data=existing_post)
                else:
                    error1 = 'Post not found.'
                    return render_template('editpost.html', post_data={}, error1=error1)
            return render_template('editpost.html', post_data={})
        else:
            if 'load-post' in request.form:
                permalink = request.form['post-link']
                if permalink:
                    print("hi")
                    existing_post = find_post(permalink)
                    if existing_post:
                        return render_template('editpost.html', post_data=existing_post)
                    else:
                        error1 = 'Post not found.'
                        return render_template('editpost.html', post_data={}, error1=error1)
                else:
                    error1 = 'Please enter a post link.'
                    return render_template('editpost.html', post_data={}, error1=error1)
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
                    error1 = 'Post not found.'
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