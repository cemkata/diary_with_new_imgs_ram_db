    <p><b>{{translation[2]}}:</b></p>
    <table id = "files">
    <input type="text" id="fname" name="fname" style="visibility: hidden;"><button type="button" id="fileDescrptionChanger" style="visibility: hidden;" onclick="sendNewName()">{{translation[3]}}</button>
	<table class="table responsive">
      <tbody>
        % for f in files:
          <tr>
			  <td>{{f["title"]}}</td>
			  <td> <a href="/diary/getfile/{{f['id']}}"  target="_blank">{{translation[4]}}</a></td>
			  <td> <button title="{{translation[5]}}" onclick="copyToClipboard('getfile/{{f['id']}}')">{{translation[6]}}</button> </td>
			  <td> <button title="{{translation[7]}}" onclick="deleteFile('{{f['id']}}')">{{translation[8]}}</button> </td>
			  <td> <button title="{{translation[9]}}" onclick="editDetails('{{f['id']}}', '{{f['title']}}')">{{translation[10]}}</button></td>
		  </tr>
        % end
      </tbody>
    </table>