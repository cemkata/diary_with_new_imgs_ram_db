<!DOCTYPE html>
<html>
<!DOCTYPE html>
<head>
<title>{{action}}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel='stylesheet' href='/static/css/w3.css'>
</head>
<body>

 <div class="container">

    <form class="well form-horizontal" action=" " method="post"  id="contact_form">
<fieldset>

<!-- Form Name -->
<legend><center><h2><b>{{action}} Form</b></h2></center></legend><br>

<!-- Text input-->

<div class="form-group">
  <label class="col-md-4 control-label">First Name</label>  
  <div class="col-md-4 inputGroupContainer">
  <div class="input-group">
  <span class="input-group-addon"><i class="icon"></i></span>
%if defined('fname'):
  <input  name="first_name" placeholder="First Name" value="{{fname}}" class="form-control-error"  type="text">
%else:
  <input  name="first_name" placeholder="First Name" class="form-control"  type="text">
%end
    </div>
  </div>
</div>

<!-- Text input-->

<div class="form-group">
  <label class="col-md-4 control-label" >Last Name</label> 
    <div class="col-md-4 inputGroupContainer">
    <div class="input-group">
  <span class="input-group-addon"><i class="icon"></i></span>
%if defined('lname'):
  <input  name="last_name" placeholder="Last Name" value="{{lname}}" class="form-control-error"  type="text">
%else:
  <input name="last_name" placeholder="Last Name" class="form-control"  type="text">
%end
    </div>
  </div>
</div>

<!-- Text input-->

<div class="form-group">
  <label class="col-md-4 control-label">Username</label>  
  <div class="col-md-4 inputGroupContainer">
  <div class="input-group">
  <span class="input-group-addon"><i class="icon"></i></span>
%if defined('user_name'):
  <input  name="user_name" placeholder="Username" value="{{user_name}}" class="form-control-error"  type="text">
%else:
  <input  name="user_name" placeholder="Username" class="form-control"  type="text">
%end
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

<!-- Text input-->

<div class="form-group">
  <label class="col-md-4 control-label" >Confirm Password</label> 
    <div class="col-md-4 inputGroupContainer">
    <div class="input-group">
  <span class="input-group-addon"><i class="icon"></i></span>
  <input name="confirm_password" placeholder="Confirm Password" class="form-control"  type="password">
    </div>
  </div>
</div>

<!-- Text input-->
       <div class="form-group">
  <label class="col-md-4 control-label">E-Mail</label>  
    <div class="col-md-4 inputGroupContainer">
    <div class="input-group">
        <span class="input-group-addon"><i class="icon"></i></span>
%if defined('email'):
  <input  name="email" placeholder="E-Mail Address" value="{{email}}" class="form-control-error"  type="text">
%else:
  <input name="email" placeholder="E-Mail Address" class="form-control"  type="text">
%end
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
