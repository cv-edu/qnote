from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import os
import cv2
import matplotlib.pyplot as plt
import urllib
import urllib.request
import numpy as np
import pyimgur



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

#pyimgur
client_id = "12a16f29537f608"
client_key = "42279ff7636c3174f6e4c0dc75092372e3940656"
im = pyimgur.Imgur(client_id)

#renders the home page
@app.route('/')
def main():
    return render_template('homepage.html')



#runs when user has chosen a file to upload and clicks "send"
@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(os.path.join(APP_ROOT, 'images/'), file.filename))
    
    print(file.filename)
    filepath = os.path.join(os.path.join(APP_ROOT, 'images/'))+file.filename
    print(filepath)
    print(file)
    
    image_link = upload_file(filepath)
    process(image_link)

    return main()
    
    #read(image.link)
    # target = os.path.join(APP_ROOT, 'images/')
    # print(target)
    # 
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    #     print('hello')
    # 
    # for file in request.files.getlist("file"):
    #     print(file)
    #     filename = file.filename
    #     print(filename)
    #print(file.filename)
    #read('https://i0.wp.com/thepostmansknock.com/wp-content/uploads/2017/03/1cursive_worksheet-12-of-15.jpg')


def upload_file(filepath):
    print('hello')
    image = im.upload_image(filepath)
    print(image.link)
    return image.link

    return render_template("homepage.html")
    #     #destination = "/".join(target,filename)
    #     #print(destination)
    #     #file.save(destination)


contoured = []
approx_contours = []

def read(filename):
    #cv2.imwrite('images', filename)
    resp = urllib.request.urlopen(filename)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    #img = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    global contoured
    contoured = gray.copy()
    cv2.drawContours(contoured, contours, -1, color=(0, 255, 0), thickness=10)

    largest = max(contours, key=cv2.contourArea)

    global approx_contours
    approx_contours = []
    for c in filter(lambda cnt: cnt is not largest, contours):
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        if len(approx) is 4:
            approx_contours.append(approx)

    min_area = 5e4
    approx_contours = [c for c in approx_contours if cv2.contourArea(c) > min_area]

    contoured = gray.copy()
    cv2.drawContours(contoured, approx_contours, -1, color=(127, 0, 127), thickness=7)
    
def save():
    for i, cnt in enumerate(approx_contours):
        x, y, w, h = cv2.boundingRect(cnt)

        img = contoured[y:y+h, x:x+w]
        plt.imsave(f"contour-{i+1}.png", img);


def process(filename):
    read(filename)
    save()


if __name__ == '__main__':
    app.run(port=4010)
