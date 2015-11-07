from flask import Flask
from flask import render_template

app = Flask(__name__)

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
    app.run(host='0.0.0.0')
