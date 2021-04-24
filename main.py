from song import Song
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

# Vars
CSV = "music_src.csv"
songs = []

def main():

    file = open(CSV, "r")

    for line in file:    
        song = Song(line)
        songs.append(song)

    file.close()

    driver = webdriver.Chrome(options=options)

    for song in songs:
        
        driver.get(song.shazamLink)
        time.sleep(4)
        html = driver.page_source
        song._get_shazam_attrs(html)

        print(song)

    driver.quit()


if __name__ == '__main__':
	main()