import serial
import mysql.connector as mysql
from mysql.connector import errorcode
import matplotlib.pyplot as plot
import time 
	
#soil moisture data
def soil_moisture(serial):
	time.sleep(2)
	serial.write(("2\n").encode())
	moisture = serial.readline().decode()
	moisture = moisture.replace('Soil Moisture: ','')
	return moisture

#insert data db 
def insert_data(connection, data):
	insert_query = ("INSERT INTO tbl_soilmoisture(reading) VALUES(%s)")
	reading = (data,)
	try:
		cursor = connection.cursor()
		cursor.execute(insert_query, reading)	
	except mysql.Error as err:
		print(err)
		connection.rollback()
	
	
#main method
def main():
	# Serial Connection
	ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) # Serial initialization
	ser.flush()
	if ser.is_open == True:
		try:
			#MySQL Connection
			con = mysql.connect(user='rpi', password='PASSWORD', host='HOSTNAME', database='gardendb') #MySQL open connection
			insert_data(con, soil_moisture(ser)) # Inserting soil readings to db
			con.commit()
		except mysql.Error as err:
			print(err) 
		con.close() #MySQL connection close
	
#initialization
main()
