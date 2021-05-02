import os
import time
import getpass
import requests
import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from song import Song

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

IN = "music_src.csv"
OUT = "output.csv"
songs = []


def download(songs_list: list):
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
                filename = ydl.prepare_filename(info)[:-5] + ".mp3"
            song.filePath = dir + filename
    os.chdir(pwd)


def main():
    inputFile = open(IN, "r")
    for line in inputFile:    
        song = Song(line)
        songs.append(song)
    inputFile.close()

    driver = webdriver.Chrome(options=options)
    for song in songs:
        driver.get(song.shazamLink)
        time.sleep(5)
        html = driver.page_source
        song._set_shazam_attrs(html)
        print(song)
    driver.quit()

    outputFile = open(OUT, "w")
    for song in songs:
        outputFile.write(f"{song.id},{song.artist},{song.title},{song.album},{song.genre},{song.albumArtLink},{song.youtubeLink}\n")
    outputFile.close()

    download(songs)


if __name__ == "__main__":
	main()