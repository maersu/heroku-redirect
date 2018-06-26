# Redirect Legacy

Just a simple app that catches everything and redirects it to `$REDIRECT_TO`

Example:

http://blog.myolddomain.com/part1/part2 -> https://www.mynewdomain.com/part1/part2


## Development:

install

```
pipenv install --python 3.6
```

Run

```
export REDIRECT_TO=https://example.com && export INJECT_SUBDOMAINS='blog, info' pipenv run python app.py

```