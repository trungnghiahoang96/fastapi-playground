from pprint import pprint

from bottle import *


@route("/")
def home():
    
    pprint(dict(request.headers))

    if 'text/html' in request.headers.get('Accept', '*/*'):
        response.content_type = 'text/html'
        return "<h1>Hello world!</h1>"
    
    response.content_type = 'text/plain'
    return 'nghia'

@route('/now')
def time_service():
    response.content_type = 'text/plain'
    response.set_header('Cache-Control', 'max-age=1')
    return time.ctime()

@route('/upper/<word>')
def upper_case_service(word):
    return f"<h1> {word.upper()} </h1>"

@route('/area/circle')
def circle_area_service():
    import math
    pprint(dict(request.query))

    try:
        radius = float(request.query.get('radius','0.0'))
    except ValueError as e:
        return e.args[0]

    area = math.pi * (radius ** 2.0)
    if 'text/html' in request.headers.get('Accept', '*/*'):
        return '<h1> Area: ' + str(area) + '</h1>'

    return dict(radius=radius, area=area, service=request.path)

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)


