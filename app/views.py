from app import app

from flask import render_template, request, redirect, jsonify, make_response

from datetime import datetime

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
        "name" : "João Victor",
        "bio" : "Dev Python",
        "twitter_handle":"@jefferson123"
    },
    "cesar": {
        "name" : "Cesar Evaristo",
        "bio" : "Dev Java",
        "twitter_handle":"@cesinha"
    },
    "heverton": {
        "name" : "Henrique Everton",
        "bio" : "Suporte",
        "twitter_handle":"@heverton"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)

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
    
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        print("Post")

        if request.files:

            image = request.files["image"]

            print("post image")
            
            print(image)

            return redirect(request.url)

    return render_template("public/upload_image.html")