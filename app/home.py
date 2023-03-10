from app.model import db, Kanban
from flask import request, redirect, url_for,flash, render_template, session
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity, get_jwt, get_csrf_token
from flask_jwt_extended import unset_jwt_cookies

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix="/admin")


@admin.route("/")
@jwt_required(locations = ["cookies"])
def home():
    user = get_jwt_identity()
    uuid = get_jwt()
    kanbans = Kanban.query.filter_by(public_id = uuid['uuid'])
#     kanbans = Kanban.query.all()
    return render_template("home.html", kanbans=kanbans, user=user)

@admin.route("/addnote")
@jwt_required(locations = ["cookies"])
def addnote():
     user = get_jwt_identity()
     return render_template("add.html", user=user)

@admin.route("/show/<id>/", methods=["GET", "POST"])
@jwt_required(locations = ["cookies"])
def details(id):
     my_data = Kanban.query.get(id)
     return render_template("edit.html", kanban=my_data)

@admin.route("/insert", methods=["POST"])
@jwt_required(locations = ["cookies"])
def insert():
    if request.method == "POST":
         claims = get_jwt()
         uuid = claims["uuid"]
         title = request.form["title"]
         content = request.form["content"]
         my_data = Kanban(public_id = uuid, title=title, content=content, is_done=False)
         db.session.add(my_data)
         db.session.commit()
         
         flash("Kanban Added!")
         return redirect(url_for('admin.home'))

#this is our update route where we are going to update our employee
@admin.route('/update', methods = ['GET', 'POST'])
@jwt_required(locations = ["cookies"])
def update():

    if request.method == 'POST':
        my_data = Kanban.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.content = request.form['content']

        db.session.commit()
        flash("Data Updated Successfully")

        return redirect(url_for('admin.home'))

@admin.route('/done/<id>', methods=["GET", "POST"])
@jwt_required(locations = ["cookies"])
def status(id):
     if request.method == 'POST':
          my_data = Kanban.query.get(id)
          my_data.is_done = not my_data.is_done
          db.session.commit()
          flash("Data Marked as Done!")

          return redirect(url_for('admin.home'))

#This route is for deleting our employee
@admin.route('/delete/<id>/', methods = ['GET', 'POST'])
@jwt_required(locations = ["cookies"])
def delete(id):
    my_data = Kanban.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Data Employee Deleted Successfully")

    return redirect(url_for('admin.home'))


@admin.route("/logout", methods=["POST"])
@jwt_required(locations = ["cookies"])
def logout():
    response = redirect(url_for("auth.index"))
    unset_jwt_cookies(response)
    return response