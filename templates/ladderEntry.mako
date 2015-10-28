<%
import re
from datetime import datetime
from tntfl.player import Player

def idsafe(text):
  return re.sub("[^A-Za-z0-9\-_\:\.]", "_", text)

trend = []
size = player.skillBuffer.size()
for i in range(0, size):
    trend.append([i, player.skillBuffer.getSkill(i)])

if len(trend) > 0:
  trendColour = "#0000FF" if trend[0][1] < trend[size - 1][1] else "#FF0000";
else:
  trendColour = "#000000"

daysAgo = (datetime.now() - player.games[-1].timeAsDatetime()).days
daysToGo = Player.DAYS_INACTIVE - daysAgo
nearlyInactive = daysToGo <= 14
%>
% if index == -1:
<tr class="inactive">
      <td class="ladder-position inactive">-</td>
% else:
  % if nearlyInactive:
    <tr class="nearly-inactive" title="Player will become inactive in ${daysToGo} day${"s" if daysToGo > 0 else ""}">
  % else:
    <tr>
  % endif
      <td class="ladder-position ${"ladder-first" if index is 0 else "" }">${index + 1}</td>
% endif
      <td class="ladder-name"><a href="${base}player/${player.name | u}/">${player.name}</a></td>
      <td class="ladder-stat">${"{:d}".format(len(player.games))}</td>
      <td class="ladder-stat">${"{:d}".format(player.wins)}</td>
      <td class="ladder-stat">${"{:d}".format(len(player.games) - player.wins - player.losses)}</td>
      <td class="ladder-stat">${"{:d}".format(player.losses)}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsFor)}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst) if player.goalsAgainst > 0 else "0"}</td>
      <td class="ladder-stat">${"{:.3f}".format(player.overrated())}</td>
      <td class="ladder-stat ladder-skill">${"{:.3f}".format(player.elo)}</td>
      <td class="ladder-stat ladder-trend"><div id="${player.name | idsafe}_trend" class="ladder-trend">&nbsp;</div></td>
      <script type="text/javascript">
        $(function() {
          $.plot("#${player.name | idsafe}_trend", [ ${trend} ], {'legend' : {show: false}, 'xaxis': {show: false}, 'yaxis': {show: false}, 'grid': {'show': false}, 'series': {'shadowSize': 0}, 'colors': ['${trendColour}']});
        });

  
      </script>
      </tr>