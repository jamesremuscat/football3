from datetime import date, datetime, timedelta

class Game(object):
    skillChangeToBlue = 0
    positionSwap = False
    deletedBy = None
    deletedAt = 0

    def __init__(self, redPlayer, redScore, bluePlayer, blueScore, time):
        self.redPlayer = redPlayer.lower()
        self.redScore = int(redScore)
        self.redPosChange = 0
        self.redPosAfter = -1
        self.bluePlayer = bluePlayer.lower()
        self.blueScore = int(blueScore)
        self.bluePosChange = 0
        self.bluePosAfter = -1
        self.time = int(time)
        self.redAchievements = []
        self.blueAchievements = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(redPlayer=self.redPlayer, bluePlayer=self.bluePlayer, redScore=self.redScore, blueScore=self.blueScore)

    def isDeleted(self):
        return self.deletedAt > 0

    def timeAsDatetime(self):
        return datetime.fromtimestamp(self.time)

    @staticmethod
    def formatTime(inTime):
        time = datetime.fromtimestamp(float(inTime))
        dateStr = time.strftime("%Y-%m-%d %H:%M")

        if date.fromtimestamp(float(inTime)) == date.today():
            dateStr = "%02d:%02d" % (time.hour, time.minute)
        elif date.fromtimestamp(float(inTime)) > (date.today() - timedelta(7)):
            dateStr = "%s %02d:%02d" % (("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[time.weekday()], time.hour, time.minute)

        return dateStr
