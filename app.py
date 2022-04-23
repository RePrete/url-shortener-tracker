import configparser
from random import choice
import string
import os
import requests

from flask import Flask, request, redirect, jsonify, render_template
from flask_caching import Cache
 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

configparser.ConfigParser()

cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': os.environ.get('TTL', 60 * 60 * 24 * 7),
    'CACHE_KEY_PREFIX': 'ust_',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
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
    ip = request.headers.get('X-Forwarded-For')
    location = requests.get("https://geolocation-db.com/json/" + ip + "&position=true").json()
    store_location(url_id, location)
    return redirect(cache.get(url_id), code=302)

@app.route("/<url_id>/locations")
def getLocations(url_id: string):
    locations = cache.get('location_' + url_id)
    return jsonify(locations)


def store_location(url_id, location):
    existing_locations = cache.get('location_' + url_id)
    if existing_locations:
        existing_locations.append(location)
        locations = existing_locations
    else:
        locations = [location]
    cache.set('location_' + url_id, locations)

@app.route("/test")
def test():
    return render_template('preview.html')

if __name__ == "__main__":
        app.run()