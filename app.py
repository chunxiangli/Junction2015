from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def index(name=None):
    return render_template('index.html')

# @app.route('/search')
# def index(name=None):
#     # search
#     return render_template('index.html')

@app.route('/results')
def results(name=None):
    return render_template('results.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
