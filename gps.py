'''
GPS Interfacing with Raspberry Pi using Python
http://www.electronicwings.com

See link below for sign conventions (Pos. Latitude = North, Negative Latitude = South,
Positive Longitude = East, Negative Longitude = West)

http://academic.brooklyn.cuny.edu/geology/leveson/core/linksa/decimalconvert.html

See link for GPGGA string information: https://raspberrypi.stackexchange.com/questions/12029/extracting-required-information-from-nmea-gps-data
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_MSL_altitude = []
    nmea_MSL_altitude_unit = []
    nmea_north_south_indicator = []
    nmea_east_west_indicator = []
    nmea_satellites = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    nmea_MSL_altitude = NMEA_buff[8]            #extract mean sea level altitude from GPGGA string
    nmea_MSL_altitude_unit = NMEA_buff[9]       #extract altitude unit. ex. meters,M
    nmea_north_south_indicator = NMEA_buff[2]   #if south of equator, latitude is negative
    nmea_east_west_indicator = NMEA_buff[4]     #if west of prime meridian, longitude is negative
    nmea_satellites = NMEA_buff[6]              #number of satellites in view
    
    if nmea_north_south_indicator == 'S':
        nmea_latitude = '-'+ nmea_latitude
    
    if nmea_east_west_indicator == 'W':
        nmea_longitude = '-'+ nmea_longitude
          
    print("NMEA Time: ", nmea_time,'\n')
    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    print("MSL altitude is:", nmea_MSL_altitude, nmea_MSL_altitude_unit, '\n')
    print(nmea_north_south_indicator,'of equator',',',nmea_east_west_indicator,'of prime meridian','\n')
    print(nmea_satellites , 'satellites in view','\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    


gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0



try:
    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude
 
            print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
            map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
            print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
            print("------------------------------------------------------------\n")
           
                        
except KeyboardInterrupt:
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)
