//This is functionality for the right column
function deleteFile(fileID){
    //TODO
    var answer = window.confirm("Delete file?");
    if (answer) {
      var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
      fd.append("fileID",  fileID);

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "./deleteFile");

      xhr.onload = function() {
		
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

var updateFileId;

function editDetails(fileID, name){
    updateFileId = fileID;
    document.getElementById("fname").value = name;
    document.getElementById("fname").style.visibility = 'visible';
    document.getElementById("fileDescrptionChanger").style.visibility = 'visible';
}

function sendNewName(){
    document.getElementById("fname").style.visibility = 'hidden';
    document.getElementById("fileDescrptionChanger").style.visibility = 'hidden';

    var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
    fd.append("fileID",  updateFileId);
    fd.append("details", document.getElementById("fname").value);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "./updateFileDetails");

    xhr.onload = function() {
            var fd = new FormData();
            fd.append("postID", document.getElementById("postID").value);

             var xhr = new XMLHttpRequest();
             xhr.open("POST", "./nicShowFiles");

             xhr.onload = function() {
                 var tabl = "<tbody>";
                 var data = JSON.parse(xhr.responseText);
                 for(var i = 0; i < data.length; i++){

                    let id = data[i].id;
                    let title = data[i].title
                     tabl += `<tr><td>` + title + `</td><td><a href="getfile/`+ id +`" target="_blank">Link</a></td><td>
                      <button title="Copy link to file" onclick="copyToClipboard('getfile/`+ id +`')">Copy</button> </td><td>
                      <button title="Delete the file" onclick="deleteFile('`+ id +`')">Delete</button> </td><td>
                      <button title="Edit file user friendly text" onclick="editDetails('`+ id +`', '`+ title +`')">Edit</button></td></tr>`;
                 }
                 tabl += "</tbody>";
                document.getElementById("files").innerHTML = tabl;
             };
            xhr.send(fd);
    };
    xhr.onerror = function() {
		tmpBar = document.getElementById("errorBar")
		tmpBar.style.display='block'
		tmpBar.childNodes[tmpBar.childNodes.length - 1].textContent  = "File not uploaded!";
    };
    xhr.send(fd);
}


function changeAnswerType(selct){
    var ansArea = document.getElementById("answers_area")
    var selected = selct.value
    var newHtml = ""
    if(selected == '0'){ //freetext
        newHtml += `<input type="text" id="freeTextAns" style = "width: 100%;" value="">`;
        ansArea.innerHTML = newHtml;
        return;
    } else if(selected == '1'){ //one choice
        var type = "radio"
    } else{ //multiple
        var type = "checkbox"
    }
    var numLines = document.getElementById("noQuestion").value
    lines = ansArea.getElementsByClassName("showinline");
    if (numLines <= 0){
        numLines = 4;
    }
    for(let i = 0; i < lines.length; i++){
        newHtml += `<div class="showinline">`;
        newHtml += `<span><input type="`+ type + `" name="chBoxGrup"/>`;
        newHtml += `</span><input type="text" class="textAns" style = "width: 100%;" value="` + lines[i].children[1].value + `">`;
        newHtml += `</div><br>`;
    }
    if(lines.length < numLines){
        var lineToAdd = numLines - lines.length;
        for(let i = 0; i < lineToAdd; i++){
        newHtml += `<div class="showinline">`;
        newHtml += `<span><input type="`+ type + `" name="chBoxGrup"/>`;
        newHtml += `</span><input type="text" class="textAns" style = "width: 100%;" value="">`;
        newHtml += `</div><br>`;
        }
    }
    ansArea.innerHTML = newHtml;
}

function changeAnswerCount(){
    var ansArea = document.getElementById("answers_area");
    var numLines = document.getElementById("noQuestion").value;
    lines = ansArea.getElementsByClassName("showinline");
    var type = lines[0].children[0].firstChild.type;
    if(type == 'checkbox'){
        if(numLines<3){ //In multiple choise we need at least 3
            numLines = 3;
        }
    }else{
        if(numLines < 2){ //In single choise we need at least 2
            numLines = 2;
        }
    }

    if (numLines <= 0){
        numLines = 4;
    }
    if(lines.length < numLines){
        var lineToAdd = numLines - lines.length;

        var newHtml = ansArea.innerHTML;
        for(let i = 0; i < lineToAdd; i++){
        newHtml += `<div class="showinline">`;
        newHtml += `<span><input type="`+ type + `" name="chBoxGrup"/>`;
        newHtml += `</span><input type="text" class="textAns" style = "width: 100%;" value="">`;
        newHtml += `</div><br>`;
        }
    }else{
        var newHtml = "";
        for(let i = 0; i < numLines; i++){
        newHtml += `<div class="showinline">`;
        newHtml += lines[i].innerHTML;
        newHtml += `</div><br>`;
        }
    }
    ansArea.innerHTML = newHtml;
}