import re
import urllib
import requests
from bs4 import BeautifulSoup


class Song:
    def __init__(self, line):

        fields = line.split(",")
        self.id = fields[0]
        self.date = fields[1]
        self.title = fields[2].replace('"', "")
        self.artist = fields[3].replace('"', "")
        self.trackId = fields[5]

        self.genre = None
        self.album = None
        self.albumArt = None
        self.filePath = None

        self.shazamLink = fields[4]
        self.youtubeLink = None
        self.albumArtLink = None

    def __repr__(self):
        toString = (
            f"{self.id}. {self.artist} - {self.title} ({str(self.album)}) / "
            f"{str(self.genre)}\nShazam:\t{str(self.shazamLink)}\nYT:\t"
            f"{str(self.youtubeLink)}\nCover:\t{str(self.albumArtLink)}\n\n"
        )
        return toString

    def _set_shazam_attrs(self, html):
        soup = BeautifulSoup(html, "html.parser")
        self._get_youtube_link(soup, html)
        if self.youtubeLink:
            self._get_album_art_link(soup, html)
            self._get_genre(soup, html)
            self._get_album(soup, html)

    def _get_youtube_link(self, soup, html):
        try:
            self.youtubeLink = soup.find("div", {"class": "video-container"})[
                "data-href"
            ]
        except Exception:
            try:
                query = urllib.parse.quote(f"{self.artist} {self.title} audio")
                response = requests.get(
                    "https://www.youtube.com/results?search_query=" + query
                ).text
                url_key = re.findall(r'\/watch\?v=([^:]+?)"', response)[0]
                self.youtubeLink = "https://www.youtube.com/watch?v=" + url_key
            except Exception:
                print(f"NO YOUTUBE LINK FOR {self.id}. {self.artist} - {self.title}")
                self.youtubeLink = None

    def _get_album_art_link(self, soup, html):
        self.albumArtLink = soup.find("img")["src"]  # .replace('400x400', '1000x1000')
        if (
            self.albumArtLink
            == "/resources/35fb0bf7dff89be0cfc82701544ec0c6f2b6fb75/nocoverart.jpg"
        ):
            self.albumArtLink = None
            print(f"NO ALBUM ART FOR {self.id}. {self.artist} - {self.title}")

    def _get_genre(self, soup, html):
        try:
            self.genre = soup.find("h3", {"class": "genre"}).text
        except Exception:
            print(f"NO GENRE FOR {self.id}. {self.artist} - {self.title}")
            self.genre = None

    def _get_album(self, soup, html):
        try:
            self.album = soup.find("div", {"class": "playlist-title ellip"}).text
            if self.album.endswith(" - Single"):
                self.album = self.album.replace(" - Single", "")
            if self.album.endswith(" - EP"):
                self.album = self.album.replace(" - EP", "")
        except Exception:
            print(f"NO ALBUM FOR {self.id}. {self.artist} - {self.title}")
            self.album = None
