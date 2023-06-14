import spotipy
import pandas as pd
import festivo_classes as sc

from festivo_classes import Artist
from collections import defaultdict
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


def userAuthentication():
    """Authenticates user

    Returns
    -------
    sp : class Spotify
    Spotify API Client obj
    """
    load_dotenv()
    scope = "user-top-read playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return sp


def getRecommendedArtists(sp, timeRange, festival_name, festival_year):
    top_artists, related_artists = getTopAndRelatedArtists(sp, timeRange)
    festival_artists = readCSVFile(festival_name, festival_year)
    recommended_artists = generateRecommendedArtists(sp, top_artists, related_artists, festival_artists, timeRange)
    
    return recommended_artists


def getTopAndRelatedArtists(sp, timeRange):
    """Call to access users top and related artists based on user specififed range

    Parameters 
    ----------
    sp : class Spotify
        Spotify API Client obj
    
    Returns
    -------
    top_artists : set
        set of users top artists
    related_artists : dic
        dic of related artists based on users top artists
    """
    if timeRange == 'genres':
        timeRange = 'long_term'
    top_artists_json = sp.current_user_top_artists(time_range=timeRange, limit=50)
    top_artists, related_artists = accessTopandRelatedArtists(sp, top_artists_json)

    return top_artists, related_artists


def accessTopandRelatedArtists(sp, top_artists_json):
    """gets users top artists and related artist from Spotify API

    Parameters
    ----------
    sp : class Spotify
        Spotify API Client obj
    top_artists_json : dic
        json variable containing users top artists information from Spotify API 

    Returns
    -------
    top_artists : list
        list of users top artists
    rel_artists : dic
        dic of related artists based on users top artists
    """
    top_artists = []
    rel_artists = {}

    for i, item in enumerate(top_artists_json['items']):
        top_artist = Artist(name=item['name'], _id=item['id'], genres=item['genres'], image=item['images'][0]['url'], uri=item['uri'])
        top_artists.append(top_artist)
        related_artists = sp.artist_related_artists(top_artist._id)['artists']
        for j,rel_item in enumerate(related_artists):
            rel_artist = Artist(name=rel_item['name'], _id=rel_item['id'], genres=rel_item['genres'], image=rel_item['images'][0]['url'], uri=rel_item['uri'])
            if rel_artist in rel_artists:
                rel_artists[rel_artist] += 1
            else:
                rel_artists[rel_artist] = 1

            if i >= 40 and j >= 3:
                break
            elif i >= 30 and j >= 7:
                break
            elif i >= 20 and j >= 11:
                break
            elif i >= 10 and j >= 15:
                break
            else:
                continue

    return top_artists, rel_artists


