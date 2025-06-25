from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask, 
    request, 
    render_template, 
    redirect, 
    url_for)
from config import Config
from models import Note

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

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

@app.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(
        url_for("home")
    )

@app.route("/about")
def about():
    return "Note app"

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "POST REQUEST!!!! :)", 201
    return "contact page"
