from app.model import db, Kanban
from flask import request, redirect, url_for,flash, render_template, session
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity, get_jwt, get_csrf_token
from flask_jwt_extended import unset_jwt_cookies
import uuid

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies

from datetime import datetime
from datetime import timedelta
from datetime import timezone

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix="/admin")

@admin.after_request
def refresh_expiring_jwts(response):
    "refreshing JWT token that gonna expires"
    try:
        exp_timestamp = get_jwt()["exp"]
        jwt_cred = get_jwt()
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            additional_claims = {"uuid":jwt_cred["uuid"]}
            access_token = create_access_token(identity=get_jwt_identity(), 
            additional_claims=additional_claims)
        return response
    except (RuntimeError, KeyError):
        response = redirect(url_for("auth.index"))
        # Case where there is not a valid JWT. Just return the original response
        return response

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
         public_id = claims["uuid"]
         kanban_id = str(uuid.uuid4)
         title = request.form["title"]
         content = request.form["content"]
         my_data = Kanban(kanban_id = kanban_id ,public_id = public_id, title=title, content=content, is_done=False)
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

@admin.route('/done/<kanban_id>', methods=["GET", "POST"])
@jwt_required(locations = ["cookies"])
def status(kanban_id):
     if request.method == 'POST':
          my_data = Kanban.query.get(kanban_id)
          my_data.is_done = not my_data.is_done
          db.session.commit()
          flash("Data Marked as Done!")

          return redirect(url_for('admin.home'))

#This route is for deleting our employee
@admin.route('/delete/<kanban_id>/', methods = ['GET', 'POST'])
@jwt_required(locations = ["cookies"])
def delete(kanban_id):
    my_data = Kanban.query.get(kanban_id)
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