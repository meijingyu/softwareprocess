import os
import xml.dom.minidom
import time
import math
import prod.Angle as Angle
from math import tan
from cgi import logfile
from matplotlib.cbook import Null
from cmath import sqrt

class Fix(object):
    def __init__(self,logFile='log.txt'):
        functionName = "Fix.__init__: "
        if not isinstance(logFile, basestring):
            raise ValueError(functionName + "logFile must be a String!")
        if len(logFile) < 1:
            raise ValueError(functionName)
        self.body='0'
        self.date='0'
        self._time_='0'
        self.observation='0'
        self.AriesFile=0
        self.starFile=0
        self.logFile = logFile
        self.sightingFile = ''
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        self.absSightingFilePath=''
        self.sightingfileerror=0
        try:
            self.logFile = open(logFile,'r')
        except IOError:
            self.logFile = open(logFile, 'w')
        else:
            self.logFile = open(logFile,'a')
        time_now =self.get_time()
        spath=os.path.abspath(logFile)
        self.logFile.write("LOG:\t"+time_now+"\tLog file:"+spath+"\n")
        self.logFile.flush()

    def get_time(self):
        time_now =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        return time_now
    
    def setSightingFile(self,sightingfile=0):
        if sightingfile is 0:
            raise ValueError('Fix.setSightingFile:')
        if isinstance(sightingfile, int) or isinstance(sightingfile, float):
            raise ValueError('Fix.setSightingFile:')
        self.sightingFile =sightingfile
        if os.path.exists(sightingfile):
            self.absSightingFilePath = os.path.abspath(self.sightingFile)
        else:
            raise ValueError('Fix.setSightingFile:')
        
        if not os.path.realpath(self.absSightingFilePath):
            raise ValueError('Fix.setSightingFile:')
        if ".xml" not in sightingfile:
            raise ValueError('Fix.setSightingFile:')
        sightingFile_list = sightingfile.split(".")
        if sightingFile_list[0] == "":
            raise ValueError('Fix.setSightingFile:')
        
        time_now =self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\tSighting file:"+self.absSightingFilePath+"\n")
        self.logFile.flush()
        try:
            open(sightingfile, 'r')
        except:
            raise ValueError('Fix.setSightingFile:')
        return self.absSightingFilePath
    
    def getSightings(self):
        try:
            os.path.exists(self.sightingFile)
        except:
            raise ValueError("file not exist")
        dom = xml.dom.minidom.parse(self.sightingFile)
        sightings = dom.documentElement
        sightingslist = sightings.getElementsByTagName("sighting")
        self.sightingfileerror=0
        N = len(sightings.getElementsByTagName("sighting"))
