/* START CONFIG */
var nicUploadOptions = {
	buttons : {
		'upload' : {name : 'Upload Image', type : 'nicUploadButton'}
	}
	
};
/* END CONFIG */

var nicUploadButton = nicEditorAdvancedButton.extend({	
	//nicURI : 'https://api.imgur.com/3/image',
  errorText : 'Failed to upload image',

	addPane : function() {
		if(typeof window.FormData === "undefined") {
		  return this.onError("Image uploads are not supported in this browser, use Chrome, Firefox, or Safari instead.");
		}
		
		this.im = this.ne.selectedInstance.selElm().parentTag('IMG');

		var container = new bkElement('div')
		  .setStyle({ padding: '10px' })
		  .appendTo(this.pane.pane);

			new bkElement('div')
		  .setStyle({ fontSize: '14px', fontWeight : 'bold', paddingBottom: '5px' })
		  .setContent('Insert an Image')
		  .appendTo(container);

		this.fileInput = new bkElement('input')
		  .setAttributes({ 'type' : 'file', 'accept' : 'image/*' })
		  .appendTo(container);

		this.progress = new bkElement('progress')
		  .setStyle({ width : '100%', display: 'none' })
		  .setAttributes('max', 100)
		  .appendTo(container);

		this.fileInput.onchange = this.uploadFile.closure(this);
	},

  onError : function(msg) {
    this.removePane();
    alert(msg || "Failed to upload image");
  },

  uploadFile : function() {
    var file = this.fileInput.files[0];
    if (!file || !file.type.match(/image.*/)) {
      this.onError("Only image files can be uploaded");
      return;
    }
    this.fileInput.setStyle({ display: 'none' });
    this.setProgress(0);

    var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
    fd.append("image", file);
	fd.append("postID", document.getElementById("postID").value)

    var xhr = new XMLHttpRequest();
    //xhr.open("POST", this.ne.options.uploadImgURI || this.nicURI);
    xhr.open("POST", this.ne.options.uploadImgURI);

    xhr.onload = function() {
      try {
        var data = JSON.parse(xhr.responseText);
      } catch(e) {
        return this.onError();
      }
      if(data.error) {
        return this.onError(data.error);
      }
      this.onUploaded(data);
    }.closure(this);

    xhr.onerror = this.onError.closure(this);
    xhr.upload.onprogress = function(e) {
      this.setProgress(e.loaded / e.total);
    }.closure(this);
    //xhr.setRequestHeader('Authorization', 'Client-ID c37fc05199a05b7');
    xhr.send(fd);
  },

  setProgress : function(percent) {
    this.progress.setStyle({ display: 'block' });
    if(percent < .98) {
      this.progress.value = percent;
    } else {
      this.progress.removeAttribute('value');
    }
  },

  onUploaded : function(options) {
    this.removePane();
    var src = '/diary/getfile/' + options.link;
    if(!this.im) {
      this.ne.selectedInstance.restoreRng();
      var tmp = 'javascript:nicImTemp();';
      this.ne.nicCommand("insertImage", src);
      this.im = this.findElm('IMG','src', src);
    }
    var w = parseInt(this.ne.selectedInstance.elm.getStyle('width'));
    if(this.im) {
      this.im.setAttributes({
        src : src,
        className : "popImage",
        width : (w && options.width) ? Math.min(w, options.width) : ''
      });
    }
  }
});

if (typeof initPageEditor !== 'undefined'){
  nicEditors.registerPlugin(nicPlugin,nicUploadOptions);
}

var nicCodeOptions = {
	buttons : {
		'table' : {name : 'Insert table', type : 'nicAddTableButton'},
		'xhtml' : {name : 'Edit HTML', type : 'nicCodeButton'},
	}
	
};

var nicCodeButton = nicEditorAdvancedButton.extend({
	width : '350px',
		
	addPane : function() {
		this.addForm({
			'' : {type : 'title', txt : 'Edit HTML'},
			'code' : {type : 'content', 'value' : this.ne.selectedInstance.getContent(), style : {width: '340px', height : '200px'}}
		});
	},
	
	submit : function(e) {
		var code = this.inputs['code'].value;
		this.ne.selectedInstance.setContent(code);
		this.removePane();
	}
});

