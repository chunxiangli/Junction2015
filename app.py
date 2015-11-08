import os
import flask
from flask import Flask
from flask import render_template, request

from search import search as search_routes
from find import findNeighbors

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

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    #print(data)
    response = search_routes(data['homeCity'], data['cities'], data['startTime'], data['endTime'])
    # print(type(response))
    print(response)
    return response

@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    #print(data)
    response = findNeighbors(data['homeCity'], data['cities'], data['startTime'], data['endTime'])
    print(type(response))
    print(response)
    return flask.jsonify(response)

@app.route('/results')
def results(name=None):
    return render_template('results.html')

app.debug = True

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
