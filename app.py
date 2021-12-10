
#importing libraries
import os
import numpy as np
import flask
import pickle
#import pickle
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#creating instance of the class
app=Flask(__name__)
run_with_ngrok(app)

#to tell flask what url shoud trigger the function index()
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/index',methods = ['POST'])
def index():
    return render_template('index.html')


#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,10)
    loaded_model = pickle.load(open("model/insurancerandom.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]
   


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        print(to_predict_list)
        result = ValuePredictor(to_predict_list)
        
        if int(result)==1:
            prediction='Yes He/She Will take the insurance'
        else:
            prediction='NO He/She may not take the insurance'

        print(result)
        from keras import backend as K
        K.clear_session()
            
        return render_template("result.html",prediction=prediction)
if __name__ == "__main__":
        app.run()