var nicAddTableButton = nicEditorAdvancedButton.extend({
	addPane : function () {
		this.addForm({
			    '': { type: 'title', txt: 'Insert Table' },
			    'rows': { type: 'text', txt: 'Rows', value: '5', style: { width: '150px'} },
			    'cols': { type: 'text', txt: 'Columns', value: '2', style: { width: '150px'} },
			    'border': { type: 'text', txt: 'Border', value: '1', style: { width: '150px'} },
			    'width': { type: 'text', txt: 'Width', value: '100%', style: { width: '150px'} }
		});
	},
	
	submit: function (e) {
		var rows = parseInt(this.inputs['rows'].value);
		if(isNaN(rows)){
			alert("Check rows value")
			return false;
		}
		var cols = parseInt(this.inputs['cols'].value);
		if(isNaN(cols)){
			alert("Check columns value")
			return false;
		}
		var border = parseInt(this.inputs['border'].value);
		if(isNaN(border)){
			alert("Check border value")
			return false;
		}
		var width = parseInt(this.inputs['width'].value);
		if(isNaN(width)){
			alert("Check width value")
			return false;
		}
		var cellw = (1/cols)*100;
		var TableCode = '<table width="'+ width +'%" border="'+ border +'"><thead><tr>';
	
		for (i=1;i<=cols;i++) {
			TableCode += '<th width="'+ cellw +'%">Header</th>';
		}
		
		TableCode += '</tr></thead><tbody>';
		
		var alternate = 'even';
		
		for (j=1;j<=rows;j++)	{

			TableCode += '<tr>';

			for (i=1;i<=cols;i++)	{
				TableCode += '<td width="'+ cellw +'%">Content</td>';
			}

			TableCode += '</tr>';		
		}
		
		TableCode += '</tbody></table>';
		this.removePane();
		this.ne.nicCommand('insertHTML', TableCode);
	}
});

if (typeof initPageEditor !== 'undefined'){
  nicEditors.registerPlugin(nicPlugin,nicCodeOptions);
}

var nicUploadFile = nicEditorAdvancedButton.extend({
  errorText : 'Failed to upload',

	addPane : function() {
    if(typeof window.FormData === "undefined") {
      return this.onError("Failed to upload.");
    }

    var container = new bkElement('div')
      .setStyle({ padding: '10px' })
      .appendTo(this.pane.pane);

		new bkElement('div')
      .setStyle({ fontSize: '14px', fontWeight : 'bold', paddingBottom: '5px' })
      .setContent('Upload file')
      .appendTo(container);

    docList = ['Image', 'Document PDF', 'Other file', 'Audio', 'Video'];
    htmlStr = ``
    for(let i = 0; i< docList.length; i++){
      if(i == 0){
        htmlStr += `<input type="radio" name="type" id="row`+ i +`" value="` + i + `" checked="checked"><label for="row`+i+`">`+ docList[i] +`</label><br>`;
      }else{
        htmlStr += `<input type="radio" name="type" id="row`+ i +`" value="` + i + `"><label for="row`+i+`">`+ docList[i] +`</label><br>`;
      }
    }
    htmlStr += `<br><label for="usFendly">User friendly name:</label><input type="text" id="usfrname" name="usfrname"><br>`
		container.innerHTML += `<div style="font-size: 12px; font-weight: bold; padding-bottom: 5px;">` + htmlStr;

    this.fileInput = new bkElement('input')
      .setAttributes({ 'type' : 'file' })
      .appendTo(container);

    this.progress = new bkElement('progress')
      .setStyle({ width : '100%', display: 'none' })
      .setAttributes('max', 100)
      .appendTo(container);

    this.fileInput.onchange = this.uploadFile.closure(this);
	},

  onError : function(msg) {
    this.removePane();
    alert("Failed to upload file");
  },

  uploadFile : function() {
    var file = this.fileInput.files[0];
    if (!file) {
      this.onError("Sothing went wrong.");
      return;
    }
	
	  fileType = document.querySelector('input[name=type]:checked').defaultValue;
	
    this.fileInput.setStyle({ display: 'none' });
    this.setProgress(0);

    var fd = new FormData(); // https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
    fd.append("filetype", fileType);
    fd.append("postID", document.getElementById("postID").value)
    fd.append("usfrname", document.getElementById("usfrname").value)
    fd.append("filedata", file);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", this.ne.options.uploadFileURL);

    xhr.onload = function() {
      try {
        var data = JSON.parse(xhr.responseText);
		var table = document.getElementById("files");
		var row = table.insertRow(0);
		
		
		var tabl = `<tr><td>` + data.name + `</td><td><a href="./getfile/`+ data.link +`"  target="_blank">Link</a></td><td> <button onclick="copyToClipboard('getfile/`+ data.link +`')">Copy link</button>  <button title="Delete the file" onclick="deleteFile('`+ data.link + `')">Delete</button> </td><td> <button title="Edit file user friendly text" onclick="editDetails('`+ data.link + `', '`+ data.name +`')">Edit</button></td></tr> </td></tr>`;
        row.innerHTML = tabl;
      } catch(e) {
        return this.onError();
      }
      if(data.error) {
        return this.onError(data.error);
      }
      this.onUploaded(data);
    }.closure(this);
    xhr.onerror = this.onError.closure(this);
    xhr.upload.onprogress = function(e) {
      this.setProgress(e.loaded / e.total);
    }.closure(this);
    //xhr.setRequestHeader('Authorization', 'Client-ID c37fc05199a05b7');
    xhr.send(fd);
  },

  setProgress : function(percent) {
    this.progress.setStyle({ display: 'block' });
    if(percent < .98) {
      this.progress.value = percent;
    } else {
      this.progress.removeAttribute('value');
    }
  },

  onUploaded : function(options) {
    this.removePane();
  }
});

