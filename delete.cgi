#!/usr/bin/env python

import cgi
import os
from tntfl.ladder import TableFootballLadder
from tntfl.web import redirect_302, fail_404, serve_template

form = cgi.FieldStorage()


ladder = TableFootballLadder("ladder.txt")
if "game" in form:
    gameTime = int(form["game"].value)
    if "deleteConfirm" in form and form["deleteConfirm"].value == "true":
        deletedBy = os.environ["REMOTE_USER"] if "REMOTE_USER" in os.environ else "Unknown"
        deleted = ladder.deleteGame(gameTime, deletedBy)
        if deleted:
            redirect_302("./")
        else:
            fail_404()
    else:
        found = False
        for game in ladder.games:
            if game.time == gameTime and not found:
                found = True
                serve_template("deleteGame.mako", game=game)
        if not found:
            fail_404()
            print
else:
    fail_404()
