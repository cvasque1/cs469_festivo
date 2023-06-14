from concurrent.futures import thread
import os, sys
from time import time
from flask import Flask, session, request, redirect, render_template, url_for, flash, send_from_directory, jsonify
from flask_session import Session
from datetime import timedelta
from dotenv import load_dotenv
import spotipy
import uuid
import festivo_features as festivo
import threading

load_dotenv()

app = Flask(__name__, static_folder='../festivo-mockup/build')

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


def createSpotifyOAuth(cache_handler):
    return spotipy.oauth2.SpotifyOAuth(
        scope='user-top-read playlist-modify-public',
        cache_handler=cache_handler,
        show_dialog=True,
        client_id='YOUR CLIENT ID HERE', 
        client_secret='YOUR CLIENT SECRET HERE',
        redirect_uri='<YOUR PAGE URL HERE>/authorize'
    )


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_public(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    elif path.endswith(".js"):  # Explicitly handle JavaScript files
        return send_from_directory(os.path.join(app.static_folder, 'static/js'), path)
    elif path.endswith(".css"):  # Explicitly handle CSS files
        return send_from_directory(os.path.join(app.static_folder, 'static/css'), path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    

@app.route('/app/<path:path>')
def serve_private(path):
    if 'uuid' not in session:
        return redirect('/')
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    elif path.endswith(".js"):  # Explicitly handle JavaScript files
        return send_from_directory(os.path.join(app.static_folder, 'static/js'), path)
    elif path.endswith(".css"):  # Explicitly handle CSS files
        return send_from_directory(os.path.join(app.static_folder, 'static/css'), path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/get_auth_url')
def get_auth_url():
    if 'uuid' not in session:
        # Create a new UUID for the session if one doesn't exist
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = createSpotifyOAuth(cache_handler)
    
    auth_url = auth_manager.get_authorize_url()
    if 'uuid' in session:
        del session['uuid']
    return jsonify({'auth_url': auth_url})


@app.route('/authorize')
def authorize():
    if 'uuid' not in session:
        # Create a new UUID for the session if one doesn't exist
        session['uuid'] = str(uuid.uuid4())
        
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = createSpotifyOAuth(cache_handler)
    if auth_manager.validate_token(cache_handler.get_cached_token()):
        # If the token is valid, redirect to homepage
        return redirect('/app/home')
    else:
        # If the token isn't valid, get a new one
        try:
            auth_manager.get_access_token(request.args.get("code"))
            return redirect('/app/home')
        except:
            # If there is an error in getting a new token, redirect to landing page
            return redirect('/')



# Obtain the display name of user account
@app.route('/api/user', methods=['GET'])
def get_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = createSpotifyOAuth(cache_handler)
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Get the current user
    display_name = spotify.me()["display_name"]

    return jsonify({'name': display_name})


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return jsonify({'message': 'Sign-out successful'})


# @app.before_request
# def before_request():
#     # Check if the user is authenticated
#     if 'uuid' not in session and request.endpoint not in ['serve', 'authorize', 'sign_out']:
#         # If the user is not authenticated, redirect them to the login page
#         return redirect('/')


@app.route('/api/festivals')
def get_festivals():
    festivals = festivo.get_festivals_from_excel()
    print(jsonify(festivals))
    return jsonify(festivals)


@app.route('/api/recommended-artists/<festival_name>/<festival_year>/<time_range>', methods=["GET"])
def get_recommended_artists(festival_name, festival_year, time_range):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    recommended_artists = festivo.getRecommendedArtists(spotify, time_range, festival_name, festival_year)
    session[time_range] = recommended_artists
    formatted_artists = [{'image':x.image, 'name':x.name, 'compatibility':y, 'url':x.uri} for (x,y) in recommended_artists.items()]
    return jsonify(formatted_artists)


@app.route('/api/create-playlist/<festival_name>/<festival_year>/<time_range>', methods=['GET'])
def create_playlist(festival_name, festival_year, time_range):
    # Get the authenticated Spotify object from the session or any other required authentication process
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = createSpotifyOAuth(cache_handler)
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Perform the necessary steps to create the playlist using festivo.createRecommendedPlaylist
    festivo.createRecommendedPlaylist(spotify, session[time_range], 
                                      festival_name, festival_year, time_range)

    # Return a JSON response indicating the success
    return jsonify({'message': 'Playlist created successfully'})



'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=8080, debug=True)
    # app.run(threaded=True, port=int(os.environ.get("PORT",
    #                                                os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))