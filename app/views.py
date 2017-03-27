from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify, make_response
from math import sqrt
from googleads import oauth2
from oauth2client import client
from flask.ext.login import login_user, logout_user, current_user, login_required

import pycurl
import urllib
import json
import io
import requests


# @app.route('/authorize/<provider>')
# def oauth_authorize(provider):
    # # Flask-Login function
    # if not current_user.is_anonymous():
        # return redirect(url_for('index'))
    # oauth = OAuthSignIn.get_provider(provider)
    # return oauth.authorize()

# @app.route('/callback/<provider>')
# def oauth_callback(provider):
    # if not current_user.is_anonymous():
        # return redirect(url_for('index'))
    # oauth = OAuthSignIn.get_provider(provider)
    # username, email = oauth.callback()
    # if email is None:
        # # I need a valid email address for my user identification
        # flash('Authentication failed.')
        # return redirect(url_for('index'))
    # # Look if the user already exists
    # user=User.query.filter_by(email=email).first()
    # if not user:
        # # Create the user. Try and use their name returned by Google,
        # # but if it is not set, split the email address at the @.
        # nickname = username
        # if nickname is None or nickname == "":
            # nickname = email.split('@')[0]

        # # We can do more work here to ensure a unique nickname, if you 
        # # require that.
        # user=User(nickname=nickname, email=email)
        # db.session.add(user)
        # db.session.commit()
    # # Log in the user, by default remembering them for their next visit
    # # unless they log out.
    # login_user(user, remember=True)
    # return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def home():
 return render_template('home.html')
 

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	return render_template('dashboard.html')

@app.route('/_ACOSintervalb', methods=['GET', 'POST'])
def Calculate_ACOS_intervalb():
	clicks = request.args.get('clicks', 0, type=int)
	conversions = request.args.get('conversions', 0, type=int)
	cpc = request.args.get('cpc', 0, type=float)
	totalsales = request.args.get('totalsales', 0, type=float)
	totalspend = request.args.get('totalspend', 0, type=float)
	
	if clicks == 0:
		return 0

	z = 1.96 #1.44 = 85%, 1.96 = 95%
	phat = conversions / clicks
	plow = ((phat + z*z/(2*clicks) - z * sqrt((phat*(1-phat)+z*z/(4*clicks))/clicks))/(1+z*z/clicks))
	phigh = ((phat + z*z/(2*clicks) + z * sqrt((phat*(1-phat)+z*z/(4*clicks))/clicks))/(1+z*z/clicks))
	
		
	ACOSbest = ((cpc - 0.05 * cpc) / ((totalsales / conversions * phigh)))*100
	ACOSworst = ((cpc + 0.05 * cpc) / ((totalsales / conversions * plow)))
	
	ACOSbest = round(ACOSbest, 1)
	
	return jsonify( resultb = ACOSbest)

@app.route('/_ACOSintervalw', methods=['GET', 'POST'])
def Calculate_ACOS_intervalw():
	clicks = request.args.get('clicks', 0, type=int)
	conversions = request.args.get('conversions', 0, type=int)
	cpc = request.args.get('cpc', 0, type=float)
	totalsales = request.args.get('totalsales', 0, type=float)
	totalspend = request.args.get('totalspend', 0, type=float)
	
	if clicks == 0:
		return 0

	z = 1.96 #1.44 = 85%, 1.96 = 95%
	phat = conversions / clicks
	plow = ((phat + z*z/(2*clicks) - z * sqrt((phat*(1-phat)+z*z/(4*clicks))/clicks))/(1+z*z/clicks))
	phigh = ((phat + z*z/(2*clicks) + z * sqrt((phat*(1-phat)+z*z/(4*clicks))/clicks))/(1+z*z/clicks))
	
		
	ACOSbest = ((cpc - 0.05 * cpc) / ((totalsales / conversions * phigh)))
	ACOSworst = ((cpc + 0.05 * cpc) / ((totalsales / conversions * plow)))*100
	
	ACOSworst = round(ACOSworst, 1)
	
	return jsonify(resultw = ACOSworst)

@app.route('/privacypolicy', methods=['GET', 'POST'])
def privacy():
		return render_template('privacypolicy.html')
	
