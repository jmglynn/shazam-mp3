# SHAZAM-MP3

Automated workflow to download Shazam library as MP3 files complete with the following embedded metadata:
* Artist
* Title
* Album (when available)
* Genre
* Album Art

## INSTALLATION (MacOS)

```
brew install chromedriver
brew install ffmpeg
pip install -r requirements.txt
```

## USAGE
1. Log into https://www.shazam.com/myshazam
2. Click `DOWNLOAD CSV` on the right side (Only supported on desktop, Safari on iOS devices and Chrome on Android devices)
3. Command usage: `python3 main.py [path_to_shazamlibrary.csv]` (path parameter is optional; will default to reading from `music_src.csv` if you want to paste your csv file/specific subset of entries there)
4. An `mp3_downloads` directory will appear on your desktop with all the final files. You can then open them in your desired media player.


## Disclaimers
* Sometimes metadata such as genre, album, or cover art are unavailable. In this case, the genre or album will be set to `None`, and no cover art will be added
* Sometimes no Youtube link is present on the Shazam page, so a query is made to youtube using the artist, title, and "audio" keyword to get an audio-only youtube link. If any errors arise in this process, the song is skipped entirely and not downloaded or processed any further
* Messages are printed to the terminal when genre, album, album art, or the Youtube link cannot be discerned


## Personalization
Obviously you can look through the code and personalize any number of aspects, but some may be of interest are:

### `main.py`
* `IN` - global variable for the default input filepath containing the shazam csv entries to be processed
* `ydl_opts` - customize download quality/codec/etc of the Youtube video (full documentation [here](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#options))
* `OUT` - path to output file you want to create; what exactly is output can be customized at the end of `main()`

### `song.py`
* `get_album_art_link` - customize the size of the cover art (default is 400x400)
    * The code to do this is already there, just uncomment like so: `self.albumArtLink = soup.find('img')['src'].replace('400x400', '1000x1000')` where 1000x1000 is the custom size you want
