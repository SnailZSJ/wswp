from sanic.sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/json")
def post_json(request):
    return json({ "received": True, "message": request.json })


@app.route("/form")
def post_json(request):
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })


@app.route("/files")
def post_json(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type,
    }

    return json({ "received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters })


@app.route("/query_string")
def query_string(request):
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })