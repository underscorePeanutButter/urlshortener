from flask import Flask, redirect, render_template, request
import sqlite3
import time

app = Flask(__name__)

@app.route("/")
def homepage():
    db = sqlite3.connect("urls.db")
    
    urls = db.execute("SELECT * FROM Urls")

    urls = urls.fetchall()

    return render_template("home.html", urls=urls)

@app.route("/shorten", methods=["POST"])
def shorten_url():
    db = sqlite3.connect("urls.db")
    form_data = request.form

    command = f"SELECT * FROM Urls WHERE shortened_tag=\"{form_data['shortened_tag']}\""
    tag_instances = db.execute(command)

    if len(tag_instances.fetchall()) != 0:
        return render_template("error.html", message="That tag is already assigned.")

    command = f"INSERT INTO Urls VALUES ('{form_data['shortened_tag']}', '{form_data['full_url']}', {time.time()})"
    db.execute(command)
    
    db.commit()

    return render_template("shortened_result.html", shortened_tag=form_data['shortened_tag'])

@app.route("/url/<tag>")
def redirect_url(tag):
    db = sqlite3.connect("urls.db")

    command = f"SELECT * FROM Urls WHERE shortened_tag=\"{tag}\""
    tag_instances = db.execute(command)

    tag_instances = tag_instances.fetchall()

    if len(tag_instances) == 0:
        return render_template("error.html", message="That tag doesn't exist.")

    return redirect(tag_instances[0][1])
