%def rightblock():
<form action='/{{project}}/doc/new' method='post' class="well">
  <input type='text' name='pagename' placeholder="Page name..."/><br />
  <textarea name='content' class="input-xlarge"></textarea><br />
  <input type="submit" value="Submit" class="btn btn-primary"/>
</form>
%end
%rebase wiki/wiki_base project=project, leftmenu=leftmenu, rightblock=rightblock, title=title
