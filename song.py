from bs4 import BeautifulSoup

class Song:
    def __init__(self, line):

        fields = line.split(",")
        self.id = fields[0]
        self.date = fields[1]
        self.title = fields[2].replace("\"", "")
        self.artist = fields[3].replace("\"", "")
        self.trackId = fields[5]

        self.genre = None
        self.album = None
        self.albumArt = None

        self.shazamLink = fields[4]
        self.youtubeLink = None
        self.albumArtLink = None


    def __repr__(self):
        toString = self.id + ".\t" + self.artist + " - " + self.title + " (" + self.album + ")\nShazam:\t" + self.shazamLink + "\nYT:\t" + self.youtubeLink + "\nAlbum:\t" + self.albumArtLink + "\n\n"
        return toString 
        
    def _get_shazam_attrs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self._get_youtube_link(soup, html)
        self._get_album_art_link(soup, html)
        self._get_genre(soup, html)
        self._get_album(soup, html)

    def _get_youtube_link(self, soup, html):
        self.youtubeLink = soup.find('div', {'class': 'video-container'})['data-href']

    def _get_album_art_link(self, soup, html):
        self.albumArtLink = soup.find('img')['src'].replace('400x400', '1000x1000')

    def _get_genre(self, soup, html):
        self.genre = soup.find('h3', {'class': 'genre'}).text     

    def _get_album(self, soup, html):
        self.album = soup.find('div', {'class': 'playlist-title ellip'}).text   
