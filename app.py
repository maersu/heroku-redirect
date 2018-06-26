import os, re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from flask import Flask, request, redirect

app = Flask(__name__)

INJECT_SUBDOMAINS = [s.strip() for s in os.environ.get('INJECT_SUBDOMAINS', '').split(',') if s.strip()]

REDIRECT_TO = os.environ.get('REDIRECT_TO', 'https://example.com')

CONVERT_PAGE_QUERY = os.environ.get('CONVERT_PAGE_QUERY', '')
redirect_parts = urlparse(REDIRECT_TO)

page_regex = re.compile(".*\/page\/(?P<id>\d+)\/$")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def all(path):
    parts = urlparse(request.url)
    parts = parts._replace(scheme=redirect_parts.scheme)

    if parts.netloc.split('.')[0] in INJECT_SUBDOMAINS:
        parts = parts._replace(path='/{}{}'.format(parts.netloc.split('.')[0], parts.path))

    if CONVERT_PAGE_QUERY:
        print('CONVERT_PAGE_QUERY', parts.path)
        m = page_regex.match(parts.path)
        if m:
            print(m.group(1))
            parts = parts._replace(path=parts.path.split('/page/')[0])
            query_dict = {k: v[0] for k, v in parse_qs(parts.query).items()}
            query_dict['page'] = m.group(1)

            print(query_dict)
            parts = parts._replace(query=urlencode(query_dict))

    return redirect(urlunparse(parts._replace(netloc=redirect_parts.netloc)))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
