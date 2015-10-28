<%page args="sortCol=10, sortOrder=1, showInactive=0"/>
<%! from datetime import datetime %>
<%namespace name="blocks" file="blocks.mako" />
<%
headings = [
    "Pos",
    "Player",
    "Games",
    "Wins",
    "Draws",
    "Losses",
    "For",
    "Against",
    "Goal ratio",
    "Overrated",
    "Skill",
    "Trend"
]

%>
      <table class="table table-hover ladder" id="ladder">
        <thead>
            <tr>
% for heading in headings:
              <th class="${"headerSortUp" if sortCol==loop.index and sortOrder==1 else "headerSortDown" if sortCol==loop.index else ""}">${heading}</th>
% endfor
            </tr>
        </thead>
        <tbody>
<% rank = 0 %>
% for player in ladder.getPlayers():
  % if player.isActive():
    ${blocks.render("ladderEntry", player=player, index=rank, base=base)}
    <% rank += 1 %>
  % else:
    ${blocks.render("ladderEntry", player=player, index=-1, base=base)}
  % endif
% endfor
          </tbody>
        </table>
        <p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <div class="controls form">
          <button class="button_active form-control" onclick="$('.inactive').show(); $('.button_active').hide();">Show inactive</button>
          <button class="form-control inactive" onclick="$('.inactive').hide(); $('.button_active').show();">Hide inactive</button>
        </div>
        <script type="text/javascript">
        $("#ladder").tablesorter({'sortList': [[${sortCol},${sortOrder}]], 'headers': { 11: { 'sorter': false}}});
        $("#ladder").floatThead();
        // ${showInactive}
% if showInactive == "1":
        $('.inactive').show(); $('.button_active').hide();
% endif
        </script>