# Url shortener -> accepts only 20 users at a time.
# This web app shortens long urls into short 3-lettered strings. Which are easy to remember.
import string
import random
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True :
        rand_letters = random.choices(letters, k=3)
        rand_letters = ''.join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        url_received = request.form['nm']
        # Check if url already exists.
        found_url = None
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            return render_template('index.html', url=found_url.short)
        else :
            # Create short url if not found.
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', url=short_url)
    else:
        return render_template('index.html', url = '')

# @app.route('/shorten', methods=['POST'])
# def shorten():
#     url = request.form['url']
#     return render_template('shorten.html', url=url)

@app.route('/<short_url>')
def original_link(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        # print(long_url.long)
        return redirect(long_url.long)
    else:
        return render_template('404.html', message = "Invalid short url")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/list')
def list():
    urls = Urls.query.all()
    return render_template('list.html', urls=urls)

@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html', message = "Invalid route (Page not Found !)")

if __name__ == '__main__' :
    app.run(debug=True, port=7000)