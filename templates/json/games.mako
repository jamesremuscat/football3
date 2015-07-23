<%! base = "../../../" %>
<%
def accept(game):
    return (not fromTime or game.time >= fromTime) and (not toTime or game.time <= toTime)
%>
<%inherit file="json.mako" />[
% for g in [g for g in ladder.games if accept(g)]:
    ${self.blocks.render("game", game=g, base=self.attr.base)}${"," if loop.index < len (ladder.games) - 1 else ""}
% endfor
]
