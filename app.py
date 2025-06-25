from flask import (
    Flask
    )
from config import Config
from models import db
from notes.routes import notes_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(notes_bp)