#         a =0
#         for a in (0,N-1):
        for sighting in sightingslist:
            if(len(sightings.getElementsByTagName("body")) == len(sightings.getElementsByTagName("sighting"))):
                print len(sightings.getElementsByTagName("body")) 
                print len(sightings.getElementsByTagName("sighting"))
                self.body = sightings.getElementsByTagName("body")[0].childNodes[0].data
                if not self.body == "unknown":
                    if(len(sightings.getElementsByTagName("date") )==len(sightings.getElementsByTagName("sighting"))):
                        self.date = sightings.getElementsByTagName("date")[0].childNodes[0].data
                        if(len(sightings.getElementsByTagName("time") ) == len(sightings.getElementsByTagName("sighting"))):
                            self._time_ = sightings.getElementsByTagName("time")[0].childNodes[0].data
                            if(len(sightings.getElementsByTagName("observation")) ==len(sightings.getElementsByTagName("sighting"))):
                                self.observation = sightings.getElementsByTagName("observation")[0].childNodes[0].data
                                if(len(sightings.getElementsByTagName("height"))!=0):
                                    height = sightings.getElementsByTagName("height")[0].childNodes[0].data
                                else:
                                    height = 0.0
                                if(len(sightings.getElementsByTagName("temperature"))!=0):
                                    temperature = sightings.getElementsByTagName("temperature")[0].childNodes[0].data
                                else:
                                    temperature = 72
                                if(len(sightings.getElementsByTagName("pressure"))!=0):
                                    pressure = sightings.getElementsByTagName("pressure")[0].childNodes[0].data
                                else:
                                    pressure = 1010
                                if(len(sightings.getElementsByTagName("horizon")) != 0):
                                    print len(sightings.getElementsByTagName("horizon"))
                                    horizon = sightings.getElementsByTagName("horizon")[0].childNodes[0].data
                                else:
                                    horizon = "Natural"
                            else:
                                return 0
                                self.sightingfileerror+=1
                                continue
                        else:
                            return 0
                            self.sightingfileerror+=1
                            continue
                    else:
                        return 0
                        self.sightingfileerror+=1
                        continue
                else:
                    return 0
                    self.sightingfileerror+=1
                    continue
            else:
                return 0
                self.sightingfileerror+=1
                continue
            if (horizon =="Natural"):
                dip=(-0.97* math.sqrt(float(height)))/60
            else:
                dip=0.0
            observation_angle = Angle.Angle()
            observation_angle.setDegreesAndMinutes(self.observation)
            observation_angle_degrees =observation_angle.getDegrees()
            refraction = ( -0.00452 * float(pressure) ) / ( 273 + (float(temperature) - 32 ) / 1.8 ) /math.tan((math.pi * float(observation_angle_degrees))/180.0)             
            adjustideAtitude = observation_angle_degrees+dip+(refraction)
            adjust_angle = Angle.Angle()
            adjust_angle.setDegrees(adjustideAtitude)
            print adjustideAtitude
            adjustideAtitude_angle =adjust_angle.getString()
            star = self.readstarFile()
            aries = self.readAriesFile()
            if star is not None:
                star_longtitude =star['longtitude']
                geographicPositionLatitude = star['latitude']
                star_SHA_angle = Angle.Angle()
                star_SHA_angle.setDegreesAndMinutes(star_longtitude)
                SHA = star_SHA_angle.getDegrees()
            if not aries is None:
                ariesGHA_angle1 = Angle.Angle()
                ariesGHA_angle2 = Angle.Angle()
                ariesGHA_angle1.setDegreesAndMinutes(aries[0]['gha'])
                ariesGHA_angle2.setDegreesAndMinutes(aries[1]['gha'])
                
                time_seconds = self._time_.split(":")
                s = float(time_seconds[1]) * 60 + float(time_seconds[2])
                GHA = ariesGHA_angle1.getDegrees() +ariesGHA_angle1.subtract(ariesGHA_angle1)* (s / 3600)
                longtitude= GHA + SHA
                longtitude_angle = Angle.Angle()
                longtitude_angle.setDegrees(longtitude)
                geographicPositionLongitude = longtitude_angle.getString()
                time_now= self.get_time()
                self.logFile.write("LOG:\t"+time_now+"\t"+self.body+"\t"+self.date+"\t"+self._time_+"\t"+str(adjustideAtitude_angle)+"\t"+geographicPositionLatitude+"\t"+geographicPositionLongitude+"\n")
                self.logFile.flush()
            return (geographicPositionLatitude, geographicPositionLongitude)
        time_now= self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\t"+"Sighting errors:\t"+str(self.sightingfileerror)+"\n")
        self.logFile.flush()
        self.logFile.close()   
    
    def setAriesFile(self,AriesFile=0):
        self.AriesFile = AriesFile
        spath= os.path.abspath(self.AriesFile)
        self.logFile =open(self.logFile,"a")
        time_now= self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\tAries File:"+spath+"\n")
        self.logFile.flush()
    
    def setStarFile(self,starFile=0):
        self.starFile= starFile
        spath= os.path.abspath(self.starFile)
        self.logFile =open("log.txt","a")
        time_now= self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\tstarFile:"+spath+"\n")
        self.logFile.flush()
    
    def readstarFile(self):
        if self.starFile == "":
            raise ValueError("Fix.readStars:")
        if self.body =="":
            raise ValueError("Fix.readStars:")
        if self.date =="":
            raise ValueError("Fix.readStars:")
        if self._time_ =="":
            raise ValueError("Fix.readStars:")
        if self.starFile ==0:
            starFile_data = {'body': 0, 
                         'date': 0,
                         'longtitude': "0d0.0",
                         'latitude': "0d0.0"}
            return starFile_data
        else:
            self.starFile = open(self.starFile)
            starReadlines = self.starFile.readlines()
            a =0
            starFile_data = {'body': '', 'date': '', 'longitude': '','latitude':'' }
            for starReadline in starReadlines:
                    starFilelist = starReadline.split()
                    if(starFilelist[0] == self.body):
                        date1 = time.strptime(self.date, "%Y-%m-%d")
                        date2 = time.strptime(starFilelist[1], "%m/%d/%y")
                        if date1>date2 or a == 0:
                            starFile_data = {'body': starFilelist[0], 
                             'date': starFilelist[1],
                             'longtitude': starFilelist[2],
                             'latitude': starFilelist[3]}
                            a += 1
                        else:
                            return starFile_data
    def readAriesFile(self):
        if self.AriesFile =="":
            raise ValueError("Fix.readStars:")
        if self._time_ =="":
            raise ValueError("Fix.readStars:")
        if self.date =='':
            raise ValueError("Fix.readStars:")
        if self.AriesFile ==0:
            ariesline_data1 = {'date': 0,
                                 'hour': 0,
                                 'gha': "0d0.0"}
            ariesline_data2 = {'date': 0,
                                 'hour': 0,
                                 'gha': "0d0.0"}
            return ariesline_data1,ariesline_data2
        else:
            self.AriesFile =open(self.AriesFile)
            ariesReadlines =self.AriesFile.readlines()
            a =0 
            for ariesReadline in ariesReadlines:
                ariesFilelist= ariesReadline.split()             
                date1 = time.strptime(self.date, "%Y-%m-%d")
                time1list = self._time_.split(":")
                time1 = int(time1list[0])
                date2 = time.strptime(ariesFilelist[0], "%m/%d/%y")
                time2 = int(ariesFilelist[1])
                if date1 == date2 and time1 == time2:
                    if a == 0:
                        ariesline_data1 = {'date': ariesFilelist[0],
                                     'hour': ariesFilelist[1],
                                     'gha': ariesFilelist[2]}
                        a = a+1 
                    if a== 1 and date1 ==date2 and time1+1 ==time2:
                        ariesline_data2 = {'date': ariesFilelist[0],
                                     'hour': ariesFilelist[1],
                                     'gha': ariesFilelist[2]}
                        return ariesline_data1,ariesline_data2
            if a == 0:
                return False 
        
                    
        
                              
    
        
                    