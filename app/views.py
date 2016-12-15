from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify, make_response
from math import sqrt


						
@app.route('/', methods=['GET', 'POST'])
def home():
		return render_template('home.html')

@app.route('/privacypolicy', methods=['GET', 'POST'])
def privacy():
		return render_template('privacypolicy.html')
		
@app.route('/count', methods=['GET', 'POST'])
def count():
	if 'count' in request.cookies:
			flash('Create an account to continue using the PPC ACOS Interval Tool')
			return render_template('signup.html')
	else:
		response = make_response(redirect(url_for('count')))
		response.set_cookie('count','1')
		flash('cookie created')
		return render_template('home.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # # Here we use a class of some kind to represent and validate our
    # # client-side form data. For example, WTForms is a library that will
    # # handle this for us, and we use a custom LoginForm to validate.
    # form = LoginForm()
    # if form.validate_on_submit():
        # # Login and validate the user.
        # # user should be an instance of your `User` class
        # login_user(user)

        # flask.flash('Logged in successfully.')

        # next = flask.request.args.get('next')
        # # is_safe_url should check if the url is safe for redirects.
        # # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
            # return flask.abort(400)

        # return flask.redirect(next or flask.url_for('index'))
    # return flask.render_template('login.html', form=form)
	
	
#@app.route('/setcount', methods=['GET', 'POST'])
#def setcount():
#	count = request.get.

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
	
