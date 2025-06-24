from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    role = "admin"
    notes = ["note 1", "note 2", "note 3"]
    return render_template("home.html", role=role, notes=notes)

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
        note = request.form.get("note") or "No encontrado"
        return redirect(
            url_for("confirmation", note=note)
        )
    return render_template("note_form.html")