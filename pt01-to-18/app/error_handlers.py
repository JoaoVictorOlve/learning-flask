from app import app

from flask import render_template, request

@app.errorhandler(404)
def not_found(e):

    print(e)
    return render_template("public/error_templates/404.html")

@app.errorhandler(500)
def server_error(e):

    app.logger.error("Server error")
    return render_template("public/error_templates/500.html")

@app.errorhandler(403)
def server_error(e):

    app.logger.error("Forbidden")
    return render_template("public/error_templates/403.html")
