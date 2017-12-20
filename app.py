from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory, send_file, jsonify
import pickle as pkl
import os
from mongoUtil import mongoUtil
import json

app = Flask(__name__)
app.secret_key = os.urandom(12)
util = mongoUtil()


@app.route('/',methods=['GET','POST'])
def home():
    try:
        #This checks if the request is a POST request.
        if request.method == 'POST':
            #This gets the cif number that the user is searching for
            cif = request.form['cifSearch']
            #This uses the Mongo Util class to search and get the cif info in a list format
            li = list(util.get_cif_info(cif))
            #This will parse the Json dictionary
            ret = parseJson(dict(li[0]))
            try:
                #This will only run if there is survey data.
                survey_data = li[0]['survey']
                nps_score = survey_data['nps']
            except:
                nps_score = None
                print("No Survey Data")
            #If there is no NPS score then we simply return the no results page
            if nps_score is None:
                return render_template('index.html', cifNumber=cif,npsScore=0,no_results="True",jsondict="{}")
            return render_template('index.html', cifNumber=cif,npsScore=nps_score,no_results="False",jsondict=dict(li[0]))
    except:
        #This case runs when there is no CIF in the database for the searched CIF number
        errorS = "Error Occured, no CIF found."
        return render_template('index.html', cifNumber='',npsScore=0,no_results="True",jsondict="{}",errorString=errorS,errorOccured='True')
    return render_template('index.html', cifNumber='',npsScore=0,no_results="True",jsondict="{}")

    
#This function parses the json and returns the json dictionary
def parseJson(json_dict):
    returnThis = jsonify(json_dict)
    #returnThis = json.dumps(json_dict, sort_keys=True, indent=4)
    return returnThis


#Test CIFS
# F3E2A6390D273A13B61A925335A7490B   nps 10
# 500C71E28DF02FB637F5649DB4B4CB9D   nps 6
# 9EBA762DE297792E74BA277EC7658E6A   nps 0
# 293A0708F90AED21EF0CA0101C438F73   nps 8

