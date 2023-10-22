from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)


@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("all_notes.html", notes=notes)

@app.route("/note/<int:id>", methods=["GET", "POST"])
def note_details(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        note.title = request.form["title"]
        note.content = request.form["content"]
        db.session.commit()
        return redirect("/")

    return render_template("note.html", note=note)

@app.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect("/")
    else: 
        return render_template("create_note.html")
    
@app.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
