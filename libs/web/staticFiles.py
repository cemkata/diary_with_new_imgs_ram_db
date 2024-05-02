from libs_extrn.bottle import Bottle, static_file

app = Bottle()

##Static files are provided here
@app.route('/favicon.ico')
def favicon():
    return static_file('diary.svg', root='./views/static/img')

@app.route('/static/<filepath:path>')
def static_content(filepath):
     return static_file(filepath, root='./views/static')

@app.route('/ui/<filepath:path>')
def staticFiles(filepath):
    return static_file(filepath,  root='./views/ui')