import os
import sys
import time
import eyed3
import getpass
import requests
import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import dropwhile
from selenium.webdriver.chrome.options import Options

from song import Song

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

eyed3.log.setLevel("ERROR")

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

IN = "music_src.csv"
OUT = "output.csv"
if len(sys.argv) == 2:
    IN = sys.argv[1]


def download_with_metadata(songs: list):
    pwd = os.getcwd()
    dir = "/Users/" + getpass.getuser() + "/Desktop/mp3_downloads/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)

    for song in songs:
        if song.youtubeLink is not None:
            print(f"\nDOWNLOADING: {song}")
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
                if mp3.tag is None:
                    mp3.initTag()
                mp3.tag.title = song.title
                mp3.tag.artist = song.artist
                mp3.tag.album_artist = song.artist
                mp3.tag.album = song.album
                mp3.tag.genre = song.genre
                if song.albumArtLink is not None:
                    mp3.tag.images.set(
                        3, requests.get(song.albumArtLink).content, "image/jpeg"
                    )
                mp3.tag.save(version=(2, 3, 0))
        else:
            print(f"SKIPPING: {song}")

    os.chdir(pwd)


def is_header(line):
    return line.startswith("Shazam Library") or line.startswith("Index,TagTime")


def main():
    ts = time.time()
    songs = []

    # Open the Shazam library CSV (skipping the header lines) and create a Song for each line
    with open(IN, "r") as f:
        for line in dropwhile(is_header, f):
            song = Song(line)
            songs.append(song)
    f.close()

    # Webscraping of each song's Shazam page to gather all necessary info and related links
    print("\nGathering information about songs...\n\n")
    driver = webdriver.Chrome(options=options)
    for song in songs:
        driver.get(song.shazamLink)
        time.sleep(3)
        html = driver.page_source
        song._set_shazam_attrs(html)
    driver.quit()

    # Download each track from its Youtube link and add all meta fields/album art
    download_with_metadata(songs)

    # A reduced CSV with all the pertinent metadata we care about for tracking purposes
    outputFile = open(OUT, "w")
    for song in songs:
        outputFile.write(
            f"{song.id},{song.artist},{song.title},{song.album},{song.genre},{song.albumArtLink},{song.youtubeLink}\n"
        )
    outputFile.close()

    print(f"FINISHED in {time.time() - ts} seconds!")


if __name__ == "__main__":
    main()