def getArtistGenres(sp, artist_name):
    """Fetches the genres of an artist from the Spotify API

    Parameters
    ----------
    sp : spotipy.Spotify
        Spotify API client
    artist_name : str
        Name of the artist

    Returns
    -------
    genres : list of str
        List of the artist's genres
    """
    # Search for the artist
    results = sp.search(q='artist:' + str(artist_name), type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        # If the artist was found, return their genres
        return items[0]['genres']
    else:
        # If the artist was not found, return an empty list
        return []



def get_festivals_from_excel():
    xls = pd.ExcelFile('static/festivo_festivals.xlsx')
    festivals = []
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        image = df.columns[0]
        years = df.columns[1:].tolist()
        for year in years:
            artists = df[year].dropna().tolist()
            festivals.append({
                'name': sheet_name,
                'year': int(year),
                'imageURL': f'../image/{image}',
                'artists': artists
            })

    return festivals


def readCSVFile(festival, year):
    """reads in csv file of artists

    Returns
    -------
    coachella_artists : list
        list of coachella artists
    """
    xls = pd.ExcelFile('static/festivo_festivals.xlsx')
    df = xls.parse(festival)
    festival_artists = df[int(year)].dropna().tolist()

    return festival_artists


def generateRecommendedArtists(sp, top_artists, related_artists, festival_artists, timeRange):
    """Generates recommended artists based on user's top artists and the festival artists

    Parameters
    ----------
    top_artists : set(type(Class Artist))
        set containing users top artists
    related_artists : dic(type(Class Artist): int)
        dic containing artists related to users top artists, along with their match index

    Returns
    -------
    recommended_artists : dic
        a dic of Class Artists and their match index
    """
    recommended_artists = {}    
    if timeRange == "genres":
        top_genres = getTopGenres(top_artists)
        for artist in festival_artists:
            results = sp.search(q='artist:' + str(artist), type='artist')
            if results['artists']['items']:
                art = results['artists']['items'][0]
                artist_genres = set(art['genres'])
                genre_matching_score = len(top_genres & artist_genres)
                if genre_matching_score > 1:
                    rec = Artist(name=art['name'], _id=art['id'], genres=art['genres'], image=art['images'][0]['url'], uri=art['uri'])
                    recommended_artists[rec] = genre_matching_score
    else:
        related_artists_and_index = getArtistAndMatchIndex(related_artists)
        top_artists_dic = getPopularArtists(top_artists)
        for artist in festival_artists:
            if artist in getArtistNames(top_artists):
                recommended_artists[top_artists_dic[artist]] = 200
            elif artist in getArtistNames(related_artists):
                recommended_artists[related_artists_and_index[artist][0]] = 100 + related_artists_and_index[artist][1]
            
    sorted_recommendations = sorted(recommended_artists.items(), key=lambda item: item[1], reverse=True)
    limited_recommendations = dict(sorted_recommendations[:(len(festival_artists)//4)])

    return limited_recommendations


def getTopGenres(top_artists):
    top_genres = set()
    for artist in top_artists:
        top_genres.update(artist.genres)
    return top_genres


def getPopularArtists(artists):
    artist_dic = {}
    for artist in artists:
        artist_dic[artist.name] = artist
    return artist_dic


def getArtistAndMatchIndex(artists):
    artist_dic = {}
    for artist, index in artists.items():
        artist_dic[artist.name] = [artist, index]
    return artist_dic


def getArtistNames(artists):
    artist_names = []
    for artist in artists:
        artist_names.append(artist.name)
    return artist_names


def getRecommendedTopTracks(sp, recommended_artists):
    top_tracks = []
    for artist in recommended_artists.keys():
        top_tracks_json = sp.artist_top_tracks(artist._id)
        tracks = top_tracks_json['tracks']
        for i in range(len(tracks) - 5):
            track = sc.Track(name=tracks[i]['name'], _id=tracks[i]['id'])
            top_tracks.append(track)
    return top_tracks


def createPlaylist(sp, pName, pDesc):
    user_id = sp.me()['id']
    new_playlist = sp.user_playlist_create(user=user_id, name=pName, description=pDesc)
    playlist = sc.Playlist(name=new_playlist['name'], _id=new_playlist['id'])
    return playlist


def chunks(tracks, n):
    n = max(1, n)
    return (tracks[i:i+n] for i in range(0, len(tracks), n))


def getTrackIds(recc_top_tracks):
    track_ids = []
    for track in recc_top_tracks:
        track_ids.append(track._id)
    track_ids_chunks = chunks(track_ids, 10)
    return track_ids_chunks


def addTracksToPlaylist(sp, playlist, recc_top_tracks):
    track_ids_chunks = getTrackIds(recc_top_tracks)
    for tracks in track_ids_chunks:
        sp.playlist_add_items(playlist._id, tracks)


def createRecommendedPlaylist(sp, recommended_artists, festival, year, term):
    recc_top_tracks = getRecommendedTopTracks(sp, recommended_artists) # list/set/dic of object Track
    # promptFinished("getting top recommended tracks")
    timeRange = {
        "long_term": "Last Month",
        "medium_term": "Last 6 Months",
        "long_term": "All Time"
    }
    pName = f"Festivo - {festival} {year} Reccommended Artists - {timeRange[term]}"
    pDesc = "Your recommended artists for Coachella 2022 generated by Festify!\n\nThis isn't all-inclusive but its a good place to start. :)"
    playlist = createPlaylist(sp, pName, pDesc) # object Playlist
    addTracksToPlaylist(sp, playlist, recc_top_tracks)
    



