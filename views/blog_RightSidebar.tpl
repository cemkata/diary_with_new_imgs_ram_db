<%
mainStyle = 'bottom-footer-grid-right-sidebar'
if not defined('additionalSyles'):
  additionalSyles = []
end # if not defined('additionalSyles'):
%>
% include('blog_header.tpl', title=content['title'], mainStyle = mainStyle, additionalSyles = additionalSyles)

	<div class="bottom-footer-grid-right-sidebar">
		<header class="header">
			<h1>{{!content['header']}}</h1>
		</header>
		<main class="main-content">
			{{!content['main']}}
		</main>
		<section class="right-sidebar">
	{{!content['right']}}
		</section>
% include('blog_footer.tpl', footer=content['footer'])