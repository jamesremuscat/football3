<%! title = "Stats | " %>
<%! base = "../" %>
<%!
from collections import OrderedDict
from datetime import date, datetime
from tntfl.game import Game
from tntfl.player import Player %>
<%inherit file="html.mako" />
<% msgs = sorted([g for g in ladder.games if not g.isDeleted()], key=lambda x: abs(x.skillChangeToBlue), reverse=True) %>
<%

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    return int(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

redGoals = 0
blueGoals = 0
for game in ladder.games:
    redGoals += game.redScore
    blueGoals += game.blueScore

activePlayers = 0
for player in ladder.players.values():
    if player.isActive():
      activePlayers += 1

skillBounds = ladder.getSkillBounds()
%>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Stats</h2>
        </div>
        <div class="panel-body">
          <dl class="dl-horizontal">
            <dt>Total games</dt>
            <dd>${len(ladder.games)}</dd>
            <dt>Total goals by red</dt>
            <dd>${redGoals}</dd>
            <dt>Total goals by blue</dt>
            <dd>${blueGoals}</dd>
            <dt>Total players</dt>
            <dd>${len(ladder.players)}</dd>
            <dt>Active players</dt>
            <dd>${activePlayers} (${"{:.2%}".format(float(activePlayers) / len(ladder.players))})</dd>
          </dl>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Records</h2>
        </div>
        <div class="panel-body">
          <dl class="dl-horizontal">
            <dt>Highest ever skill</dt>
            <dd><b>${"{:.3f}".format(skillBounds['highest']['skill'])}</b> (<a href="${self.attr.base}player/${skillBounds['highest']['player'].name}">${skillBounds['highest']['player'].name}</a>, ${self.blocks.render("gameLink", time=skillBounds['highest']['time'], base=self.attr.base)})</dd>
            <dt>Lowest ever skill</dt>
            <dd><b>${"{:.3f}".format(skillBounds['lowest']['skill'])}</b> (<a href="${self.attr.base}player/${skillBounds['lowest']['player'].name}">${skillBounds['lowest']['player'].name}</a>, ${self.blocks.render("gameLink", time=skillBounds['lowest']['time'], base=self.attr.base)})</dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Most Significant Games</h2>
        </div>
        <div class="panel-body">
% for game in msgs[0:5]:
    ${self.blocks.render("game", game=game, base=self.attr.base)}
% endfor
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Least Significant Games</h2>
        </div>
        <div class="panel-body">
% for game in msgs[-5:]:
    ${self.blocks.render("game", game=game, base=self.attr.base)}
% endfor
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Games Per Day</h2>
        </div>
        <div class="panel-body">
          <div id="gamesPerDay">&nbsp;</div>
          <script type="text/javascript">
<%

gamesPerDay = OrderedDict()

for game in ladder.games:
    day = datetime.fromtimestamp(game.time).replace(hour=0, minute=0, second=0, microsecond=0)
    if day not in gamesPerDay:
      gamesPerDay[day] = 0
    gamesPerDay[day] += 1

plotData = []

for day, tally in gamesPerDay.iteritems():
    plotData.append([totimestamp(day) * 1000, tally])

%>
          $.plot("#gamesPerDay", [ ${plotData} ], {'legend' : {show: false}, 'xaxis': {mode: 'time'}, grid: {hoverable: true}, colors: ['#0000FF']});
          </script>
        </div>
      </div>
    </div>
  </div>
</div>
