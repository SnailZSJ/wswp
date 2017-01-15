from sanic.sanic import Sanic
from app.api_1_0.blueprint import bp


app = Sanic(__name__)
app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)