var nicUploadFileOptions = {
	buttons : {
		'uploadFile' : {name : 'Upload file', type : 'nicUploadFile'},
	},
    iconFiles: {
        'uploadFile': '/static/img/nic/test_nicEditorClip.png'
    }
};

if (typeof initPageEditor !== 'undefined'){
  nicEditors.registerPlugin(nicPlugin,nicUploadFileOptions);
}

function copyToClipboard (str) {
  const el = document.createElement('textarea');
  el.value = el.baseURI + str;
  el.setAttribute('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild(el);
  el.select();
  //document.execCommand('copy');
  navigator.clipboard.writeText(el.value);
  document.body.removeChild(el);
};

/* START CONFIG */
var nicImageOptionsBase64 = {
	buttons : {
		'image' : {name : 'Add Image', type : 'nicImageButtonBase64', tags : ['IMG']}
	}
};
/* END CONFIG */

var tmp_holder = 0;
var nicImageButtonBase64 = nicEditorAdvancedButton.extend({

	//mouseClick : this.addPane(),

  addPane : function() {
    this.im = this.ne.selectedInstance.selElm().parentTag('IMG');
    this.fileInput = new bkElement('input')
      .setAttributes({ 'type' : 'file' , "accept" : "image/*"})
      .appendTo(this.pane.pane);

    tmp_holder = this;

    this.fileInput.onchange = this.setBase64Image;
    this.fileInput.click();
	},

  setBase64Image : function(e) {
    if (this.files[0]) {
      var reader = new FileReader();
      reader.addEventListener("load", function() {
        if(!tmp_holder.im) {
          var tmp = 'javascript:nicImTemp();';
          tmp_holder.ne.nicCommand("insertImage",tmp);
          tmp_holder.im = tmp_holder.findElm('IMG','src',tmp);
        }
        if(tmp_holder.im) {
          tmp_holder.im.setAttributes({
            src : this.result,
            alt : '',
            className : "popImage",
            align : 'none',
          });
        }
        tmp_holder.removePane();
        tmp_holder = 0;
      });
      reader.readAsDataURL(this.files[0]);
    }
  }
});

if (typeof initPageEditor === 'undefined'){
  for(let i = 0; i < nicEditors.nicPlugins.length; i++){
    try {
      if(nicEditors.nicPlugins[i].o.buttons.image.type == "nicImageButton"){
        nicEditors.nicPlugins.splice(i, 1)
        nicEditors.registerPlugin(nicPlugin,nicImageOptionsBase64);
        i = nicEditors.nicPlugins.length;
      }
    } catch (error) {
      j = 0;
    }
  }
}

//Used https://success.outsystems.com/Documentation/How-to_Guides/Front-End/How_can_you_prevent_users_from_losing_unsaved_changes%3F

var confirmationMessage = "You have unsaved changes. Are you sure you want to leave?";

var isModified = function () {
  if (document.getElementById("title")!=null){
    return !(titletextLength == document.getElementById("title").value.length) && (descriptiontextLength == document.getElementById("area").value.length);
  }else{
    return !(titletextLength == document.getElementById("area_question").value.length) && (descriptiontextLength == document.getElementById("area_explanation").value.length);
  }
}

// Handle normal button and link clicks on the page
document.body.addEventListener(
  "click",
    function(event){
     if (event.target.tagName === "BUTTON" || event.target.tagName === "A") {
        var associatedWithForm = event.target.form
        var isInProtectedForm = associatedWithForm && event.target.form.id ===  $parameters.FormId
        if(!isInProtectedForm && isModified()) {
            if(!confirm(confirmationMessage)) {
                event.stopPropagation();
                event.preventDefault()
                return false;
             }
          }
        }
  }
)

// Catch navigating back
window.onpopstate = function(event) {
  if(isModified()) {
        if(!confirm(confirmationMessage)) {
          history.pushState(null, document.title, location.href);
        }
    }
}

function confirmExit (event) {
   if(isModified()) {
       (event || window.event).returnValue = confirmationMessage; //Gecko + IE
       return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
    }
}

// Catch window close
window.onbeforeunload = confirmExit;

//variables used to check if the text was modifed
//Well if the nex text is the same length as the old the chech will return true
//To be fixed later
if (typeof initPageEditor !== 'undefined'){
  var titletextLength = document.getElementById("title").value.length
  var descriptiontextLength = document.getElementById("area").value.length
}else{
  var titletextLength = document.getElementById("area_question").value.length
  var descriptiontextLength = document.getElementById("area_explanation").value.length
}
