import os
import csv
import sys
import time
import eyed3
import getpass
import requests
import threading
import youtube_dl
from queue import Queue
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

IN = sys.argv[1] if len(sys.argv) == 2 else "music_src.csv"
OUT = "output.csv"


def download_with_metadata(song: Song):
    pwd = os.getcwd()
    dir = "/Users/" + getpass.getuser() + "/Desktop/mp3_downloads/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)

    if song.youtubeLink is not None:
        print(f"\nDOWNLOADING: {song}")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song.youtubeLink, download=True)
            filename = ydl.prepare_filename(info)
            if filename.endswith(".webm.part"):
                filename = filename[:-10] + ".mp3"
            elif filename.endswith(".webm"):
                filename = filename[:-5] + ".mp3"
            else:
                filename = filename[:-4] + ".mp3"
        song.filePath = dir + filename

        # Embed all metadata fields and album art to the track
        if song.filePath is not None:
            mp3 = eyed3.load(song.filePath)
            if mp3.tag is None:
                mp3.initTag()
            mp3.tag.title = song.title
            mp3.tag.artist = song.artist
            mp3.tag.album_artist = song.artist
            mp3.tag.album = song.album
            mp3.tag.genre = song.genre
            if song.lyrics is not None:
                mp3.tag.lyrics.set(song.lyrics)
            if song.albumArtLink is not None:
                mp3.tag.images.set(
                    3, requests.get(song.albumArtLink).content, "image/jpeg"
                )
            mp3.tag.save(version=(2, 3, 0))
    else:
        print(f"SKIPPING: {song}")

    os.chdir(pwd)


def youtube_threader(i, q):
    while True:
        song = q.get()
        print(f"{i}: Downloading...")
        try:
            download_with_metadata(song)
        except Exception as e:
            print(f"ERROR: COULDN'T DOWNLOAD {song}\n{e}")
        print(f"{i} Finished!")
        q.task_done()


def main():
    t0 = time.time()
    songs = []
    q = Queue()
    num_threads = 10

    # Open the Shazam library CSV (skipping the header lines) and create a Song for each line
    with open(IN, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            try:
                if len(line) == 6 and type(int(line[0])) == int:
                    song = Song(line)
                    songs.append(song)
            except Exception as e:
                print(f"Error creating song object from CSV line {line}: {e}")
    f.close()

    # Webscraping of each song's Shazam page to gather all necessary info and related links
    print("\nGathering information about songs...\n\n")
    driver = webdriver.Chrome(options=options)
    for i in range(num_threads):
        threading.Thread(
            target=youtube_threader,
            daemon=True,
            args=(
                i,
                q,
            ),
        ).start()

    for song in songs:
        try:
            driver.get(song.shazamLink)
            time.sleep(2)
            html = driver.page_source
            song._set_shazam_attrs(html)
            # Queue each scraped song to start downloading from YT with meta/album art
            q.put(song)
        except Exception as e:
            print(f"ERROR: SKIPPING DOWNLOAD OF {song}\n{e}.")
    q.join()
    driver.quit()

    # A reduced CSV with all the pertinent metadata we care about for tracking purposes
    outputFile = open(OUT, "a")
    for song in songs:
        outputFile.write(
            f"{song.id},{song.artist},{song.title},{song.album},{song.genre},{song.albumArtLink},{song.youtubeLink}\n"
        )
    outputFile.close()

    print(f"FINISHED {len(songs)} songs in {time.time() - t0} seconds!")


if __name__ == "__main__":
    main()
