<%! title = "" %>
<%! base = "../../" %>
<%inherit file="html.mako" />
${self.blocks.render("game", game=game, base=self.attr.base)}
<div class="recent-game container-fluid">
  <div class="row achievements">
    <div class="col-md-4">
    % for ach in game.redAchievements:
      ${self.blocks.render("achievement", ach=ach)}
    % endfor
    </div>
    <div class="col-md-4 col-md-offset-4">
    % for ach in game.blueAchievements:
      ${self.blocks.render("achievement", ach=ach)}
    % endfor
    </div>
  </div>
</div>
<p><a href="json">This game as JSON</a></p>
% if not game.isDeleted():
<a href="delete" class="btn btn-danger pull-right"><span class="glyphicon glyphicon-lock"></span> Delete game</a>
% endif