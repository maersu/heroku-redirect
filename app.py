import os
from urllib.parse import urlparse, urlunparse
from flask import Flask, request, redirect

app = Flask(__name__)

INJECT_SUBDOMAINS = [s.strip() for s in os.environ.get('INJECT_SUBDOMAINS', '').split(',') if s.strip()]

REDIRECT_TO = os.environ.get('REDIRECT_TO', 'https://example.com')
redirect_parts = urlparse(REDIRECT_TO)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def all(path):
    parts = urlparse(request.url)
    parts = parts._replace(scheme=redirect_parts.scheme)

    if parts.netloc.split('.')[0] in INJECT_SUBDOMAINS:
        parts = parts._replace(path='/{}{}'.format(parts.netloc.split('.')[0], parts.path))

    parts = parts._replace(netloc=redirect_parts.netloc)

    return redirect(urlunparse(parts))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
