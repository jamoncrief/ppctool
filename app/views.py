from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify, make_response
from math import sqrt
from googleads import oauth2
from oauth2client import client

import pycurl
import urllib
import json
import io
import requests
		
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '603499396792-bl8scdsmlncnjiff8l61f0e8l6li3din.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 't2hCcF5NCR5Iq3sewc1T67aQ'
REDIRECT_URI = '/dashboard'  # one of the Redirect URIs from Google APIs console
 
SECRET_KEY = 'DkqQvXDQifThH7_xWNgZoA'
DEBUG = True

app.secret_key = SECRET_KEY
oauth = OAuth()
 
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
 
@app.route('/', methods=['GET', 'POST'])
def home():
	
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
 
    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
 
    return res.read()
 return render_template('home.html')
 
@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)
 
 
 
@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('home'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

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
	
