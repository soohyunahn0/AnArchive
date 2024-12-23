from connection import get_db
from fic import blog_posts
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
from datetime import date

def create_post_table():
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''
    create table if not exists BlogPosts (
        "PostId" integer primary key autoincrement,
        "UserID" integer,
        "Title" Text,
        "Author" Text,
        "Content" Text,
        "Permalink" Text,
        "Tags" Text,
        "published_on" date
    )
    ''')
    posts = get_posts()
    if len(posts) == 0:
        for post in blog_posts:
            insert_post(post)

def insert_post(post):
    connection = get_db()
    sql = connection.cursor()
    post_items = post.values()
    sql.execute('''
        Insert into BlogPosts (UserID, Title, Author, Content, Permalink, Tags, published_on)
        values(?, ?, ?, ?, ? ,?, ?)
    ''', list(post_items))
    connection.commit()

def update_post(post):
    connection = get_db()
    sql = connection.cursor()
    post_items = post.values()
    sql.execute('''
        Update BlogPosts
        set UserID=?, Title=?, Author=?, Content=?, Permalink=?, Tags=?
        where PostId=?
    ''', list(post_items))
    connection.commit()

def get_posts():
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts order by UserID desc''')
    saved_posts = data.fetchall()
    return saved_posts

def get_user_posts(user_id):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts where UserID=?''', [user_id])
    saved_posts = data.fetchall()
    return saved_posts

def count_posts():
    connection = get_db()
    sql = connection.cursor()
    count_query = sql.execute('''select count(PostId) from BlogPosts''')
    count = count_query.fetchone()
    return count[0]

def paginated_posts(current_page, per_page):
    connection = get_db()
    sql = connection.cursor()
    
    prev_page = current_page - 1
    offset = prev_page * per_page

    data = sql.execute('''select * from BlogPosts order by PostId desc
                          limit ? offset ?''', [per_page, offset])

    saved_posts = data.fetchall()
    return saved_posts

def find_post(permalink):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts where permalink = ?''', [permalink])
    post = data.fetchone()
    return post

def find_post1(PostId):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts where PostId = ?''', [PostId])
    post = data.fetchone()
    return post

def find_keyword(keyword):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts where Title = ?
                            or * from BlogPosts where Author = ?
                            or * from BlogPosts where Content = ?
                            or * from BlogPosts where Tags = ?''', [keyword])
    posts = data.fetchall()
    return posts

def random_post():
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from BlogPosts order by random() Limit 1''')
    post = data.fetchone()
    return post

def delete_post(post_id):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('delete from BlogPosts where PostId=?', [post_id])
    print(data)
    connection.commit()