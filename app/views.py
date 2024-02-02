import os
from app import app

from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort, request, make_response, session, url_for

from datetime import datetime

from werkzeug.utils import secure_filename

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
def index():

    print(app.config["DB_NAME"])

    return render_template("public/index.html")

@app.route("/jinja")
def jinja():

    my_name = "João"

    age = 18

    langs = ["Python", "JavaScript", "Java"]
    
    friends = {
        "Jefferson":19,
        "Willbert":22,
        "Toberson":17,
        "Thalerya":19
    }

    colours = ("Black", "Blue")

    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url
        
        def pull(self):
            return f"Pullin repo {self.name}"
        
        def clone(self):
            return f"Cloning into {self.url}"
        
    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design tutorial",
        url="https://github.com/JoaoVictorOlve/jinja"
    )
        
    def repeat(x, qty):
        return x * qty
    
    date = datetime.utcnow()
    
    my_html = "<h1>THIS IS SOME HTML</h1>"

    return render_template(
        "public/jinja.html", my_name=my_name, age=age,
        langs=langs, friends=friends, colours=colours,
        cool=cool, GitRemote=GitRemote, repeat=repeat,
        my_remote=my_remote, date=date, my_html=my_html
        )

@app.route("/about")
def about():
    return "<h1 style='color: red'>About!</h1>"

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form

        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sign_up.html")

users = {
    "joao": {
        "username" : "joao",
        "bio" : "Dev Python",
        "password": "123",
        "twitter_handle":"@jefferson123"
    },
    "cesar": {
        "username" : "cesar",
        "bio" : "Dev Java",
        "password": "123",
        "twitter_handle":"@cesinha"
    },
    "heverton": {
        "username" : "heverton",
        "bio" : "Suporte",
        "password": "123",
        "twitter_handle":"@heverton"
    }
}

# @app.route("/profile/<username>")
# def profile(username):

#     user = None

#     if username in users:
#         user = users[username]

#     return render_template("public/profile.html", username=username, user=user)

@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"Foo is {foo}, bar is {bar} and baz is {baz}"

@app.route("/json", methods=["POST"])
def json():

    if request.is_json:
        req = request.get_json()

        response = {
            "message" : "JSON received!",
            "name" : req.get("name")
        }

        res = make_response(jsonify(response), 200)

        return res
    
    else:

        res = make_response(jsonify({"message":"No JSON received"}), 400)

        return res
    
@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST",])
def create_entry():

    req = request.get_json()

    print(req)

    res =  make_response(jsonify(req), 200)

    return res

@app.route("/query")
def query():

    if request.args:
        args = request.args

        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())

        return f"(Query) {serialized}", 200

    else:
        return "No query received", 200
    
app.config["IMAGE_UPLOADS"] = r"C:\Users\Computador\Documents\learning-flask\app\static\img\uploads"
app.config["ALLOWED_IMAGE_EXTENSION"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSION"]:
        return True
    else:
        return False
    
def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("file exceeded maximum size")
                return redirect(request)

            image = request.files["image"]

            if image.filename == "":
                print("Image must have name")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            
            print("Image saved")

            return redirect(request.url)

    return render_template("public/upload_image.html")

@app.route("/get-image/<string:image_name>")
def get_image(image_name):

    try:
        return send_from_directory(directory=app.config["CLIENT_IMAGES"], path=image_name, as_attachment=False)

    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<string:file_name>")
def get_csv(file_name):

    try:
        return send_from_directory(directory=app.config["CLIENT_CSV"], path=file_name, as_attachment=True)

    except FileNotFoundError:
        abort(404)

@app.route("/get-reports/<path:path>")
def get_report(path):

    try:
        return send_from_directory(directory=app.config["CLIENT_REPORTS"], path=path, as_attachment=True)

    except FileNotFoundError:
        abort(404)

@app.route("/cookies")
def cookies():

    res = make_response("Cookies", 200)

    cookies = request.cookies

    flavor = cookies.get("flavor")
    choc_type = cookies.get("chocolate type")
    chewy = cookies.get("chewy")
    brand = cookies.get("brand")

    print(flavor, choc_type, chewy, brand)

    print(flavor)

    res.set_cookie(
        "flavor",
        value="chocolate chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        samesite=None
        )
    
    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")

    return res

app.config["SECRET_KEY"] = "IUTeyRP4dqWMx6C925Zthg"

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]
        
        if not password == user["password"]:
            print("Password is wrong!")
            return redirect(request.url)
        
        else:
            session["USERNAME"] = user["username"]
            session["PASSWORD"] = user["password"]
            print("User added to session")
            return redirect(url_for("profile"))

    return render_template("public/sign_in.html")

@app.route("/profile")
def profile():

    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for('sign_in'))
    
@app.route("/sign-out")
def sign_out():
    session.pop('USERNAME', None)
    session.pop('PASSWORD', None)
    return redirect(url_for('sign_in'))