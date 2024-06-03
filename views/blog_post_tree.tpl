<ul class="tree">
  <li><a href="/table/">GO to self help table</a></li>
  <li><a href="/diary/editor">Add post</a></li>

%for t in tree:
  <li class="section">
	<input type="checkbox" id="group{{t['year']}}">
	<label for="group{{t['year']}}">{{t['year']}}</label>
	%for m in t['mounts']:
	<ul>
	  <li class="section">
		<input type="radio" name="group_{{t['year']}}" id="group{{t['year']}}-{{m['mountName']}}">
		<label for="group{{t['year']}}-{{m['mountName']}}">{{m['mountName']}}</label>
		<!-- <label for="group{{t['year']}}-{{m['mountName']}}">{{m['mountName']}} ({{m['mountNumber']}})</label> -->
		<ul>
		%for d in m['days']:
		  <li><a href="/diary/{{d[0]}}/{{m['mountNumber']}}/{{t['year']}}">{{d[0]}} | <span style="color: black;">{{d[1]}}</span></a></li>
		%end #%for d in m['days']:
		</ul>
	  </li>
	</ul>
	%end #%for m in t['mounts']:
  </li>
%end #for t in tree:
<!-- </ul><ul  style="color: rgba(0, 0, 0, 0);"> -->
<li class="hidden_section">
	<input type="checkbox" id="adminMenu">
	<label for="adminMenu" style="color: rgba(0, 0, 0, 0);">Admin Menu</label>
		<ul>
		  <li><a href="/diary/admin">Admin panel</a></li>
		  <li><a href="/logout">Logout</a></li>
		  <!-- <li><a href="/table/">GO to self help table</a></li>
		  <li><a href="/diary/editor">Add post</a></li> -->
		</ul>
</li>
</ul>