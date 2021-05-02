# SHAZAM-MP3

Automated workflow to download Shazam library as MP3 files complete with the following embedded metadata:
* Artist
* Title
* Album (when available)
* Genre
* Album Art

## INSTALLATION

```
brew install chromedriver
brew install ffmpeg
pip install -r requirements.txt
```

## USAGE



#### Usage of Youtube-DL on command line
`$ youtube-dl --extract-audio --add-metadata --xattrs --embed-thumbnail --audio-quality 0 --audio-format mp3 URL`
