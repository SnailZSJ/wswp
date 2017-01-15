from sanic.sanic import Sanic
from sanic.response import text


app = Sanic()


@app.route('/tag/<tag>')
async def person_handler(request, tag):
    return text('Tag - {}'.format(tag))


@app.route('/number/<integer_arg:int>')
async def person_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))


@app.route('/number/<number_arg:number>')
async def person_handler(request, number_arg):
    return text('Number - {}'.format(number))


@app.route('/person/<name:[A-z]>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))


@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))