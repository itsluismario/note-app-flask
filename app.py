from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

import os 
from flask_sqlalchemy import SQLAlchemy

DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

app.config["SQLALCHEMY_DATABASE_URI"]= f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date =  db.Column(db.DateTime, default=datetime.utcnow)

    # Common python method
    # It shows the value in the terminal
    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    notes = Note.query.all()
    ids = [note.id for note in notes]
    dates = [note.date.strftime("%Y-%m-%d %H:%M:%S") for note in notes]
    return render_template(
        "home.html", 
        notes=notes, 
        ids=ids,
        dates=dates,
        zip=zip
    )

@app.route("/about")
def about():
    return "Note app"

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "POST REQUEST!!!! :)", 201
    return "contact page"

@app.route("/api/info")
def api_info():
    data = {
        "name": "Notes app",
        "version": "1.0.1"
    }
    return jsonify(data), 200

@app.route("/confirmation")
def confirmation():
    return "Test"

@app.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title") or ""
        content = request.form.get("content") or ""
        
        note_db = Note (
            title=title,
            content=content
        )
    
        db.session.add(note_db)
        db.session.commit()

        return redirect(
            url_for("home")
        )
    return render_template("note_form.html")

@app.route("/edit-note/<int:id>", methods=["GET","POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    print(note)
    if request.method == "POST":
        title = request.form.get("title") or ""
        content = request.form.get("content") or ""

        note.title = title
        note.content = content
        db.session.commit()
        return redirect(
            url_for("home")
        )
    
    return render_template("edit_note.html", note=note)