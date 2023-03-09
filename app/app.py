from flask import Flask, redirect, url_for, render_template, request, flash
# from admin.pages import pages
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "Not So Secret Key"
# app.register_blueprint(pages, url_prefix="/home")

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'kanban.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Kanban(db.Model):
    __tablename__ = 'kanban'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))
    is_done = db.Column(db.Boolean, default=False)

    def __init__(self, title, content, is_done):
            self.title= title
            self.content=content
            self.is_done = is_done
    
with app.app_context():
    db.create_all()


@app.route("/")
# def login():
#     return render_template("login.html")
def home():
    kanbans = Kanban.query.all()
    return render_template("home.html", kanbans=kanbans)

@app.route("/addnote")
def show():
     return render_template("add.html")

@app.route("/show/<id>/", methods=["GET", "POST"])
def details(id):
     my_data = Kanban.query.get(id)
     return render_template("edit.html", kanban=my_data)

@app.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
         
         title = request.form["title"]
         content = request.form["content"]
         my_data = Kanban(title=title, content=content, is_done=False)
         db.session.add(my_data)
         db.session.commit()
         
         flash("Kanban Added!")
         return redirect(url_for('home'))

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Kanban.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.content = request.form['content']

        db.session.commit()
        flash("Data Updated Successfully")

        return redirect(url_for('home'))

@app.route('/done/<id>', methods=["GET", "POST"])
def status(id):
     if request.method == 'POST':
          my_data = Kanban.query.get(id)
          my_data.is_done = not my_data.is_done
          db.session.commit()
          flash("Data Marked as Done!")

          return redirect(url_for('home'))

#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Kanban.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Data Employee Deleted Successfully")

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
