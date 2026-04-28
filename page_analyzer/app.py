import os

import psycopg2
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .parser import check_data
from .url_repository import UrlRepository
from .url_validator import normalize_url, validate_url

load_dotenv()

BASE_DIR = os.path.dirname(__file__)        # если файл в page_analyzer — ok
template_dir = os.path.join(BASE_DIR, 'templates')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
print('DB=', DATABASE_URL)


@app.route('/')
def index():
    return flask.render_template(
        'index.html',
    )


@app.route('/urls')
def urls_get():
    conn = psycopg2.connect(DATABASE_URL)
    repo = UrlRepository(conn)
    urls = repo.get_content() or []
    return flask.render_template(
        'urls.html',
         urls=urls
    )


@app.route('/urls/<int:id>')
def url_show(id):
    conn = psycopg2.connect(DATABASE_URL)
    repo = UrlRepository(conn)
    messages = flask.get_flashed_messages(with_categories=True)
    url = repo.find(id)
    checked_urls = repo.find_checks(id)
    return flask.render_template(
        'show.html',
        url=url,
        checked_urls=checked_urls,
        messages=messages
    )


@app.route('/urls', methods=['POST'])
def url_post():
    conn = psycopg2.connect(DATABASE_URL)
    repo = UrlRepository(conn)
    url = flask.request.form.to_dict()
    errors = validate_url(url['url'])
    
    if errors:
        flask.flash(errors["url"], 'error')
        return flask.render_template(
            'index.html',
        ), 422

    normalized_url = normalize_url(url['url'])
    url_info = repo.find_by_name(normalized_url)
    if url_info is not None:
        flask.flash('Страница уже существует', 'error')
        return flask.redirect(flask.url_for('url_show', id=url_info), code=302)

    url_id = repo.save(normalized_url)
    flask.flash('Страница успешно добавлена', 'success')
    return flask.redirect(flask.url_for('url_show', id=url_id), code=302)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_check(id):
    conn = psycopg2.connect(DATABASE_URL)
    repo = UrlRepository(conn)
    url_info = repo.find(id)
    print("id=", id)
    print("url_info=", url_info)
    try:
        
        response = requests.get(url_info.get('name'))
    
        response.raise_for_status()
    
    except requests.RequestException:
        flask.flash('Произошла ошибка при проверке', 'error')
        return flask.redirect(flask.url_for('url_show', id=id), code=302)

    status = response.status_code
    data = check_data(response)
    data['status'] = status
    repo.get_checked(data, url_info)
    flask.flash('Страница успешно проверена', 'success')
    return flask.redirect(flask.url_for('url_show', id=id), code=302)


if __name__ == '__main__':
    app.run(debug=True)
