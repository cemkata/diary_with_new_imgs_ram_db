<%
mainStyle = 'bottom-footer-grid-left-sidebar'
if not defined('additionalSyles'):
  additionalSyles = []
end # if not defined('additionalSyles'):
%>
% include('blog_header.tpl', title=content['title'], mainStyle = mainStyle, additionalSyles = additionalSyles)

	<div class="left-sidebar-bottom-footer-grid">
		<header class="header">
			<h1>{{!content['header']}}</h1>
		</header>
		<main class="main-content">
			{{!content['main']}}
		</main>
		<section class="left-sidebar">{{!content['left']}}</section>
% include('blog_footer.tpl', footer=content['footer'])