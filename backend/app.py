import os
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db_connection():
    if os.getenv('DOCKER_ENV', False):  # Check if running in Docker
        client = MongoClient('mongodb://mongodb:27017/')  # Use Docker network hostname
    else:
        client = MongoClient('mongodb://localhost:27017/')  # Localhost for development
    db = client['flask_blog']
    return db


def get_post(post_id):
    db = get_db_connection()
    try:
        post = db.posts.find_one({'_id': ObjectId(post_id)})
    except InvalidId:
        abort(404)  # Return a 404 if the ObjectId is invalid
    if post is None:
        abort(404)  # Return a 404 if the post doesn't exist
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    db = get_db_connection()
    posts = list(db.posts.find())
    return render_template('index.html', posts=posts)


@app.route('/<post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db = get_db_connection()
            db.posts.insert_one({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db = get_db_connection()
            db.posts.update_one({'_id': ObjectId(id)}, {'$set': {'title': title, 'content': content}})
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<id>/delete', methods=['POST'])
def delete(id):
    post = get_post(id)
    db = get_db_connection()
    db.posts.delete_one({'_id': ObjectId(id)})
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
