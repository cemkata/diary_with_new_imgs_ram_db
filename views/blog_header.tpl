<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="content-language" content="en">
    <title>{{title}}</title>
    <link rel="stylesheet" type="text/css" href="/static/css/{{mainStyle}}.css">
  % for st in additionalSyles:
    <link rel="stylesheet" type="text/css" href="/static/css/{{st}}.css">
  % end #for st in additionalSyles:
    <base href=".">
</head>
<body>