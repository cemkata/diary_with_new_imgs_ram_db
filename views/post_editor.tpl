    <input type="hidden" id="postID" value="{{postID}}">
    <input type="hidden" id="postDate" value="{{postDate}}">
    <p>{{translation[0]}}<br>
      <input type="text" id="title" value="{{pageName}}">
    </p>
    <p>{{translation[1]}}<br>
      <textarea id="area" class="area" >{{pageContent}}</textarea>
	</p>
    <script type="text/javascript">initPageEditor = true;</script>
    <script src="/static/js/nicEdit.js" type="text/javascript"></script>
    <script src="/static/js/nicEditorMyExtension.js" type="text/javascript"></script>
    <script src="/static/js/nicEditorRightColumn.js" type="text/javascript"></script>

    <script type="text/javascript">
      bkLib.onDomLoaded(function() {
          new nicEditor({fullPanel : true, uploadImgURI : './nicUploadImg',
          uploadFileURL:'./nicUploadFile',onSave : saveEdit,
          iconsPath : "/static/img/nic/new_nicEditorIcons.png",
          tableURL : './nicShowFiles'}).panelInstance('area');
      });

      function saveEdit(content, id, instance) {
         var title = document.getElementById("title").value;
         var postID = document.getElementById("postID").value;
		 
		 saveTable();

         var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
         fd.append("title", title);
         fd.append("postID",  postID);
		 //remove the <divs> created during the editing
		 var cleanForm = ""
		 var tmpStr = content.split("</div>")
		 for(let i = 0; i < tmpStr.length;i++){
		    tmpStr[i] = tmpStr[i].replace('<div>', '<br>');
			if(tmpStr[i].startsWith('<div')){
			   tmpStr[i] += "</div>"
			}/*else{
			   tmpStr[i] += ""
			}*/
			cleanForm += tmpStr[i]
		 }
         fd.append("content", cleanForm);
         var xhr = new XMLHttpRequest();
         //xhr.open("POST", "./editor");
         xhr.open("POST", "./nicSave");

         xhr.onload = function() {
			 if(xhr.status == 200){
				tmpBar = document.getElementById("infoBar");
				tmpBar.style.display='block';
				tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Everithing is saved saved!";
			 }
		 };
		 xhr.onerror = function() {
			tmpBar = document.getElementById("errorBar")
			tmpBar.style.display='block'
			tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Error when saving!";
		 };
         //xhr.setRequestHeader('Authorization', 'Client-ID c37fc05199a05b7');
         xhr.send(fd);
      }
	  
	  function saveTable(){
		 var postDate = document.getElementById("postDate").value;
		 var feelingTable = document.getElementById("feelings");
		 var cats_length = document.getElementById("cats_length").value;
		 var goals_length = document.getElementById("goals_length").value;
		 var cells = feelingTable.querySelectorAll('[contenteditable=true]');
		 cells.forEach((cell, index) => {
			if(cell.innerText.length != 0){
				//Woraaround for compatibility with table save that is used here
				catSkip = 1 + (index - index % goals_length) / goals_length
				inx = index + 1 * catSkip
				
				result = JSON.stringify({customStyle: "",
										 cellRow: inx,
										 rowID: postDate,
										 cellText:cell.innerText});
				 var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
				 fd.append("contetnt", result)
				 var xhr = new XMLHttpRequest();
				 xhr.open("POST", "/table/");  //Here we send the data to the table save function
				 xhr.onload = function() {
					 /*if(xhr.status == 200){
						tmpBar = document.getElementById("infoBar")
						tmpBar.style.display='block'
					 }*/
				 };
				 xhr.onerror = function() {
					tmpBar = document.getElementById("errorBar")
					tmpBar.style.display='block'
					tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "Error when saving!";
				 };
				 xhr.send(fd);
			}
		 });
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