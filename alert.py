import matplotlib.pyplot as plot
import mysql.connector as mysql
from mysql.connector import errorcode
import datetime
import matplotlib.dates as mdates



def week_query(connection, start, stop):
	query = "SELECT reading, datetime FROM tbl_soilmoisture WHERE datetime >= %s AND datetime <= %s" 
	x = (start, stop,)
	try:
		cursor = connection.cursor()
		cursor.execute(query, x)
		data = cursor.fetchall()
	except mysql.Error as err:
		print(err)
		connection.rollback()
	return data


	
def plot_image(x, y):
	x_values = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in x]
	formatter = mdates.DateFormatter("%m/%d/%Y")
	ax = plot.gca()
	ax.xaxis.set_major_formatter(formatter)
	locator = mdates.DayLocator()
	ax.xaxis.set_major_locator(locator)

	plot.plot(x_values, y, '--b')
	plot.title("Average Soil-Moisture Reading")
	plot.xlabel("Datetime")
	plot.ylabel("Soil Moisture")
	
	plot.grid(True)
	plot.savefig("Readings/"+str(x_values[len(x_values)-1].strftime("%m-%d-%Y"))+".png")

def x(date):
	null_date = ""
	data = []
	for x in date:
		if x.strftime("%m/%d/%Y") != null_date:
			null_date = x.strftime("%m/%d/%Y")
			data.append(null_date)
	data.sort()
	return data

def y(date_data, data):
	avg_data = []
	for x in date_data:
		sum_reading = 0
		for y in data:
			if x == y[1].strftime("%m/%d/%Y"):
				sum_reading += int(y[0])
		avg_data.append(round(sum_reading/3))
	return avg_data
		
	
def main():
	start_day = (datetime.datetime.now() - datetime.timedelta(7))
	stop_day = datetime.datetime.now()
	#MySQL initialization
	try:
		con = mysql.connect(user='rpi', password='PASSWORD', host='HOSTNAME', database='gardendb') #MySQL connection
		data = week_query(con, start_day, stop_day) # weekly data from soil sensor
		plot_image(x([row[1] for row in data]), y(x([row[1] for row in data]), data))
		con.commit()
	except mysql.Error as err:
		print(err)
	con.close()
	
	
	
#initialization
main()
	
