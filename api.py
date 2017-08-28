from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from firebase_token_generator import create_token
import os
from random import *
import json
import sendgrid
from sendgrid.helpers.mail import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solidareasy.sqlite3'
app.config['SECRET_KEY'] = 'random string'

db = SQLAlchemy(app)

class videoValidate(db.Model):
	id = db.Column('video_id', db.Integer, primary_key = True)
	email = db.Column(db.String(100))
	name = db.Column(db.String(80))
	token = db.Column(db.String(120), unique = True)

	def __init__(self, email, name, token):
		self.email = email
		self.name = name
		self.token = token

@app.route('/token', methods = ['GET', 'POST']) #for generate one token
def token():
  	auth_payload = {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"}
  	options = {"admin": True}
  	token = create_token("<AIzaSyARXSs-bBjRg4FGya6yV7opSEaHibywSj0>", auth_payload, options)
	return token

@app.route('/token/check', methods=['GET','POST']) #for add to bd
def checkToken():
	if request.method == 'POST':	
		if not request.form['email'] or not request.form['name'] or not request.form['token']:
			flash('Please enter all the fields', 'error')
		# videoT = token()
		else:	
			video = videoValidate(request.form['email'], request.form['name'], request.form[token()])
			db.session.add(video)
			db.session.commit()
			sendMail()
	return render_template('new.html')


@app.route('/', methods = ['GET', 'POST'])
def requesToken():
		videoValidate = token()
		db.session.add(videoValidate)
		db.session.commit()

@app.route('/sendmail', methods=['POST']) #for send one email with bd add
def sendMail():
	testC()
	token()
	sg = sendgrid.SendGridAPIClient(apikey='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')
	data = {
	"personalizations": [
	    {
	      "to": [
	        {
	          "email": "lucasfonmiranda@gmail.com"
	        }
	      ],
	      "subject": "Sending with SendGrid is Fun"
	    }
	  ],
	  "from": {
	    "email": "contato@solidareasy.com"
	  },
	  "content": [
	    {
	      "type": "text/html",
	      "value": ("Token: " + token()) 
	    }
	  ]
	}
	video = videoValidate(request.form['email'], request.form['name'] ,request.form[testC()])
	db.session.add(video)
	db.session.commit()
	response = sg.client.mail.send.post(request_body=data)
	return jsonify({"status": response.status_code})

def testC():
	testa = randrange(100,1000)
	return testa
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)