class Song:
    def __init__(self, line):
        fields = line.split(",")
        self.id = fields[0]
        self.date = fields[1]
        self.title = fields[2].replace("\"", "")
        self.artist = fields[3].replace("\"", "")
        self.shazamLink = fields[4]
        self.trackId = fields[5]

        self.genre = None
        self.album = None
        self.youtubeLink = None
        self.albumArt = None

    def __repr__(self):
        toString = self.id + ".\t" + self.artist + "\t" + self.title + "\n"
        return toString 
        