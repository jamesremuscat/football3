import time
import os.path
from datetime import date
from tntfl.aks import CircularSkillBuffer


class ExclusionsFile(object):

    def __init__(self, fileName):
        self.exclusions = []
        if os.path.exists(fileName):
            f = open(fileName, 'r')
            for line in f.readlines():
                self.exclusions.append(line.strip().lower())

    def contains(self, name):
        return (name in self.exclusions)


exclusions = ExclusionsFile("ladderExclude")


class Streak(object):
    def __init__(self):
        self.count = 0
        self.fromDate = 0
        self.toDate = 0


class Player(object):

    # Number of days inactivity after which players are considered inactive
    DAYS_INACTIVE = 60

    def __init__(self, name):
        self.name = name
        self.elo = 0.0
        self.games = []
        self.withinActive = 0
        self.wins = 0
        self.losses = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.skillBuffer = CircularSkillBuffer(10)
        self.gamesAsRed = 0
        self.gamesPerDay = {}
        self.achievements = {}
        self.excluded = exclusions.contains(name)

    def game(self, game):
        if self.name == game.redPlayer:
            delta = -game.skillChangeToBlue
            opponent = game.bluePlayer
            self.gamesAsRed += 1
            if game.redScore > game.blueScore:
                self.wins += 1
            elif game.redScore < game.blueScore:
                self.losses += 1
            self.goalsFor += game.redScore
            self.goalsAgainst += game.blueScore
        elif self.name == game.bluePlayer:
            delta = game.skillChangeToBlue
            opponent = game.redPlayer
            if game.redScore < game.blueScore:
                self.wins += 1
            elif game.redScore > game.blueScore:
                self.losses += 1
            self.goalsFor += game.blueScore
            self.goalsAgainst += game.redScore
        else:
            return
        self.skillBuffer.put({'oldskill': self.elo, 'skill': self.elo + delta, 'played': opponent})
        self.elo += delta

        gameDate = game.timeAsDatetime().date()
        if gameDate in self.gamesPerDay:
            self.gamesPerDay[gameDate] += 1
        else:
            self.gamesPerDay[gameDate] = 1

        self.games.append(game)
        self.withinActive = game.time + (60 * 60 * 24 * self.DAYS_INACTIVE)

    def getSkillBounds(self):
        highestSkill = {"time": 0, "skill": 0}
        lowestSkill = {"time": 0, "skill": 0}
        elo = 0
        for game in self.games:
            if self.name == game.redPlayer:
                delta = -game.skillChangeToBlue
            else:
                delta = game.skillChangeToBlue
            elo += delta
            if elo > highestSkill["skill"]:
                highestSkill = {"time": game.time, "skill": elo}
            elif elo < lowestSkill["skill"]:
                lowestSkill = {"time": game.time, "skill": elo}
        return {"highest": highestSkill, "lowest": lowestSkill}

    def mostSignificantGame(self):
        mostSignificantGame = None
        for game in self.games:
            if self.name == game.redPlayer:
                delta = -game.skillChangeToBlue
            else:
                delta = game.skillChangeToBlue
            if mostSignificantGame is None or abs(delta) > abs(mostSignificantGame.skillChangeToBlue):
                mostSignificantGame = game
        return mostSignificantGame

    @property
    def gamesToday(self):
        today = date.today()
        return self.gamesOn(today)

    def gamesOn(self, date):
        if date in self.gamesPerDay:
            return self.gamesPerDay[date]
        return 0

    def achieve(self, achievements):
        for achievement in achievements:
            if achievement in self.achievements.keys():
                self.achievements[achievement] += 1
            else:
                self.achievements[achievement] = 1

    def isActive(self, atTime=time.time()):
        #  Using date.* classes is too slow here
        return (self.withinActive > atTime) and (not self.excluded)

    def overrated(self):
        lastSkill = self.skillBuffer.lastSkill()
        if self.skillBuffer.isFull:
            return lastSkill - self.skillBuffer.avg()
        return 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":" + str(self.elo)

    def wonGame(self, game):
        return (game.redPlayer == self.name and game.redScore > game.blueScore) or (game.bluePlayer == self.name and game.blueScore > game.redScore)

    def lostGame(self, game):
        return (game.redPlayer == self.name and game.redScore < game.blueScore) or (game.bluePlayer == self.name and game.blueScore < game.redScore)

    def getStreaks(self):
        winStreak = Streak()

        loseStreak = Streak()

        currentStreak = Streak()

        lastWon = False
        lastLost = False

        for game in self.games:
            wonGame = self.wonGame(game)
            lostGame = self.lostGame(game)

            if (wonGame != lastWon) or (lostGame != lastLost):
                # end of streak
                if lastWon:
                    if currentStreak.count > winStreak.count:
                        winStreak = currentStreak
                if lastLost:
                    if currentStreak.count > loseStreak.count:
                        loseStreak = currentStreak
                currentStreak = Streak()
                currentStreak.fromDate = game.time
                currentStreak.toDate = game.time if (wonGame or lostGame) else 0
                currentStreak.count = 1 if (wonGame or lostGame) else 0

            if (wonGame and lastWon) or (lostGame and lastLost):
                currentStreak.toDate = game.time
                currentStreak.count += 1

            lastWon = wonGame
            lastLost = lostGame

        currentStreakType = "wins" if lastWon else "losses" if lastLost else "(last game was a draw)"

        return {'win': winStreak, 'lose': loseStreak, 'current': currentStreak, 'currentType': currentStreakType}



class PerPlayerStat(object):
    games = 0
    goalsFor = 0
    goalsAgainst = 0
    skillChange = 0
    wins = 0
    losses = 0
    draws = 0

    def __init__(self, opponent):
        self.opponent = opponent

    def append(self, goalsFor, goalsAgainst, skillChange):
        self.games += 1
        self.goalsFor += goalsFor
        self.goalsAgainst += goalsAgainst
        self.skillChange += skillChange
        if goalsFor > goalsAgainst:
            self.wins += 1
        elif goalsFor < goalsAgainst:
            self.losses += 1
        else:
            self.draws += 1
