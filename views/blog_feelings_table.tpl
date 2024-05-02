 <input type="hidden" id="cats_length" value="{{len(tableContent['categories'])}}">
 <input type="hidden" id="goals_length" value="{{len(tableContent['goal'][0])}}">
 %if defined('translation'):
 <div class='boldText size12'><button title="{{translation[12]}}" onclick="saveTable()">{{translation[12]}}</button></div>
 <br>
 % end # of if defined(translation):
 
 % for i in range(len(tableContent['categories'])):
   <div class='{{tableContent['categories'][i]['color']}} boldText size12 paddingLeft025'>{{tableContent['categories'][i]['text']}}</div>
  %for k in range(len(tableContent['goal'][i])):
	%if defined('allowEdit'):
		 <div class='grayColor paddingLeft025 size12 {{tableContent['goal'][i][k]['format']}}'>{{!tableContent['goal'][i][k]['text']}}</div>
		 % for j in range(len(tableContent['daysContent'][i][k])):
			<div class='whiteColor {{tableContent['daysContent'][i][k][j]['format']}} paddingLeft075' contenteditable='true'>{{tableContent['daysContent'][i][k][j]['text']}}</div>
		 % end # of for j in range(len(tableContent['daysContent'][i][k])):
	%else:
		 % for j in range(len(tableContent['daysContent'][i][k])):
	      % if tableContent['goal'][i][k]['text'] != '&nbsp;' and tableContent['daysContent'][i][k][j]['text'] != '&nbsp;':
	        <div class='grayColor paddingLeft025 size12 {{tableContent['goal'][i][k]['format']}}'>{{!tableContent['goal'][i][k]['text']}}</div>
          % end # of if len(tableContent['daysContent'][i][k][j]['text']) != '&nbsp;':
			<div class='whiteColor {{tableContent['daysContent'][i][k][j]['format']}} paddingLeft075'>{{tableContent['daysContent'][i][k][j]['text']}}</div>
		 % end # of for j in range(len(tableContent['daysContent'][i][k])):		
	 % end # of if not defined('allowEdit'):
  % end # of %for k in len(tableContent['goal'][i]):
 % end # of %for i in len(tableContent['categories']):
 %if defined('translation'):
 <br>
 <div class='boldText size12 paddingLeft025'><button title="{{translation[12]}}" onclick="saveTable()">{{translation[12]}}</button></div>
 % end # of if defined(translation):
