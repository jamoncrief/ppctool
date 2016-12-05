from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify
from math import sqrt
						
@app.route('/', methods=['GET', 'POST'])
def home():
	#form = DataForm()
	#if form.validate_on_submit():
	#	clicks = form.Data1.data
	#	conversions = form.Data2.data
	#	cpc = form.Data3.data
	#	totalsales = form.Data4.data
	#	return render_template('home.html')
	return render_template('home.html')#, form=form)
	
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
	
	
if __name__ == '__main__':
    app.run(debug=True)
