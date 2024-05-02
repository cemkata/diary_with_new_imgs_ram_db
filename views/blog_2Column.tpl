<%
mainStyle = 'bottom-footer-grid-2-column-grid'
if not defined('additionalSyles'):
  additionalSyles = []
end # if not defined('additionalSyles'):
%>
% include('blog_header.tpl', title=content['title'], mainStyle = mainStyle, additionalSyles = additionalSyles)

	<div class="holy-grail-bottom-footer-grid">
		<header class="header">
			<h1>{{!content['header']}}</h1>
		</header>
		<main class="main-content">
			<div class="responsive-two-column-grid">
				<div class="red">{{!column1}}</div>
				<div class="orange">{{!column2}}</div>
				<div class="yellow">{{!column3}}</div>
		</main>
% include('blog_footer.tpl', footer=content['footer'])