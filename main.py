
# from flask import *

# app = Flask(__name__,template_folder=("templates"))


# @app.route('/')
# def home():
#     return render_template("pro.html")


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
# db_path = os.path.join(BASE_DIR, 'data.db')

conn = sqlite3.connect('data.db')

def init_db():
    if not os.path.exists('data.db'):
        conn = sqlite3.connect('data.db')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.close()

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
