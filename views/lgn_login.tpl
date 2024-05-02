<!DOCTYPE html>
<html>
<!DOCTYPE html>
<head>
<title>Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel='stylesheet' href='/static/css/w3.css'>
</head>
<body>

<div class="container">
	<form class="well form-horizontal" action="./login" method="post"  id="contact_form">
		<fieldset>
			<input type="hidden" name="csrf_token" value="{{csrf_token}}"></input>
			<!-- Form Name -->
			<legend><center><h2><b>Login</b></h2></center></legend><br>

			<!-- Text input-->

			<div class="form-group">
			  <label class="col-md-4 control-label">User name</label>  
			  <div class="col-md-4 inputGroupContainer">
			  <div class="input-group">
			  <span class="input-group-addon"><i class="icon"></i></span>
			  <input  name="user_name" placeholder="User name" class="form-control"  type="text">
			  </div>
			  </div>
			</div>

			<!-- Text input-->

			<div class="form-group">
			  <label class="col-md-4 control-label" >Password</label> 
				<div class="col-md-4 inputGroupContainer">
				<div class="input-group">
			  <span class="input-group-addon"><i class="icon"></i></span>
			  <input name="user_password" placeholder="Password" class="form-control"  type="password">
				</div>
			  </div>
			</div>

			%if defined('error'):
			<!-- message -->
			  <div class="alert" role="alert" id="messageID"><i class="icon">{{error}}</i></div>
			%end

			<!-- Button -->
			<div class="form-group">
			  <label class="col-md-4 control-label"></label>
			  <div class="col-md-4"><br>
				<button type="submit" class="btn btn-warning" >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspSUBMIT <span class="icon"></span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</button>
			  </div>
			</div>
		</fieldset>
	</form>
</div><!-- /.container -->
</body>
</html>
