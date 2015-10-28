<%! title = "" %>
<%! base = "../../" %>
<%! import os %>
<%inherit file="html.mako" />
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8 col-md-offset-2">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Delete Game</h2>
        </div>
        <div class="panel-body">
<%
  user = os.environ["REMOTE_USER"] if "REMOTE_USER" in os.environ else "Stranger"
%>
          <p>${user}, are you sure you wish to delete this game?</p>
          <a href="javascript:history.go(-1);" class="btn btn-default">No, I'd rather not</a> <a class="btn btn-danger" href="?deleteConfirm=true">Yes, delete it</a>
        </div>
      </div>
    </div>
  </div>
</div>
${self.blocks.render("game", game=game, base=self.attr.base)}