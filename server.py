from flask import Flask, redirect, url_for, session, request, render_template
import sqlite3 as db
import json
from farm_crud import *

app=Flask(__name__,template_folder="template")


@app.route("/")
def default_page():
	gardens=garden_settings.list_gardens()
	gd1=json.loads(gardens)
	return render_template("analytics.html",gardens=gd1,total=len(gd1['data']))

@app.route("/list-gardens")
def api_list_page():
	gardens=garden_settings.list_gardens()
	gd1=json.loads(gardens)
	return gd1


@app.route("/analytics")
def json_analytics_page():
	dump={"light_intensity":"","humidity_level":"","temperature_level":"","soil_moisture":"","soil_watering_cycles":"","remaining_cycles":""}
	gc=garden_settings(request.args.get("garden"))
	dump['garden']=request.args.get("garden")
	inf0=json.loads(gc.get_garden_info())
	infx=inf0['data']
	if len(infx) >0:
		inf=infx[0]
		
		dump['soil_watering_cycles']=inf['watering_interval']
		live_data=live_log(request.args.get("garden"))
		hay01=json.loads(live_data.get_garden_live())
		hay0=hay01['data']
		if len(hay0) >0:
			hay=hay0[0]			
			moisture=hay['soil_moisture']
			humidity=hay['humidity_level']
			dump['garden']=hay['garden']
			temperature=hay['temperature_level']
			dump['humidity_level']=str(humidity)+"/"+str(inf['normal_humidity'])
			dump['soil_moisture']=str(moisture)+"/"+str(inf['normal_moisture_threshhold'])
			dump['temperature_level']=str(temperature)+"/"+str(inf['temperature'])
		fr=farm_crud(request.args.get("garden"))
		res0=json.loads(fr.get_garden_details_now())
		if len(res0) >0:
			res=res0
			lr=res['data']
			if len(lr) >0:
				dump['last_irrigated']=lr[0]['last_watering_time']
			else:
				dump['last_irrigated']="no data"
		else:
			dump['last_irrigated']="no data"
	return json.dumps(dump)

@app.route("/api")
def api_page():

	return json.dumps({"date":"","garden":"1", "last_watering_time":"","next_sheduled_time":"","last_rained":"","current_temperature":"","humidity":"","uv":"","soil_moisture":"","nutients":[{"type":""}]})

@app.route("/logout")
def logout_page():
	session.pop('username',None)
	session.pop('password',None)
	return redirect(url_for('default_page'))


@app.route("/login",methods=["POST","GET"])
def login_page():
	status=""
	if request.method=="POST":
		username=request.form["username"]
		password=request.form["password"]
		lg=login()
		if lg.row_count >0:
			session['username']=username
			session['password']=password
			return redirect(url_for('new_garden_page'))
		else:
			status="<div class='alert alert-warning'>You entered incorrect username/password. please try again.</div>"
			return render_template("login.html",status=status)
	else:
		return render_template("login.html",status=status)

@app.route("/add-garden",methods=["POST","GET"])
def new_garden_page():
	status=""
	if request.method=="POST":
		garden=request.form["garden"]
		address=request.form["address"]
		latitude=request.form["latitude"]
		longitude=request.form["longitude"]
		length=request.form["length"]
		width=request.form["width"]
		temperature=request.form["temperature"]
		amount_of_water_per_interval=request.form["amount_of_water_per_interval"]
		normal_humidity=request.form["normal_humidity"]
		normal_moisture_threshhold=request.form["normal_moisture_threshhold"]
		watering_interval=request.form["watering_interval"]
		crops=request.form["crops"]
		selected_watering_option=request.form["selected_watering_option"]
		other_info=request.form["other_info"]
		gi=garden_settings()
		status=gi.register_garden(garden,address, latitude,longitude,length,temperature,width,amount_of_water_per_interval,normal_humidity,normal_moisture_threshhold,crops,watering_interval,selected_watering_option,other_info)
		dec=json.loads(status)
		status="<div class='alert alert-info'>"+str(dec['message'])+"</div>"
	return render_template("new-garden.html",status=status)


@app.route("/irrigate-feedback",methods=["POST","GET"])
def irrigate():
	status=""
	response="Failed to irrigate >check settings/ sufficient moisture in the soil!"
	param0=request.args.get("irrigate")
	garden=request.args.get("garden")
	service=request.args.get("service")
	soil_moisture_level=request.args.get("initial-moisture-level")
	
	if request.method=="GET" and param0!=None and garden!=None:
		fc=farm_crud(garden)
		st=json.loads(fc.get_watering_info(soil_moisture_level))
		if st["should_water_now"]=="yes":
			current_temperature=request.args.get("current_temperature")
			humidity=request.args.get("humidity")
			uv_radiation=request.args.get("uv_radiation")
			soil_moisture=request.args.get("soil_moisture")
			amount_of_water=request.args.get("amount_of_water")
			nutrients=request.args.get("nutrients")
			already_irrigated=request.args.get("already_irrigated")
			response=fc.start_watering(current_temperature,humidity,uv_radiation, soil_moisture,amount_of_water,nutrients,already_irrigated)
		else:
			response=st["message"]
	if request.method=="GET" and service=="realtime-data" and garden!=None:
		#realtime data upload here
		ll=live_log()
		response=ll.upload_data(request.args.get("light_intensity"),request.args.get("humidity_level"),request.args.get("temperature_level"),request.args.get("soil_moisture"),request.args.get("timestamp_now"))		
	return response

if __name__=="__main__":
	app.run(port="4050", debug=True)