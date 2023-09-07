from flask import Flask, url_for, render_template, flash, request, url_for, redirect
from markupsafe import escape, Markup
import os
from distutils.log import debug
from fileinput import filename


app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'



@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'



@app.route('/fileupload/', methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/fileupload/', methods=['POST'])
def upload_submit():
    f = request.files['file']
    f.filename = './uploads/test.txt'
    f.save(f.filename) 
    return "File Subbmited"

# Debug
with app.test_request_context():
    print(url_for('index'))
    print(url_for('profile', username='John Doe'))
    url_for('static', filename='style.css')