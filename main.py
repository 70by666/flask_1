import os
import psycopg2
from flask import Flask, make_response, render_template, request, flash, session, redirect, url_for, abort, g
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from database import PgDataBase
from userlogin import UserLogin
from forms import LoginForm


app = Flask(__name__)

load_dotenv(find_dotenv())

# config
SECRET_KEY = os.getenv("SECRET_KEY")
MAX_CONTENT_LENGTH = 1024 * 1024 * 5

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(__name__)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

navbar = [{"title": "Home", "url": "/"},
          {"title": "Dogs", "url": "/dogs"},
          {"title": "Feedback", "url": "/feedback"}]


# index
@app.route("/")
def index():
    # postlist = dbase.all()
    postlist = dbase_pg.get_post_list()
    
    return render_template("index.html", title="Main page",
                                         navbar=navbar, 
                                         postlist=reversed(postlist))


# dogslist
# @app.route("/dogs")
# def dogs():
#     dogs_list = dbase_pg.get_dog_id()
#     if not dogs_list:
#         return ""
    
#     return render_template("dogs.html", title="Dogs", 
#                                         navbar=navbar,
#                                         dogs_list=dogs_list)


# @app.route("/getdog<int:dog_id>")
# @login_required
# def getdog(dog_id):
#     img = dbase_pg.get_dog(dog_id)[0]
#     if not img:
#         return ""

#     h = make_response(img.tobytes())
#     h.headers['Content-Type'] = 'image'
    
#     return h


@app.route("/adddog", methods=["POST", "GET"])
@login_required
def adddog():
    abort(404)
    # if not current_user.get_id() == "1":
    #     abort(401)
        
    # if request.method == "POST":
    #     file = request.files["file"]
    #     if file:
    #         try:
    #             img = file.read()
    #             result = dbase_pg.add_dog(img)
    #             if not result:
    #                 flash("Error", category="danger")
            
    #             flash("Success", category="success")
    #         except FileNotFoundError as Ex:
    #             print(Ex)
    #     else:
    #         flash("Error", category="danger")
            
    # return render_template("adddog.html", navbar=navbar, title="Add dog")


# feedback
@app.route("/feedback", methods=["POST", "GET"])
def feedback():
    if request.method == "POST":
        check_username_feedback = all(i.isalpha() or i.isalnum() or i == "_" for i in request.form["username_feedback"])
        if check_username_feedback and 4 < len(request.form["username_feedback"]) < 32:
            flash("Successfully sent", category="success")
        else:
            flash("Error", category="danger")

    return render_template("feedback.html", title="Feedback", 
                                            navbar=navbar)


# news
@app.route("/addnews", methods=["POST", "GET"])
@login_required
def addnews():
    if not current_user.get_id() == "1":
        abort(401)
        
    if request.method == "POST":
        # entry = CreateTable(request.form["email"], 
        #                     request.form["post"], 
        #                     request.form["urlimg"], 
        #                     request.form["titlepost"])
        # db.session.add(entry)
        # db.session.commit()
        file = request.files["file"]
        if file:
            try:
                img = file.read()
                result = dbase_pg.add_post(request.form["titlepost"], 
                                           img,
                                           request.form["text"])
                if not result:
                    flash("Error", category="danger")
            
                flash("Success", category="success")
            except FileNotFoundError as Ex:
                print(Ex)
        else:
            flash("Error", category="danger")
        
    return render_template("addnews.html", title="Add news", 
                                           navbar=navbar)


@app.route("/newspost/<int:id_post>")
@login_required
def newspost(id_post):
    # post = dbase.filter_by(id=id_post).first()
    post = dbase_pg.get_post(id_post)
    if not post:
        abort(404)
        
    return render_template("newspost.html", title=post[1], 
                                            navbar=navbar, 
                                            post=post)


@app.route("/postimg/<int:id_post>")
@login_required
def postimg(id_post):
    img = dbase_pg.get_post_img(id_post)[0]
    if not img:
        return ""

    h = make_response(img.tobytes())
    h.headers['Content-Type'] = 'image'
    
    return h


# log and reg
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase_pg.get_user_by_email(form.email.data)
        if user and check_password_hash(user[3], form.password.data):
            userlogin = UserLogin().create(user)
            sv = form.save.data
            login_user(userlogin, remember=sv)
            return redirect(request.args.get("next") or url_for("profile"))
        
        flash("Error", category="danger")
        
    return render_template("login.html", title="Log in", 
                                         navbar=navbar,
                                         form=form)
    
    # if request.method == "POST":
    #     user = dbase_pg.get_user_by_email(request.form["email"])
    #     if user and check_password_hash(user[3], request.form["password"]):
    #         userlogin = UserLogin().create(user)
    #         sv = True if request.form.get("save") else False
    #         login_user(userlogin, remember=sv)
    #         return redirect(request.args.get("next") or url_for("profile"))
        
    #     flash("Error", category="danger")
        
    # return render_template("login.html", title="Log in", 
    #                                      navbar=navbar) 


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form["name"]) > 2 and len(request.form["password"]) > 2 and \
                request.form["password"] == request.form["password2"]:
            hash = generate_password_hash(request.form["password"])
            result = dbase_pg.add_user(request.form["name"], 
                                       request.form["email"], 
                                       hash)
            if result:
                flash("Successfully sent", category="success")
                return redirect(url_for("login"))
            else:
                flash("Error", category="danger")
        else:
            flash("Error", category="danger")
            
    return render_template("register.html", title="Register", 
                                            navbar=navbar)


# users
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase_pg)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title=f"Profile {current_user.get_id()}", 
                                           navbar=navbar)


@app.route("/logout")
def logout():
    logout_user()
    flash("Success", category="success")
    
    return redirect(url_for("login"))


# ava
@app.route("/ava")
@login_required
def ava():
    img = current_user.get_ava(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    
    return h


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                result = dbase_pg.update_ava(img, current_user.get_id())
                if not result:
                    flash("Error", category="danger")
            
                flash("Success", category="success")
            except FileNotFoundError as Ex:
                print(Ex)
        else:
            flash("Error", category="danger")
            
    return redirect(url_for("profile"))


# errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Ooops 404", 
                                       navbar=navbar)


@app.errorhandler(401)
def unauthorized(error):
    return render_template("401.html", title="Ooops 401", 
                                       navbar=navbar)


# db
# class CreateTable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(80), nullable=False)
#     post = db.Column(db.String(120), nullable=False)
#     time = db.Column(db.String(120), nullable=False)
#     urlimg = db.Column(db.String, nullable=False)
#     titlepost = db.Column(db.String(120), nullable=False)

#     def __init__(self, email, post, urlimg, titlepost):
#         self.email = email
#         self.post = post
#         self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         self.urlimg = urlimg
#         self.titlepost = titlepost


def connect_db():
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DB_NAME") 
    )
    
    return conn


def create_tb():
    '''create table'''
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().execute(f.read())
        
    db.commit()
    db.close()


def get_db():
    '''connection, if not'''
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
        
       
@app.before_request
def before_request():
    # global dbase
    # dbase = CreateTable.query
    
    global dbase_pg
    db = get_db()
    dbase_pg = PgDataBase(db)

     
# run
if __name__ == "__main__":
    app.run(debug=False)
