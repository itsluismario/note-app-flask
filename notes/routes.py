from flask import (
    request, 
    render_template, 
    redirect, 
    url_for, Blueprint, flash)
from models import Note, db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/")
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

@notes_bp.route("/create-note", methods=["GET", "POST"])
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
        flash("Note created", "success")

        return redirect(
            url_for("notes.home")
        )
    return render_template("note_form.html")

@notes_bp.route("/edit-note/<int:id>", methods=["GET","POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        title = request.form.get("title") or ""
        content = request.form.get("content") or ""

        note.title = title
        note.content = content
        db.session.commit()
        return redirect(
            url_for("notes.home")
        )
    
    return render_template("edit_note.html", note=note)

@notes_bp.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(
        url_for("notes.home")
    )

@notes_bp.route("/about")
def about():
    return "Note app"

@notes_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "POST REQUEST!!!! :)", 201
    return "contact page"
