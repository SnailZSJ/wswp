from sanic.sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound
from sanic.exceptions import ServerError


app = Sanic()


@app.route('/killme')
def i_am_ready_to_die(request):
    raise ServerError("Something bad happened")


@app.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))