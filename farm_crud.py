import sqlite3 as con
import json
from datetime import date,datetime
import os

class config:
	def __init__(self,params=[]):
		self.db_directory=os.path.join(os.getcwd(),"magochi-database")
	def db_farm_crud(self):
		return os.path.join(self.db_directory,"farm_crud.db")
	def db_data_logs(self):
		return os.path.join(self.db_directory,"data_logs.db")


class login:
	def __init__(self,username,password):
		q="select *from users where username=? and password=?"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		cur=c.cursor()
		cur.execute(q,(username,password))
		data=cur.fetchall()
		c.close()
		self.row_count=len(data)
class garden_settings:
	def __init__(self,garden=""):
		self.garden=garden
		self.watering_options=["with_interval","when_soil_runs_below_set_moisture_content","dont_irrigate"]
	def register_garden(self,garden,address, latitude,longitude,length,temperature,width,amount_of_water_per_interval,normal_humidity,normal_moisture_threshhold,crops,watering_interval,selected_watering_option,other_info):
		q="insert into garden_settings(garden,address, latitude,longitude,length,temperature,width,amount_of_water_per_interval,normal_humidity,normal_moisture_threshhold,crops,watering_interval,selected_watering_option,other_info) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		cur=c.cursor()
		cur.execute(q,(garden,address, latitude,longitude,length,temperature,width,amount_of_water_per_interval,normal_humidity,normal_moisture_threshhold,crops,watering_interval,selected_watering_option,other_info))
		c.commit()
		cur.close()
		c.close()
		return json.dumps({"message":"success. garden added."})
	def get_garden_info(self):
		q="select * from garden_settings where garden=?"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		c.row_factory=con.Row
		cur=c.cursor()
		
		cur.execute(q,(self.garden,))
		data=cur.fetchall()
		f={}
		for d in data:
			f['garden']=d['garden']
			f['latitude']=d['latitude']
			f['longitude']=d['longitude']
			f['length']=d['length']
			f['temperature']=d['temperature']
			f['width']=d['width']
			f['amount_of_water_per_interval']=d['amount_of_water_per_interval']
			f['normal_humidity']=d['normal_humidity']
			f['normal_moisture_threshhold']=d['normal_moisture_threshhold']
			f['crops']=d['crops']
			f['watering_interval']=d['watering_interval']
			f['selected_watering_option']=d['selected_watering_option']
			f['other_info']=d['other_info']

		c.close()
		return json.dumps({"garden":self.garden,"data":[f]})
	def list_gardens():
		q="select * from garden_settings"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		c.row_factory=con.Row
		cur=c.cursor()
		cur.execute(q)
		datas=cur.fetchall()
		data=[]
		for d in datas:
			f={}
			f['garden']=d['garden']
			f['latitude']=d['latitude']
			f['longitude']=d['longitude']
			f['length']=d['length']
			f['temperature']=d['temperature']
			f['width']=d['width']
			f['amount_of_water_per_interval']=d['amount_of_water_per_interval']
			f['normal_humidity']=d['normal_humidity']
			f['normal_moisture_threshhold']=d['normal_moisture_threshhold']
			f['crops']=d['crops']
			f['watering_interval']=d['watering_interval']
			f['selected_watering_option']=d['selected_watering_option']
			f['other_info']=d['other_info']
			data.append(f)
		c.close()
		return json.dumps({"data":data})


class live_log: #before watering/after watering per second
	def __init__(self,garden=""):
		self.garden=garden
		self.timestamp_now=str(datetime.now())
	def upload_data(self,light_intensity,humidity_level,temperature_level,soil_moisture,timestamp_now):
		q="insert into live_log(garden,light_intensity,humidity_level,temperature_level,soil_moisture,timestamp_now) values(?,?,?,?,?,?)"
		conf=config()
		c=con.connect(conf.db_data_logs())
		cur=c.cursor()
		cur.execute(q,(self.garden,light_intensity,humidity_level,temperature_level,soil_moisture,self.timestamp_now))
		c.commit()
		cur.close()
		c.close()
		return json.dumps({"message":str(garden)+"'s data sent!"})

	def get_garden_live(self):
		q="select *from live_log where garden=?"
		conf=config()
		c=con.connect(conf.db_data_logs())
		c.row_factory=con.Row
		cur=c.cursor()
		cur.execute(q,(self.garden,))
		datas=cur.fetchall()
		data=[]
		for d in datas:
			f={}
			f['light_intensity']=d['light_intensity']
			f['humidity_level']=d['humidity_level']
			f['temperature_level']=d['temperature_level']
			f['soil_moisture']=d['soil_moisture']
			f['timestamp_now']=d['timestamp_now']
			f['garden']=d['garden']
			data.append(f)			
		return json.dumps({"garden":self.garden,"data":data})

