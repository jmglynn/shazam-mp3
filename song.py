import re
import urllib
import requests
from bs4 import BeautifulSoup


class Song:
    def __init__(self, line):
        self.id = line[0]
        self.date = line[1]
        self.title = line[2]
        self.artist = line[3]
        self.trackId = line[5]

        self.genre = None
        self.album = None
        self.filePath = None
        self.lyrics = None

        self.shazamLink = line[4]
        self.youtubeLink = None
        self.albumArtLink = None

    def __repr__(self):
        toString = (
            f"{self.id}. {self.artist} - {self.title} ({str(self.album)}) / "
            f"{str(self.genre)}\nShazam:\t{str(self.shazamLink)}\nYT:\t"
            f"{str(self.youtubeLink)}\nCover:\t{str(self.albumArtLink)}\n"
        )
        return toString

    def _set_shazam_attrs(self, html):
        soup = BeautifulSoup(html, "html.parser")
        self._get_youtube_link(soup)
        if self.youtubeLink:
            self._get_album_art_link(soup)
            self._get_genre(soup)
            self._get_album(soup)
            self._get_lyrics(soup)

    def _get_youtube_link(self, soup):
        # try:
        #     self.youtubeLink = soup.find("div", {"class": "video-container"})[
        #         "data-href"
        #     ]
        # except Exception:
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

    def _get_album_art_link(self, soup):
        self.albumArtLink = None

        self.albumArtLink = soup.find("img", {"class": "img-on"})["src"].replace(
            "400x400", "800x800"
        )
        # for child in soup.find("div", {"class": "cover-art"}).descendants:
        #     print(child)
        #     if child.name == "img":
        #         self.albumArtLink = child["src"].replace("400x400", "800x800")

        if self.albumArtLink.endswith("/nocoverart.jpg"):
            self.albumArtLink = None
            print(f"NO ALBUM ART FOR {self.id}. {self.artist} - {self.title}")

    def _get_genre(self, soup):
        try:
            self.genre = soup.find("h3", {"class": "genre"}).text
        except Exception:
            print(f"NO GENRE FOR {self.id}. {self.artist} - {self.title}")
            self.genre = None

    def _get_album(self, soup):
        try:
            self.album = soup.find("div", {"class": "playlist-title ellip"}).text
            if self.album.endswith(" - Single"):
                self.album = self.album.replace(" - Single", "")
            if self.album.endswith(" - EP"):
                self.album = self.album.replace(" - EP", "")
        except Exception:
            print(f"NO ALBUM FOR {self.id}. {self.artist} - {self.title}")
            self.album = None

    def _get_lyrics(self, soup):
        try:
            lyrics = soup.find("p", {"class": "lyrics"}).text
            print(lyrics)
            self.lyrics = lyrics
        except Exception:
            print(f"NO LYRICS FOR {self.id}. {self.artist} - {self.title}")
            self.lyrics = None
