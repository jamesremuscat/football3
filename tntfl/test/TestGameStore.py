import unittest
import os
from tntfl.gameStore import GameStore
from tntfl.game import Game

class TestGameStore(unittest.TestCase):
    def testRead(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            sut = GameStore(filePath)
            result = sut.getGames()
            self.assertEqual(len(result), 1)
            self._assertGame(result[0], game1)
        finally:
            os.remove(filePath)

    def testReadDeleted(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858, "cjm", 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f %s %.0f" % game1)

            sut = GameStore(filePath)
            result = sut.getGames()
            self.assertEqual(len(result), 1)
            self._assertGame(result[0], game1)
        finally:
            os.remove(filePath)

    def testAppend(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            game2 = ("jma", 5, "tmm", 5, 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            sut = GameStore(filePath)
            sut.appendGame(self._createGame(game2))
            result = sut.getGames()
            self.assertEqual(len(result), 2)
            self._assertGame(result[0], game1)
            self._assertGame(result[1], game2)
        finally:
            os.remove(filePath)

    def testDelete(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            sut = GameStore(filePath)
            sut.deleteGame(1445443858, "foo", 1445443861)

            result = sut.getGames()
            self.assertEqual(len(result), 1)
            self._assertGame(result[0], game1 + ("foo", 1445443861))
        finally:
            os.remove(filePath)

    def testGetAppendDelete(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            game2 = ("foo", 2, "bar", 8, 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)
                temp.write("\n%s %s %s %s %.0f" % game2)

            sut = GameStore(filePath)
            result = sut.getGames()
            self.assertEqual(len(result), 2)
            self._assertGame(result[0], game1)
            self._assertGame(result[1], game2)

            game3 = ("bar", 8, "baz", 2, 1445443860)
            game4 = ("bim", 8, "bob", 2, 1445443861)
            sut.appendGame(self._createGame(game3))
            sut.appendGame(self._createGame(game4))

            result = sut.getGames()
            self.assertEqual(len(result), 4)
            self._assertGame(result[0], game1)
            self._assertGame(result[1], game2)
            self._assertGame(result[2], game3)
            self._assertGame(result[3], game4)

            sut.deleteGame(1445443860, "baz", 1445443862)

            result = sut.getGames()
            self.assertEqual(len(result), 4)
            self._assertGame(result[0], game1)
            self._assertGame(result[1], game2)
            self._assertGame(result[2], game3 + ("baz", 1445443862))
            self._assertGame(result[3], game4)
        finally:
            os.remove(filePath)

    def _createGame(self, args):
        game = None
        if len(args) == 5 or len(args) == 7:
            game = Game(args[0], args[1], args[2], args[3], args[4])
            if len(args) == 7:
                game.deletedBy = args[5]
                game.deletedAt = args[6]
        return game

    def _assertGame(self, resultGame, expectedTuple):
        self.assertEqual(resultGame.redPlayer, expectedTuple[0])
        self.assertEqual(resultGame.redScore, expectedTuple[1])
        self.assertEqual(resultGame.bluePlayer, expectedTuple[2])
        self.assertEqual(resultGame.blueScore, expectedTuple[3])
        self.assertEqual(resultGame.time, expectedTuple[4])
        if len(expectedTuple) == 5:
            expectedTuple += (None, 0)
        self.assertEqual(resultGame.deletedBy, expectedTuple[5])
        self.assertEqual(resultGame.deletedAt, expectedTuple[6])
