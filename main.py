import os
import sys
import time
import eyed3
import getpass
import requests
import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from song import Song

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

if len(sys.argv) < 2:
    IN = "music_src.csv"
else:
    IN = sys.argv[1]
OUT = "output.csv"
songs = []


def download_with_metadata():
    pwd = os.getcwd()
    dir = "/Users/" + getpass.getuser() + "/Desktop/mp3_downloads/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    for song in songs:
        if song.youtubeLink is not None:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song.youtubeLink, download=True)
                filename = ydl.prepare_filename(info)
                if filename.endswith(".webm"):
                    filename = filename[:-5] + ".mp3"
                else:
                    filename = filename[:-4] + ".mp3"
            song.filePath = dir + filename

            # Append all metadata fields and album art to the track
            if song.filePath is not None:
                mp3 = eyed3.load(song.filePath)
                if (mp3.tag is None):
                    mp3.initTag()
                mp3.tag.title = song.title
                mp3.tag.artist = song.artist
                mp3.tag.album_artist = song.artist
                mp3.tag.album = song.album
                mp3.tag.genre = song.genre
                if song.albumArtLink is not None:
                    mp3.tag.images.set(3, requests.get(song.albumArtLink).content, 'image/jpeg')
                mp3.tag.save(version=(2,3,0))

    os.chdir(pwd)

def main():
    # This opens the CSV export of your Shazam library
    inputFile = open(IN, "r")
    for line in inputFile:    
        song = Song(line)
        songs.append(song)
    inputFile.close()

    # Webscraping of each song's Shazam page to gather all necessary info and related links
    driver = webdriver.Chrome(options=options)
    for song in songs:
        driver.get(song.shazamLink)
        time.sleep(2)
        html = driver.page_source
        song._set_shazam_attrs(html)
        print(song)
    driver.quit()

    # Download each track from its Youtube link and add all meta fields/album art
    download_with_metadata()

    # A reduced CSV with all the pertinent metadata we care about for tracking purposes
    outputFile = open(OUT, "w")
    for song in songs:
        outputFile.write(f"{song.id},{song.artist},{song.title},{song.album},{song.genre},{song.albumArtLink},{song.youtubeLink}\n")
    outputFile.close()

if __name__ == "__main__":
	main()