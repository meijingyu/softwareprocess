import os
import  xml.dom.minidom
import time
import math
import prod.Angle as Angle
from math import tan

class Fix():
    def __init__(self,logFile="log.txt"):
#         try:
#             self.getflextname(logFile)
#             self.getflextname(logFile).extension == ".txt"
#         except:
#             raise ValueError("error")
        try:
            self.logFile = open("log.txt", 'w')
        except:
            raise ValueError('could not create file')
        time_now = self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\t start of log:\n")
        self.logFile.close()
    
    def getflextname(self,filename):
        (self.shotname,self.extension) = os.path.splitext(self.filename);
        return self.shotname,self.extension    
    
    def get_time(self):
        time_now =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        return time_now
    
    def setSightingFile(self,sightingfile):
        try:
            self.getflextname(sightingfile)
            self.getflextname(sightingfile).extension == ".xml"
        except:
            raise ValueError("extension wrong")
        if (os.path.exists(sightingfile)):
            return False
        else:
            self.logFile = open("log.txt","a")
            self.logFile.write("LOG:\t",self.get_time(self),"\t Start of sighting file",sightingfile,"\n")
            self.logFile.close()
            return True
    
    def getsighting(self,sightingfile):
        try:
            os.path.exists(sightingfile)
        except:
            raise ValueError("file not exist")
        dom = xml.dom.minidom.parse(sightingfile)
        root = dom.documentElement
        
        sighting=root.getElementsByTagName('sighting')
        body=root.getElementsByTagName('body')
        date=root.getElementsByTagName('date')
        _time_=root.getElementsByTagName('time')
        observation=root.getElementsByTagName('observation')
        height=root.getElementsByTagName('height')
        temperature=root.getElementsByTagName('temperature')
        pressure=root.getElementsByTagName('pressure')
        horizon=root.getElementsByTagName('horizon')
        height= [[float(x) for x in inner] for inner in height]
        pressure= [[float(x) for x in inner] for inner in pressure]
        temperature= [[float(x) for x in inner] for inner in temperature]
        
        N = len(sighting)
        a =0
        for a in range(0,N):
            if( horizon[a]=="Natural"):
                dip = (-0.97 * ( height[a]**0.5 ) ) / 60
            else:
                dip =0.0
            angle1 = Angle.Angle()
            angle2 = Angle.Angle()
            angle_observation = angle1.setDegreesAndMinutes(observation[a])     
            t_altitude = tan(angle_observation)
            refraction = ( -0.00452 * pressure[a] ) / ( 273 + ( temperature-32/1.8 ) ) /t_altitude 
            adjustedAltitude = observation[a] + dip + refraction
            adjustedAltitude = float("%.1f"%adjustedAltitude)
            angle2 = adjustedAltitude
            adjustedAltitude = angle2.getString()
            
            self.logFile = open('log.txt',"a")
            self.logFile.write("LOG:\t",self.get_time(self),"\t",body[a],"\t",date[a],"\t",_time_[a],"\t",adjustedAltitude,"\n")
        self.logFile.write("LOG:\t",self.get_time(self),"\t Start of sighting file :\t",sightingfile)
        approximateLatitude = "0d0.0"    
        approximateLongitude = "0d0.0"    
        return (approximateLatitude, approximateLongitude)
            
        