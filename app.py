from flask import Flask
from config import db

app = Flask(__name__)

db.init_app(app)


from routes.auth import auth
app.register_blueprint(auth)


@app.route("/")
def index():
    return "Tienda de ropa funcionando"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)