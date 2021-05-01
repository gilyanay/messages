import logging

from dotenv import load_dotenv
from flask import Flask

from flask_messages.controllers import messages_bp
from flask_messages.controllers.users import users_bp

log = logging.getLogger(__name__)
load_dotenv()

app = Flask(__name__)


app.register_blueprint(messages_bp, url_prefix="/message")
app.register_blueprint(users_bp, url_prefix="/users")


if __name__ == "__main__":
    app.run("0.0.0.0", "5000")








