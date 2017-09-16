from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

#renders the home page
@app.route('/')
def main():
    return render_template('homepage.html')


#runs when user has chosen a file to upload and clicks "send"
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
        print('hello')

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        print(filename)
        #destination = "/".join(target,filename)
        #print(destination)
        #file.save(destination)

    return render_template("homepage.html")


if __name__ == '__main__':
    app.run(port=4010)
