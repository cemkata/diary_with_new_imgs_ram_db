<%
mainStyle = 'bottom-footer-grid-holy-grail'
if not defined('additionalSyles'):
  additionalSyles = []
end # if not defined('additionalSyles'):
%>
% include('blog_header.tpl', title=content['title'], mainStyle = mainStyle, additionalSyles = additionalSyles)

	<div class="holy-grail-bottom-footer-grid">
		<header class="header">
			{{!content['header']}}
		</header>
		<main class="main-content">
			{{!content['main']}}
		</main>
		<section class="left-sidebar">{{!content['left']}}</section>
		<aside class="right-sidebar">{{!content['right']}}</aside>
% include('blog_footer.tpl', footer=content['footer'])