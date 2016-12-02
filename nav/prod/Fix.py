import os
import re
import xml.dom.minidom
import time
import math 
import nav.prod.Angle as Angle
from xml.dom import minidom

sdfsdfa dfa 
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
        self.AriesFile= ''
        self.starFile=''
        self.starFilestr =''
        self.logFile = logFile
        self.sightingFile = ''
        self.sightingFileString=''
        self.geographicPositionLatitude = ''
        self.geographicPositionLongitude = ''
        self.absSightingFilePath=''
        self.sightingfileerror=0
        self.ariesFilestr=''
        self.approximateLatitude = "0d0.0"            
        self.approximateLongitude = "0d0.0"
        self.ariesFilestr_1 ="aries.txt"
        self.starFilestr_1 ="stars.txt"           
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
    
    def setSightingFile(self,sightingFile=0):
        if sightingFile is 0:
            raise ValueError('Fix.setSightingFile:')
        self.sightingFile = sightingFile
        self.sightingFileString =sightingFile
        if isinstance(sightingFile, int) or isinstance(sightingFile, float):
            raise ValueError('Fix.setSightingFile:')
        if os.path.exists(sightingFile):
            self.absSightingFilePath = os.path.abspath(self.sightingFileString)
        else:
            raise ValueError('Fix.setSightingFile:')
        
        if not os.path.realpath(self.absSightingFilePath):
            raise ValueError('Fix.setSightingFile:')
        if ".xml" not in sightingFile:
            raise ValueError('Fix.setSightingFile:')
        sightingFileArray = sightingFile.split(".")
        if sightingFileArray[0] == "":
            raise ValueError('Fix.setSightingFile:')
        time_now = self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\tsSighting file:\t" + self.absSightingFilePath + "\n")
        self.logFile.flush()
        try:
            open(sightingFile, 'r')
        except:
            raise ValueError('Fix.setSightingFile:')
        return self.absSightingFilePath
       
    def getSightings(self):
        try:
            os.path.exists(self.sightingFile)
        except:
            raise ValueError("file not exist")
        timeStr = "^(?P<hour>[0-1]?[0-9]|[2][0-3]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])$"
        dateStr = "^(?P<year>[0-9]{4})\-(?P<month>[0-3]?[0-9])\-(?P<day>[0-3]?[0-9])$"
        if self.sightingFileString =="":
            raise ValueError("Fix.getSightings:")
        openxmlfile=open(self.sightingFileString)
        doc = minidom.parse(openxmlfile)
        root = doc.documentElement
        sightings = root.getElementsByTagName("sighting")
        for sighting in sightings:

            if len(sighting.getElementsByTagName("body"))!=0:
                if len(sighting.getElementsByTagName("body")[0].childNodes) != 0:
     
                    self.body = sighting.getElementsByTagName("body")[0].childNodes[0].nodeValue
                    if self.body != "unknown" and self.body != "":
                        if len(sighting.getElementsByTagName("date"))!=0:
                            self.date =sighting.getElementsByTagName("date")[0].childNodes[0].nodeValue
                            isDate = re.search(dateStr, self.date)
                            if not isDate:
                                self.sightingfileerror+=1
                                continue
                            if self.date !="":
                                if len(sighting.getElementsByTagName("time"))!=0:
                                    self._time_ =sighting.getElementsByTagName("time")[0].childNodes[0].nodeValue
                                    isTime = re.search(timeStr, self._time_)
                                    if not isTime:
                                        self.sightingfileerror+=1
                                        continue
                                    if self._time_ !="":
                                        if len(sighting.getElementsByTagName("observation"))!=0:
                                            self.observation =sighting.getElementsByTagName("observation")[0].childNodes[0].nodeValue
                                            observation_angle=Angle.Angle()
                                            try:
                                                observation_angle.setDegreesAndMinutes(self.observation)
                                            except:
                                                self.sightingfileerror+=1
                                                continue 
                                        else:
                                            self.sightingfileerror+=1
                                            continue
                                    else:
                                        self.sightingfileerror+=1
                                        continue
                                else:
                                    self.sightingfileerror+=1
                                    continue
                            else:
                                self.sightingfileerror+=1
                                continue      
                        else:
                            self.sightingfileerror+=1
                            continue
                    else:
                        self.sightingfileerror+=1
                        continue
                else:
                        self.sightingfileerror+=1
                        continue
            else:
                self.sightingfileerror+=1
                continue
            if(len(sighting.getElementsByTagName("height"))!=0):
                height = sighting.getElementsByTagName("height")[0].childNodes[0].data
                try:
                    height = float(height)
                except:
                    self.sightingfileerror+=1
                    continue
            else:
                height = 0.0
            if(len(sighting.getElementsByTagName("temperature"))!=0):
                temperature = sighting.getElementsByTagName("temperature")[0].childNodes[0].data
                try:
                    temperature = int(temperature)
                except:
                    self.sightingfileerror+=1
                    continue
                if int(temperature) > 120 or int(temperature) <-20:
                    self.sightingfileerror+=1
                    continue
            else:
                temperature = 72
            if(len(sighting.getElementsByTagName("pressure"))!=0):
                pressure = sighting.getElementsByTagName("pressure")[0].childNodes[0].data
                try:
                    pressure = int(pressure)
                except:
                    self.sightingfileerror+=1
                    continue
                if int(pressure) >1100 or int(pressure) <100:
                    self.sightingfileerror+=1
                    continue
            else:
                pressure = 1010
            if(len(sighting.getElementsByTagName("horizon")) != 0):
                horizon = sighting.getElementsByTagName("horizon")[0].childNodes[0].data
                if not (horizon == 'Artificial' or horizon =='Natural' or horizon =='artificial' or horizon =='natural'):
                    self.sightingfileerror+=1
                    continue
            else:
                horizon = "Natural"

            if (horizon =="Natural" or horizon =="natural"):
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

            adjustideAtitude_angle =adjust_angle.getString()
            star = self.readstarFile()
            aries = self.readAriesFile()
            if star is not None:
                star_longtitude =star['longtitude']
                print star_longtitude
                geographicPositionLatitude = star['latitude']
                self.geographicPositionLatitude=geographicPositionLatitude
                star_SHA_angle = Angle.Angle()
                star_SHA_angle.setDegreesAndMinutes(star_longtitude)
                SHA = star_SHA_angle.getDegrees()

                ariesGHA_angle1 = Angle.Angle()
                ariesGHA_angle2 = Angle.Angle()
                ariesGHA_angle1.setDegreesAndMinutes(aries[0]['gha'])
                ariesGHA_angle2.setDegreesAndMinutes(aries[1]['gha'])
                
                time_seconds = self._time_.split(":")
                s = float(time_seconds[1]) * 60 + float(time_seconds[2])
                GHA = ariesGHA_angle1.getDegrees() +ariesGHA_angle1.subtract(ariesGHA_angle1)* (s / 3600)
                print str(GHA)+"=gha"
                print str(SHA)+"=Sha"
                longtitude= GHA + SHA
                longtitude_angle = Angle.Angle()
                print longtitude
                longtitude_angle.setDegrees(longtitude)
                geographicPositionLongitude = longtitude_angle.getString()
                self.geographicPositionLongitude =geographicPositionLongitude

            time_now= self.get_time()
            self.logFile.write("LOG:\t"+time_now+"\t"+self.body+"\t"+self.date+"\t"+self._time_+"\t"+str(adjustideAtitude_angle)+"\t"+self.geographicPositionLatitude+"\t"+self.geographicPositionLongitude+"\n")
            self.logFile.flush()
        time_now= self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\t"+"Sighting errors:\t"+str(self.sightingfileerror)+"\n")
        self.logFile.flush()
        self.logFile.close()
        print  self.geographicPositionLatitude+"\t"+self.geographicPositionLongitude
        print self.sightingfileerror
        return (self.approximateLatitude, self.approximateLongitude)
    
    def setAriesFile(self,ariesFile=0):
        print "start"
        if ariesFile is 0:
            
            raise ValueError('Fix.setAriesFile:')
        self.Ariesfile =ariesFile
        self.ariesFilestr = ariesFile
        self.ariesFilestr_1=ariesFile
        if isinstance(ariesFile, int) or isinstance(ariesFile, float):

            raise ValueError('Fix.setAriesFile:')
        
        if ".txt" not in ariesFile:
   
            raise ValueError('Fix.setAriesFile:')
        ariesFilelist = ariesFile.split(".")
        if ariesFilelist[0] == "":
    
            raise ValueError('Fix.setAriesFile:')
        
        if(isinstance(ariesFile, str)):
            if(os.path.exists(ariesFile)):
                try:
                    self.AriesFile = open(ariesFile)
                except:
 
                    raise ValueError("Fix.setAriesFile:")
                self.ariesFilePath = os.path.abspath(ariesFile)
                time_now = self.get_time()
                self.logFile.write("LOG:\t"+time_now+"\tAries file:"+self.ariesFilePath+"\n")
                self.logFile.flush()
                return self.ariesFilePath
            else:

                raise ValueError("Fix.setAriesFile:")
    def setStarFile(self,starFile=0):
        if starFile is 0:
            raise ValueError('Fix.setStarFile:')
        self.starFile =starFile
        self.starFilestr = starFile
        self.starFilestr_1 =starFile
        if isinstance(starFile, int) or isinstance(starFile, float):
            raise ValueError('Fix.setStarFile:')
        
        if ".txt" not in starFile:
            raise ValueError('Fix.setStarFile:')
        starFilelist = starFile.split(".")
        if starFilelist[0] == "":
            raise ValueError('Fix.setStarFile:')
        
        if(isinstance(starFile, str)):
            if(os.path.exists(starFile)):
                try:
                    self.AriesFile = open(starFile)
                except:
                    raise ValueError("Fix.setStarFile:")
                self.starFilePath = os.path.abspath(starFile)
                time_now = self.get_time()
                self.logFile.write("LOG:\t"+time_now+"\tStar file:"+self.starFilePath+"\n")
                self.logFile.flush()
                return self.starFilePath
            else:
                raise ValueError("Fix.setStarFile:")
    
    def readstarFile(self):
        starFile_data={'body': '', 'date': '', 'longitude': '','latitude':'' }
        if self.starFilestr_1 == "":
            raise ValueError("Fix.readStars:")
        if self.body =="":
            raise ValueError("Fix.readStars:")
        if self.date =="":
            raise ValueError("Fix.readStars:")
        if self._time_ =="":
            raise ValueError("Fix.readStars:")
        if self.starFilestr_1 ==1:
            starFile_data = {'body': 0, 
                         'date': 0,
                         'longtitude': "0d0.0",
                         'latitude': "0d0.0"}
            return starFile_data
        else:
            self.starFile = open(self.starFilestr_1)
            starReadlines = self.starFile.readlines()
            a =0
            starFile_data = {'body': '', 'date': '', 'longitude': '','latitude':'' }
            for starReadline in starReadlines:
                    starFilelist = starReadline.split()
                    if(starFilelist[0] == self.body):
                        date_list1 =self.date.split("-")
                        date_month=date_list1[1]
                        date_day = date_list1[2]
                        date_list2 =starFilelist[1].split("/")
                        filedate_day = date_list2[1]
                        filedate_month =date_list2[0]
                        date1 = date_month+date_day  
                        date2 = filedate_month+filedate_day
                        if int(date_month)==int(filedate_month)and int(date_day)>= int(filedate_day) and a ==0:
                            starFile_data = {'body': starFilelist[0], 
                             'date': starFilelist[1],
                             'longtitude': starFilelist[2],
                             'latitude': starFilelist[3]}
                            a += 1
                            return starFile_data
            if a==0:
                return False
    def readAriesFile(self):
        
        ariesline_data1={'body': '', 'hour': '', 'gha': ''}
        ariesline_data2={'body': '', 'hour': '', 'gha': ''}
        if self.ariesFilestr_1 =="":
            raise ValueError("Fix.readStars:")
        if self._time_ =="":
            raise ValueError("Fix.readStars:")
        if self.date =='':
            raise ValueError("Fix.readStars:")
        if self.ariesFilestr_1 ==1:
            ariesline_data1 = {'date': 0,
                                 'hour': 0,
                                 'gha': "0d0.0"}
            ariesline_data2 = {'date': 0,
                                 'hour': 0,
                                 'gha': "0d0.0"}
            return ariesline_data1,ariesline_data2
        else:
            print "yungixing2"
            self.AriesFile =open(self.ariesFilestr_1)
            ariesReadlines =self.AriesFile.readlines()
            a =0 
            for ariesReadline in ariesReadlines:
                ariesFilelist= ariesReadline.split()
                date_list1 =self.date.split("-")
                date_month=date_list1[1]
                date_day = date_list1[2]
                date_list2 =ariesFilelist[0].split("/")
                filedate_day = date_list2[1]
                filedate_month =date_list2[0]
                date1 = date_month+date_day  
                date2 = filedate_month+filedate_day
                print date1+"\t"+date2
#                 date1 = time.strptime(self.date, "%Y-%m-%d")
                time1list = self._time_.split(":")
                time1 = int(time1list[0])
#                 date2 = time.strptime(ariesFilelist[0], "%m/%d/%y")
                time2 = int(ariesFilelist[1])
                if a== 1:
                    ariesline_data2 = {'date': ariesFilelist[0],
                                     'hour': ariesFilelist[1],
                                     'gha': ariesFilelist[2]}
                    
                    return ariesline_data1,ariesline_data2
                if date1 == date2 and time1 == time2:
                    print "yunxing3"
                    if a == 0:
                        ariesline_data1 = {'date': ariesFilelist[0],'hour': ariesFilelist[1],'gha': ariesFilelist[2]}
                        a=a+1
            if a == 0:
                return False
                