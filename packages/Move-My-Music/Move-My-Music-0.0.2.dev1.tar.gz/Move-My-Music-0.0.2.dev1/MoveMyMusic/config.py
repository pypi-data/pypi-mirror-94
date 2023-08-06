"""
    Default parameters
    Configure parameters for preferred result.
"""


class Default(object):

    # Spotify API
    SP_CLIENT_ID = "61ab58057f9342c0a58c95588e95aaa4"
    SP_CLIENT_SECRET = "535062bd5a3844c7a07e8bf566e153b6"
    SCOPE = "user-library-read user-library-modify playlist-read-private playlist-modify-private"

        # GENERAL
    PLAYLIST = False     # by default gets tracks, set to True if album wanted
    PLAYLIST_L = []     # select which albums e.g ['my playlist1', 'my playlist2'], default None(all)
    ARTISTS = False
    ALBUMS = False
    ALLTRACKS = False
    DATATMP = './dataTemplate.json'
    LOG_PATH = './logs'
    CLEAN_PLATE = True
