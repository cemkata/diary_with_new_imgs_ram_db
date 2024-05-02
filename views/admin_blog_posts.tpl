<h2>{{translation[15]}}</h2>
<table class="table responsive">
  <thead>
    <tr>
      <td>{{translation[14]}}</td>
      <td>{{translation[10]}}</td>
      <td>{{translation[8]}}</td>
      <td>(Un)Hide</td>
    </tr>
  </thead>
  <tbody>
  %for p in posts:
    <tr>
      <td data-label="{{translation[14]}}">{{p['day']}}/{{p['month']}}/{{p['year']}}</td>
      <td data-label="{{translation[10]}}">&nbsp;
	  %if p['hidden']:
	  <span class = "hidden_post" >{{translation[17]}}</span>  
	  %end # of %if p['hidden']:
	  <a href="/diary/editor?postID={{p['id']}}" style="">{{p['title']}}</a></td>
      <td data-label="{{translation[8]}}"><button onclick="deletePost('{{p['id']}}')">{{translation[8]}}</button> </td>
      <td data-label="{{translation[16]}}"><button onclick="hidePost('{{p['id']}}')">{{translation[16]}}</button> </td>
    </tr>
  %end # of %for p in posts:
  </tbody>
</table>

<script>
function deletePost(postID){
    //TODO
    var answer = window.confirm("Delete file?");
    if (answer) {
      //Logic to delete the post
      var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
      fd.append("postID",  postID);

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "./deletePost");

      xhr.onload = function() {
		tmpBar = document.getElementById("infoBar")
		tmpBar.style.display='block'
		tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Post deleted.";
      };
      xhr.onerror = function() {
		tmpBar = document.getElementById("errorBar")
		tmpBar.style.display='block'
		tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Error when deleting!";
      };
      xhr.send(fd);
    }
    else {
        //some code
    }
}
function hidePost(postID){
	//Logic to delete the post

	//TODO
	var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
	fd.append("postID",  postID);

	var xhr = new XMLHttpRequest();
	xhr.open("POST", "./hidePost");

	xhr.onload = function() {
		tmpBar = document.getElementById("infoBar")
		tmpBar.style.display='block'
		tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Post (Un)Hided.";
	};
	xhr.onerror = function() {
		tmpBar = document.getElementById("errorBar")
		tmpBar.style.display='block'
		tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Error when (Un)Hide!";
	};
	xhr.send(fd);
}
</script>

<div id="errorBar" class="bar error floating">
  <div class="close" onclick="this.parentElement.style.display='none'">X</div>
  <i class="ico">&#9747;</i>
</div>
<div id="infoBar" class="bar info floating">
  <div class="close" onclick="this.parentElement.style.display='none'">X</div>
  <i class="ico">&#8505;</i>
</div>

