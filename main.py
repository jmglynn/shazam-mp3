from song import Song
import requests

# Vars
CSV = "sample.csv"
songs = []
song = None


def main():
	# Open a webpage
    # os.system("open \"\" https://www.shazam.com/myshazam")
	# pyautogui.moveTo(1420, 270)
	# time.sleep(2.5)
	# for i in range(0, 17):
	# 	fullscreen = pyautogui.screenshot('/Users/' + getpass.getuser() + '/Downloads/fullscreen.png')
		
	# 	song_separate('/Users/' + getpass.getuser() + '/Downloads/fullscreen.png', firstRun=first_run)

    file = open(CSV, "r")

    for line in file:    
        song = Song(line)
        songs.append(song)

        # print("{0} - {1}".format(song.artist, song.title))
    print(songs)

    file.close()

    # for x in range(len(songs)):
    #     print(songs[x].title)
    #     x + 1


if __name__ == '__main__':
	main()