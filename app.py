from flask import Flask, render_template, request
import requests
import os, glob
from PIL import Image
from bs4 import BeautifulSoup as bs
import colorsys
import pandas as pd
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "/data"
@app.route("/", methods=["GET","POST"])
def index():
    # if request.method == "GET":
    #     return render_template("index.html")

    # print(request.files)
    # pos_imgs = request.files.getlist("positive")
    # neg_imgs = request.files.getlist("negative")
    # all_files = pos_imgs + neg_imgs
    # barrier   = len(pos_imgs)
    # print(all_files)
    # data = {}
    # for i in range(len(all_files)):
    #     filename = secure_filename(all_files[i].filename)
    #     all_files[i].save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    #     print(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    pos = update_the_data("pos", {})
    neg = update_the_data("neg", pos)


    feats = get_all_feats(neg)

    test= update_the_data("test",{})
    my_pics(feats, test)
    return render_template("index.html")

def my_pics(all_features, testdata):
    for data in testdata:
        temp = dict(testdata[data])
        mine = {}
        for point in all_features:
            if point in temp:
                mine[point] = temp[point]
            else:
                mine[point] = 0
        testdata[data] = mine

    df = pd.DataFrame(columns=all_features)

    for img in testdata:
        df.loc[img] = pd.Series(testdata[img])

    newdf = df[[col for col in list(df) if col != "Y"] + ["Y"]]

    newdf.to_csv("test_data.csv")
def get_all_feats(data):
    all_features = set([])

    for img in data:
        for value in data[img]:
            all_features.add(value[0])
    for img in data:
        mine = set([])
        for value in data[img]:
            mine.add(value[0])
        for value in all_features:
            if value not in mine:
                data[img].append( (value, 0) )
    for img in data:
        data[img] = dict(data[img])
    all_features = list(all_features)
    df = pd.DataFrame(columns=all_features)

    for img in data:
        df.loc[img] = pd.Series(data[img])

    newdf = df[[col for col in list(df) if col != "Y"] + ["Y"]]

    newdf.to_csv("final_data.csv")
    return all_features

def update_the_data(path, datadict):
    url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/analyze"
    headers = {
        'Ocp-Apim-Subscription-Key': "<key>",
        'Content-Type': 'application/octet-stream'
    }
    params  = {'visualFeatures': 'Tags,Categories,Color'}
    files = os.listdir("data/"+path)
    data  = {}
    for img in files:
        img_data = open("data/"+path+"/"+img,"rb").read()
        response = requests.post(url,headers=headers,data=img_data,params=params)

        r = json.loads(response.text)

        data_list = []
        try:
            for var in r["categories"]:
                data_list.append( (var["name"], var["score"]) )
        except:
            pass
        try:
            for tag in r["tags"]:
                data_list.append( (tag["name"], tag["confidence"]) )
        except:
            pass
        try:
            data_list.append( ("DF",r["color"]["dominantColorForeground"]) )
        except:
            pass
        try:
            data_list.append( ("DB",r["color"]["dominantColorBackground"]) )
        except:
            pass
        try:
            data_list.append( ("AC", r["color"]["accentColor"]) )
        except:
            pass

        data_list.append( ("Y",  1 if path == "pos" else 0))
        datadict[img] = data_list

    return datadict

if __name__ == "__main__":
    app.debug = True
    app.run()
