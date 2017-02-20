from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify, make_response
from math import sqrt

import pycurl
import urllib
import json
import io
import requests
from furl import furl
from requests_oauthlib import OAuth2Session

						
@app.route('/', methods=['GET', 'POST'])
def home():
		return render_template('home.html')
		
@app.route('/privacypolicy', methods=['GET', 'POST'])
def privacy():
		return render_template('privacypolicy.html')
		
# @app.route('/count', methods=['GET', 'POST'])
# def count():
	# if 'count' in request.cookies:
			# flash('Create an account to continue using the PPC ACOS Interval Tool')
			# return render_template('signup.html')
	# else:
		# response = make_response(redirect(url_for('count')))
		# response.set_cookie('count','1')
		# flash('cookie created')
		# return render_template('home.html')
		

 
@app.route('/login', methods=['GET', 'POST'])
def loginwithamazon():
	return render_template('login.html')
	
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	
	#r=requests.get("https://ppctool.herokuapp.com/dashboard")
	#authcode=r.headers.get('access_token')
	
	#fetch authorization token after receiving the authorization code post-LwA
	#token = oauth.fetch_token(
        #the amazon oauth2 token endpoint
	#'https://api.amazon.com/auth/o2/token',
        #
        #grant_type=authorization_code,
	#code=#figureouthowtoputauthcodefromurlhere,
	#redirect_uri='https://ppctool.herokuapp.com/dashboard',
	#client_id='AKIAI5PZL5WXNSPYLZTA',
	#client_secret='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'
	#)
	

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
	
