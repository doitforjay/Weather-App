from flask import Flask, render_template, url_for, request, redirect, session, flash, g, jsonify
from functools import wraps
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource
#from bokeh.sampledata.stocks import AAPL
import pandas as pd
import requests, datetime, jinja2


application = Flask(__name__)
apikey = "AIzaSyAOJ3IXQVMQZ8T0T1hGSIPtQfXYyLjk_go"
weatherKey = "8ba7533a4402c0e6731515d9e13a5ec9"

#GET https://api.darksky.net/forecast/8ba7533a4402c0e6731515d9e13a5ec9/42.3601,-71.0589,409467600?exclude=currently,flags


locateUrl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
detailsUrl = "https://maps.googleapis.com/maps/api/place/details/json"
findAddress = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
weatherurl = "https://api.darksky.net/forecast/"
weatherparam = "?exclude=currently,flags,minutely,hourly"


template = jinja2.Template("""
<!DOCTYPE html>
<html lang="en-US">

<link
    href="http://cdn.pydata.org/bokeh/dev/bokeh-0.12.7rc3.min.css"
    rel="stylesheet" type="text/css"
>
<script 
    src="http://cdn.pydata.org/bokeh/dev/bokeh-0.12.7rc3.min.js"
></script>

<body>

    <h3>here is the weather trend for upcoming week!</h3>
    
   <h1 style="text-align:center;"> {{ city }}</h1>
    <div style="width:800px; margin:0 auto;">
    {{ script }}
    
    {{ div }}
    <h5 style="font-color:red:">--Highs</h5><h5>--Lows</h5>
    </div>
</body>
<style>
body{
	background: url(https://d2v9y0dukr6mq2.cloudfront.net/video/thumbnail/QwIr88a/winter-snow-landscape-mountain-cold-nature-white-sky-season-blue-frost-travel-ice-beautiful-tree-forest-scenic-frozen-snowy-vacation-panorama-sun-snowfall-xmas-light-christmas-beauty-background-view-park-weather-wood_4kmitlch__F0000.png);
	background-size: cover;
}
</style>
</html>
""")


def dtt(time):
	date = datetime.datetime.fromtimestamp(int(time))
	return date

@application.route('/', methods=['GET'])
def mainpage():
	return render_template("search.html")

@application.route('/plot')
def plot():
	return template.render(script=script, div=div)

@application.route('/searchLocation/<string:search>')
def searchresult(search):
	data = {"key":apikey, "query": search}
	data_req = requests.get(locateUrl, params=data)
	data_json = data_req.json()
	coordinates = data_json["results"][0]["geometry"]
	placeid = data_json["results"][0]["place_id"]
	details = {"key":apikey, "placeid":placeid}
	details_req = requests.get(detailsUrl, params=details)
	details_json = details_req.json()
	city = details_json["result"][""][3]

	lat = coordinates["location"]["lat"]
	lng = coordinates["location"]["lng"]
	coord = "/"+ str(lat) + "," + str(lng)

	weath_req = requests.get(weatherurl + weatherKey + coord + weatherparam)
	weath_json = weath_req.json()

	weath_data = weath_json["daily"]['data'][0]
	d = weath_json["daily"]['data']

	time = weath_data['time']

	x=[dtt(d[0]['time']), dtt(d[1]['time']), dtt(d[2]['time']), dtt(d[3]['time']), dtt(d[4]['time']),dtt(d[5]['time']),dtt(d[6]['time'])]

	x1 = [dtt(d[0]['time']), dtt(d[1]['time']), dtt(d[2]['time']), dtt(d[3]['time']), dtt(d[4]['time']),dtt(d[5]['time']),dtt(d[6]['time'])]
	high = [d[0]['temperatureHigh'],d[1]['temperatureHigh'] , d[2]['temperatureHigh'], d[3]['temperatureHigh'], d[4]['temperatureHigh'],d[5]['temperatureHigh'],d[6]['temperatureHigh']]
	low =[d[0]['temperatureLow'],d[1]['temperatureLow'] , d[2]['temperatureLow'], d[3]['temperatureLow'], d[4]['temperatureLow'],d[5]['temperatureLow'],d[6]['temperatureLow']]

	source = ColumnDataSource({
		'x': [x1,x1],
		'y': [high,low],
		'time_fmt':[dt.strftime("%Y-%m-%d") for dt in x1]
		})
	p = figure(plot_width=800, plot_height=250,x_axis_type='datetime')
	p.multi_line(xs='x',ys='y', color=['red','green'],source=source)
	script, div = components(p)



	#high = weath_data['apparentTemperatureHigh']
	#low = weath_data['apparentTemperatureLow']
	#hum = weath_data['humidity']
	#summ = weath_data['summary']
	#rain = weath_data['precipProbability']
	#wind = weath_data['windSpeed']
	
	return template.render(script=script, div=div, city=city)
	#return str(date)
	#return render_template("index.html", high = high, low=low, hum = hum, summ = summ, rain = rain, wind = wind)




if __name__ == '__main__':
    application.run(debug=True)
