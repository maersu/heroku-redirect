import os

from flask import Flask, request, redirect

app = Flask(__name__)

REDIRECT_TO = os.environ.get('REDIRECT_TO', 'https://example.com')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def all(path):
    return redirect(os.path.join(REDIRECT_TO, path))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
