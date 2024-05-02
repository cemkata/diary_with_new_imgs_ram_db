	<div class="tab">
	  <button class="tablinks" onclick="openTab(event, 'feelings')" id="defaultOpen">{{translation[11]}}</button>
	  <button class="tablinks" onclick="openTab(event, 'files')">{{translation[2]}}</button>
	</div>
	<div id="files" class="tabcontent">
	{{!content['tabFiles']}}
	</div>	
	<div id="feelings" class="tabcontent">
	{{!content['tabFeelings']}}
	</div>
<!-- JS -->
<script>
function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
</script>