class farm_crud:
	def __init__(self, garden=""):
		super(farm_crud, self).__init__()
		self.garden = garden
		self.date=str(date.today())
		self.timestamp_now=str(datetime.now())
		self.farm_settings=garden_settings(self.garden)
		self.next_sheduled_time=self.timestamp_now
		self.last_rained="no"

	def add_data(self,date,garden,last_watering_time,next_sheduled_time,last_rained,current_temperature,humidity,uv_radiation, soil_moisture,nutrients,already_irrigated,amount_of_water):
		q="insert into farm_data(date,garden,last_watering_time,next_sheduled_time,last_rained,current_temperature,humidity,uv_radiation, soil_moisture,nutrients,already_irrigated,amount_of_water) values(?,?,?,?,?,?,?,?,?,?,?,?)"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		cur=c.cursor()
		cur.execute(q,(date,garden,last_watering_time,next_sheduled_time,last_rained,current_temperature,humidity,uv_radiation, soil_moisture,nutrients,already_irrigated,amount_of_water))
		c.commit()
		cur.close()
		c.close()
		return json.dumps({"message":"okay"})
	def get_garden_details_history(self,garden,date):
		q="select *from farm_data where garden=? and date=? order by data_id desc"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		c.row_factory=con.Row
		cur=c.cursor()
		cur.execute(q,(garden,date))
		datas=cur.fetchall()
		data=[]
		for d in datas:
			f={}
			f['garden']=d['garden']
			f['last_watering_time']=d['last_watering_time']
			f['next_sheduled_time']=d['next_sheduled_time']
			f['last_rained']=d['last_rained']
			f['current_temperature']=d['current_temperature']
			f['humidity']=d['humidity']
			f['uv_radiation']=d['uv_radiation']
			f['soil_moisture']=d['soil_moisture']
			f['nutrients']=d['nutrients']
			f['already_irrigated']=d['already_irrigated']
			f['amount_of_water']=d['amount_of_water']
			
			data.append(f)	
		c.close()
		return json.dumps({"number_of_records":str(len(data)),"data":data})
	def get_garden_details_now(self):
		q="select *from farm_data where garden=? and date=? order by data_id desc"
		conf=config()
		c=con.connect(conf.db_farm_crud())
		c.row_factory=con.Row
		cur=c.cursor()
		cur.execute(q,(self.garden,self.date))
		datas=cur.fetchall()
		data=[]
		for d in datas:
			f={}
			f['garden']=d['garden']
			f['last_watering_time']=d['last_watering_time']
			f['next_sheduled_time']=d['next_sheduled_time']
			f['last_rained']=d['last_rained']
			f['current_temperature']=d['current_temperature']
			f['humidity']=d['humidity']
			f['uv_radiation']=d['uv_radiation']
			f['soil_moisture']=d['soil_moisture']
			f['nutrients']=d['nutrients']
			f['already_irrigated']=d['already_irrigated']
			f['amount_of_water']=d['amount_of_water']
			data.append(f)
		c.close()
		return json.dumps({"number_of_records":str(len(data)),"data":data})
	
	def start_watering(self,current_temperature,humidity,uv_radiation, soil_moisture,amount_of_water,nutrients=[],already_irrigated="yes"):
		self.add_data(self.date,self.garden,self.timestamp_now,self.next_sheduled_time,self.last_rained,current_temperature,humidity,uv_radiation, soil_moisture,nutrients,already_irrigated,amount_of_water)
		return "sucess. watered @"+self.garden+"_garden"

	def get_watering_info(self,soil_moisture_level="n/a"):
		info=self.get_garden_details_now()
		data=info["data"]
		should_water_now="no"
		if info["number_of_records"] >0:
			message="halted! no farmdata/not yet time to water/ tool not configured"
			dump=data[0]
			last_watering_time=dump["last_watering_time"]
			soil_moisture=dump["soil_moisture"]
			already_irrigated=dump["already_irrigated"]
			last_watering_time=dump["last_watering_time"]
			watering_interval=self.farm_settings["watering_interval"]
			selected_watering_option=self.farm_settings["selected_watering_option"]
			if selected_watering_option=="with_interval":
				#time_difference=now-lasttime
				time_difference=int(round(abs(last_watering_time-self.timestamp_now).total_seconds())/60)

				if time_difference >=watering_interval and already_irrigated=="no":
					should_water_now="yes"
					message="running..please wait!"
				
			if selected_watering_option=="when_soil_runs_below_set_moisture_content":
				if soil_moisture_level!="n/a":
					should_water_now="yes"
					message="running..please wait!"

		else:
			message="no records found"
		return json.dumps({"message":message,"should_water_now":should_water_now})