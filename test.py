from farm_crud import *
import json

gc=garden_settings("Fruits_garden")
d=json.loads(garden_settings.list_gardens())
#print (d['data'])
ll=live_log()
s=json.loads(ll.get_garden_live())
#print(s['data'])

w=farm_crud("Fruits_garden")
f=json.loads(w.get_garden_details_now())
print(f)