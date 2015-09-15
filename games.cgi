#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")
fromTime = int(form["from"].value) if "from" in form else None
toTime = int(form["to"].value) if "to" in form else None
serve_template("games.mako", ladder=ladder, fromTime=fromTime, toTime=toTime)
