from flask import Flask
from config import db, Config
import os


app = Flask(__name__)


app.config.from_object(Config)


db.init_app(app)



from routes.auth import auth
app.register_blueprint(auth)



@app.route("/")
def index():
    return "Tienda de ropa funcionando"



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )