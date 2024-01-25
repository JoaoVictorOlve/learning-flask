from app import app

from flask import render_template

@app.route("/")
def index():
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

    return render_template(
        "public/jinja.html", my_name=my_name, age=age,
        langs=langs, friends=friends, colours=colours,
        cool=cool, GitRemote=GitRemote, repeat=repeat,
        my_remote=my_remote
        )

@app.route("/about")
def about():
    return "<h1 style='color: red'>About!</h1>"