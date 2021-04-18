# shazam-mp3
Automated workflow to download Shazam library as MP3 files

URL: https://www.shazam.com/track/<TrackKey>


WHEN YOUTUBE PRESENT:

X-Path: 		//*[@id="yt-videocontainer"]
Full X-Path: 	/html/body/div[4]/div/main/div/div[3]/div[1]/div[2]/article/div/div
JS Path:		document.querySelector("#yt-videocontainer")
Selector: 		#yt-videocontainer

data-href="<youtubeLink>"
data-shz-dynamic-beacon="providername=youtube"


Artist - Title div
Full X-Path:    /html/body/div[4]/div/main/div/div[3]/div[1]/div[2]/article/div/div/div[2]/div
JS Path:        document.querySelector("#yt-videocontainer > div.info > div")



