# {{ project }}:app
import bottle
from bottle import (
    default_app,
    run,
    error,
    route,
    post,
    get,
    request,
    response,
    template,
    static_file
)

bottle.TEMPLATE_PATH = ['./views/', './views/templates/']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=STATIC_ROOT)

@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root=MEDIA_ROOT, download=filename)

@error(404)
def error404(error):
    return '404 - Not Found'

@route('/ip')
def ip():
    return request['REMOTE_ADDR']

@route('/')
def index():
    return template('index.html')

application = default_app()
run(debug=True, reloader=True, host='localhost', port=8080)
