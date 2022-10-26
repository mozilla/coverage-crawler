# encoding: utf-8
import flask
from flask import render_template

WEBSITE_DOMAIN = 'localhost'
WEBSITE_PORT = 8000
WEBSITE_URL = f'{WEBSITE_DOMAIN}:{WEBSITE_PORT}'
WEBSITE_TITLE = 'coverage-crawler example website'
app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def run_server(debug=False):
    app.run(host=WEBSITE_DOMAIN, port=WEBSITE_PORT, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
