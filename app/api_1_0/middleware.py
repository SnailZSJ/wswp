from sanic.sanic import Sanic
from sanic.response import text


app = Sanic()


@app.middleware
async def halt_request(request):
    print("I am a spy")


@app.middleware('request')
async def halt_request(request):
    return text('I halted the request')


@app.middleware('response')
async def halt_response(request, response):
    return text('I halted the response')


@app.route('/')
async def handler(request):
    return text('I would like to speak now please')
