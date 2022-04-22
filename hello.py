import configparser
from random import choice
import string
import config
import requests

from flask import Flask, request, redirect
from flask_caching import Cache

app = Flask(__name__)
configparser.ConfigParser()

cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': config.TTL,
    'CACHE_KEY_PREFIX': 'ust_',
    'CACHE_REDIS_URL': config.REDIS_URL,
})

def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

@app.route("/short-url", methods=['POST'])
def create():
    json = request.get_json()
    url = json.get("url")
    short_url_id = generate_short_id(8)
    cache.set(short_url_id, url)
    return {
        "short_url": short_url_id
    }

@app.route("/short-url/<url_id>")
def search(url_id: string):

    return {
        "url": cache.get(url_id)
    }


@app.route("/<url_id>")
def doRedirect(url_id: string):
    response = requests.get("https://geolocation-db.com/json/" + request.remote_addr + "&position=true").json()
    return request.remote_addr
    return redirect(cache.get(url_id), code=302)