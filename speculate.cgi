#!/usr/bin/env python

import cgi
from time import time
from tntfl.ladder import TableFootballLadder
from tntfl.game import Game
from tntfl.web import serve_template


form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")

if "previousGames" in form:
    serialisedSpecGames = form["previousGames"].value
else:
    serialisedSpecGames = ""

gameParts = serialisedSpecGames.split(",")

games = []

for i in range(0, len(gameParts) / 4):
    g = Game(gameParts[4 * i], gameParts[4 * i + 1], gameParts[4 * i + 3], gameParts[4 * i + 2], time())
    games.append(g)
    ladder.addGame(g)

if "bluePlayer" in form and "redPlayer" in form:
    redScore = form["redScore"].value if "redScore" in form else 0
    blueScore = form["blueScore"].value if "blueScore" in form else 0
    g = Game(form["redPlayer"].value, redScore, form["bluePlayer"].value, blueScore, time())
    games.append(g)
    ladder.addGame(g)
    serialisedSpecGames += ",{0},{1},{2},{3}".format(form["redPlayer"].value, redScore, blueScore, form["bluePlayer"].value)

if serialisedSpecGames != "" and serialisedSpecGames[0] == ",":
    serialisedSpecGames = serialisedSpecGames[1:]

games.reverse()
serve_template("speculate.mako", ladder=ladder, games=games, serialisedSpecGames=serialisedSpecGames)
