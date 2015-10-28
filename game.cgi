#!/usr/bin/env python

import cgi
from time import time
from tntfl.ladder import TableFootballLadder
from tntfl.game import Game
from tntfl.web import redirect_302, fail_404, serve_template

form = cgi.FieldStorage()

if "method" in form:
    ladder = TableFootballLadder("ladder.txt")
    if form["method"].value == "add":
        if "bluePlayer" in form and "redPlayer" in form:
            redScore = form["redScore"].value if "redScore" in form else 0
            blueScore = form["blueScore"].value if "blueScore" in form else 0
            game = ladder.addAndWriteGame(form["redPlayer"].value, redScore, form["bluePlayer"].value, blueScore)
            if "view" in form and form["view"].value == "json":
                serve_template("wrappedGame.mako", game=game)
            else:
                redirect_302("../%.0f" % game.time)
    elif form["method"].value == "view" and "game" in form:
        gameTime = int(form["game"].value)
        found = False
        for game in ladder.games:
            if game.time == gameTime and not found:
                serve_template("wrappedGame.mako", game=game)
                found = True
        if not found:
            fail_404()
            print
