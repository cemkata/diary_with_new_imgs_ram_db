<!DOCTYPE html>
<html xmlns='http://www.w3.org/TR/REC-html40'>

<head>
<title>{{pageTranslation[0]}}</title>
<meta http-equiv=Content-Type content='text/html; charset=utf-8'>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel=Stylesheet href='/static/css/stylesheet.css'>
<link rel=Stylesheet href='/static/css/newStyle.css'>
<script src='/static/js/jquery-3.6.4.min.js'></script>
<script src='/static/js/scripts.js'></script>
<script>
    var isMobile = false; //initiate as false
	$(document).ready(function(){
		addTableCellHandler();
		addContexMenu();
		addMenuEvents();
		stretchTabel();

		// device detection
		if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
		|| /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) {
			isMobile = true;
		}
		if(isMobile){
			//<div class="table-responsive">
			$('#wrapper').after(`<div class='table-responsive' id='table-responsive-holder'>`);
			$('#calenderTable').prependTo('#table-responsive-holder');
		}
		
		focusTodaysFisrtCell();
	});
</script>
</head>

<body>
<div id="wrapper"></div>
 <table id='calenderTable'>
  <tr>
   <th class='cellStayOnTop darkGrayColor size34 cellwidth'>{{pageTranslation[1]}}</th>
 % for row in pageContent['dateRow']:
   %if len(row) == 2:
   <th id='currentDateColor' class='darkGrayColor size34 cellwidth'>{{row[0]}}</th>
   %else:
   <th class='darkGrayColor size34 cellwidth'>{{row}}</th>
   % end #end of if len(row) == 2:
 % end #end of for row in dateRow:
  </tr>
  <tr>
   <th class='firstCell headerRow lightGrayColor size24 headerRow'>{{pageTranslation[2]}}</th>
 % for row in pageContent['dayRow']:
   <th class='lightGrayColor headerRow'>{{row}}</th>
 % end
  </tr>
 % for i in range(len(pageContent['categories'])):
  <tr>
   <td class='cellStayOnTop'><div class='{{pageContent['categories'][i]['color']}} boldText size12 paddingLeft025'>{{pageContent['categories'][i]['text']}}</div></td>
   % for row in pageContent['dayRow']:
   <th class='{{pageContent['categories'][i]['color']}} size12 paddingLeft025'></th>
   % end
  </tr>
  %for k in range(len(pageContent['goal'][i])):
  <tr>
   <td class='cellStayOnTop'><div class='grayColor size12 paddingLeft025 {{pageContent['goal'][i][k]['format']}}'>{{!pageContent['goal'][i][k]['text']}}</div></td>
  % for j in range(len(pageContent['dayRow'])):
  % try:
   % if j < len(pageContent['daysContent'][i][k]):
   <td class='editbleText whiteColor {{pageContent['daysContent'][i][k][j]['format']}}' contenteditable='true'>{{pageContent['daysContent'][i][k][j]['text']}}</td>
   % else:
   <td class='editbleText whiteColor' contenteditable='true'></td>
   % end # of if j < len(pageContent['daysContent'][i][k]):
   % except IndexError:
   <td class='editbleText whiteColor' contenteditable='true'></td>
   % end # of try/except IndexError:
  % end # of for j in range(len(pageContent['dayRow'])):
  </tr>
  % end # of %for k in len(pageContent['goal'][i]):
 % end # of %for i in len(pageContent['categories']):
 </table>

<a class="prev" onclick="plusOneDay(-1); setTimeout(scrollToTableBegin, 150);">&#10094;</a>
<a class="next" onclick="plusOneDay(1); setTimeout(scrollToTableEnd, 150);">&#10095;</a>

<div id='menu'>
 <fieldset>
  <legend>Text decoration:</legend>
  <div>
    <input type="checkbox" id="italic" name="italic">
    <label for="italic">Italic</label>
  </div>
  <div>
    <input type="checkbox" id="bold" name="bold">
    <label for="bold">Bold</label>
  </div>
  <div>
    <input type="checkbox" id="underline" name="underline">
    <label for="underline">Underline</label>
  </div>
  <div>
    <input type="checkbox" id="strikethrough" name="strikethrough">
    <label for="strikethrough">Strikethrough</label>
  </div>
 </fieldset>
</div>
<div id="errorBar" class="bar error floating">
  <div class="close" onclick="this.parentElement.style.display='none'">X</div>
  <i class="ico">&#9747;</i> {{pageTranslation[3]}}
</div>
<div id="infoBar" class="bar info floating">
  <div class="close" onclick="this.parentElement.style.display='none'">X</div>
  <i class="ico">&#8505;</i> {{pageTranslation[4]}}
</div>
</body>
</html>
