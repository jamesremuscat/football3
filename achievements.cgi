#!/usr/bin/env python

from tntfl.achievements import Achievement
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template
from collections import OrderedDict


ladder = TableFootballLadder("ladder.txt")
achievements = {}
for ach in Achievement.achievements:
    achievements[ach.__class__] = 0

for player in ladder.getPlayers():
    for name, amount in player.achievements.items():
        achievements[name] += amount

serve_template("achievements.mako", ladder=ladder, achievements=OrderedDict(sorted(achievements.iteritems(), reverse=True, key=lambda t: t[1])))
