import os
import re
#import xml.dom.minidom
import time
import math
import Angle 
from xml.dom import minidom
#11234132412412

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
        self.setstarFileFlag = 0     
        self.setAriesFileFlag =0
        self.assumd_lat =''
        self.assumd_lon =''
        self.adjustideAtitude=0
        self.sum1 = 0
        self.sum2 = 0
        self.assumd_lon_angle_number=0
        self.assumd_lat_angle_number=0
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
            print "step1"
            raise ValueError('Fix.setSightingFile:')
        if os.path.exists(sightingFile):
            print "step2"
            self.absSightingFilePath = os.path.abspath(self.sightingFileString)
        else:
            raise ValueError('Fix.setSightingFile:')
        
        if not os.path.realpath(self.absSightingFilePath):
            print "step3"
            raise ValueError('Fix.setSightingFile:')
        if ".xml" not in sightingFile:
            raise ValueError('Fix.setSightingFile:')
        sightingFileArray = sightingFile.split(".")
        if sightingFileArray[0] == "":
            print "step4"
            raise ValueError('Fix.setSightingFile:')
        time_now = self.get_time()
        print "step5"
        self.logFile.write("LOG:\t"+time_now+"\tsSighting file:\t" + self.absSightingFilePath+"\n")
        self.logFile.flush()
        try:
            open(sightingFile, 'r')
        except:
            raise ValueError('Fix.setSightingFile:')
        return self.absSightingFilePath
       
    def getSightings(self, assumd_lat='0d0.0',assumd_lon='0d0.0'): 
        self.assumd_lon = assumd_lon
        if 'S' not in assumd_lat:
            self.assumd_lat =assumd_lat
            if 'N' not in assumd_lat:
                assumd_lat_angle = Angle.Angle()
                try:
                    assumd_lat_angle.setDegreesAndMinutes(self.assumd_lat)
                except:
                    raise ValueError('Fix.getSightings:')
        if 'N' in assumd_lat:
            self.assumd_lat = assumd_lat.replace('N','')
            assumd_lat_angle = Angle.Angle()
            try:
                assumd_lat_angle.setDegreesAndMinutes(self.assumd_lat)
            except:
                raise ValueError('Fix.getSightings:')

        if 'S' in assumd_lat:
            self.assumd_lat = assumd_lat.replace('S','-')
            print self.assumd_lat
            assumd_lat_angle = Angle.Angle()
            try:
                assumd_lat_angle.setDegreesAndMinutes(self.assumd_lat)
            except:
                raise ValueError('Fix.getSightings:') 
        try:
            os.path.exists(self.sightingFile)
        except:
            raise ValueError("file not exist")
        timeStr = "^(?P<hour>[0-1]?[0-9]|[2][0-3]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])$"
        dateStr = "^(?P<year>[0-9]{4})\-(?P<month>[0-3]?[0-9])\-(?P<day>[0-3]?[0-9])$"
        if self.sightingFileString =="":
            raise ValueError("Fix.getSightings:")
        if self.setstarFileFlag==0:
            raise ValueError('Fix.getSightings:')
        if self.setAriesFileFlag ==0:
            raise ValueError('Fix.getSightings:')
        openxmlfile=open(self.sightingFileString)
        doc = minidom.parse(openxmlfile)
        root = doc.documentElement
        sightings = root.getElementsByTagName("sighting")
        self.sum1 = 0
        self.sum2 = 0
        for sighting in sightings:

            if len(sighting.getElementsByTagName("body"))!=0:
                if len(sighting.getElementsByTagName("body")[0].childNodes) != 0:
     
                    self.body = sighting.getElementsByTagName("body")[0].childNodes[0].nodeValue
                    if self.body != "Unknown" and self.body != "":
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
            self.adjustideAtitude =adjustideAtitude
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
                print "sha",SHA

                ariesGHA_angle1 = Angle.Angle()
                ariesGHA_angle2 = Angle.Angle()
                ariesGHA_angle1.setDegreesAndMinutes(aries[0]['gha'])
                ariesGHA_angle2.setDegreesAndMinutes(aries[1]['gha'])
                
                time_seconds = self._time_.split(":")
                s = float(time_seconds[1]) * 60 + float(time_seconds[2])
                GHA = ariesGHA_angle1.getDegrees() +ariesGHA_angle2.subtract(ariesGHA_angle1)* (s / 3600)
                print str(GHA)+"=gha"
                print str(SHA)+"=Sha"
                longtitude= GHA + SHA
                longtitude_angle = Angle.Angle()
                print longtitude
                longtitude_angle.setDegrees(longtitude)
                geographicPositionLongitude = longtitude_angle.getString()
                self.geographicPositionLongitude =geographicPositionLongitude
            a  = self.calculatelocalhourangle()
            print a[0],a[1]
            azi = a[0]
            distanceA =a[1]
            azi_angle =Angle.Angle()
            azi_degrees = azi_angle.setDegreesAndMinutes(azi)
            azi_radians = math.radians(azi_degrees)
            distance_cos = distanceA*math.cos(azi_radians)
            print "distance_cos",distance_cos
            distance_sin =distanceA*math.sin(azi_radians)
            print 'distance_sin',distance_sin
            self.sum1= self.sum1+distance_cos
            self.sum2 =self.sum2+distance_sin
            
            geo_latlist = self.geographicPositionLatitude.split('d')
            geo_lat1 = geo_latlist[0]
            if int(geo_lat1)>0:
                self.geographicPositionLatitude = 'N'+self.geographicPositionLatitude
            else:
                geo_lat1 =abs(int(geo_lat1))
                self.geographicPositionLatitude ='S'+str(geo_lat1)+"d"+geo_latlist[1]
            time_now= self.get_time()
            self.logFile.write("LOG:\t"+time_now+"\t"+self.body+"\t"+self.date+"\t"+self._time_+"\t"+str(adjustideAtitude_angle)+"\t"+self.geographicPositionLatitude+"\t"+self.geographicPositionLongitude+"\t"+self.assumd_lat+"\t"+self.assumd_lon+"\t"+a[0]+"\t"+str(a[1])+"\n")
            self.logFile.flush()
        print "self.sum1",self.sum1
        print "self.sum2",self.sum2
        approximate_lat =self.assumd_lat_angle_number+self.sum1/60
        print 'approximate_lat',approximate_lat
        if approximate_lat == 0 or approximate_lat == -180 or approximate_lat ==180 or approximate_lat==-360:
            appro_lat = '0d0.0'
            self.approximateLatitude = appro_lat
        if approximate_lat == 90 or approximate_lat == -270:
            self.approximateLatitude= 'N90d0.0'
        if approximate_lat == -90 or approximate_lat == 270:
            self.approximateLatitude= 'S90d0.0'
        if  0<approximate_lat<90:
            appro_angle  = Angle.Angle()
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'N'+appro_lat
        if 90<approximate_lat<180:
            approximate_lat = 90-approximate_lat%90
            appro_angle  = Angle.Angle()
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'N'+appro_lat
        if 180<approximate_lat<270:
            appro_angle  = Angle.Angle()
            approximate_lat = abs(approximate_lat)%90
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'S'+appro_lat
        if 270<approximate_lat<360:
            appro_angle  = Angle.Angle()
            approximate_lat = 90 - abs(approximate_lat)%90
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'S'+appro_lat
        if -90<approximate_lat<0:
            appro_angle  = Angle.Angle()
            appro_angle.setDegrees(abs(approximate_lat))
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'S'+appro_lat
        if -180<approximate_lat<-90:
            approximate_lat = 90-abs(approximate_lat)%90
            appro_angle  = Angle.Angle()
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'S'+appro_lat
        if -270<approximate_lat<-180:
            appro_angle  = Angle.Angle()
            approximate_lat = abs(approximate_lat)%90
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'N'+appro_lat
        if -270<approximate_lat<-360:
            approximate_lat = 90-abs(approximate_lat)%90
            appro_angle  = Angle.Angle()
            appro_angle.setDegrees(approximate_lat)
            appro_lat = appro_angle.getString()
            self.approximateLatitude = 'N'+appro_lat
        approximate_lon =self.assumd_lon_angle_number+self.sum2/60
        print 'approximate_lon',approximate_lon
        appro_angle_lon = Angle.Angle()
        appro_angle_lon.setDegrees(approximate_lon)
        self.approximateLongitude = appro_angle_lon.getString()
        
        time_now= self.get_time()
        self.logFile.write("LOG:\t"+time_now+"\t"+"Sighting errors:\t"+str(self.sightingfileerror)+"\n")
        self.logFile.write("LOG:\t"+time_now+"\t"+"Approximate Latitude:\t"+self.approximateLatitude+"\t"+"Approximate Longtitude:"+"\t"+self.approximateLongitude+"\n")
        self.logFile.flush()
        self.logFile.close()
        print  "jieguoshi:",self.approximateLatitude+"\t"+self.approximateLongitude
        return (self.approximateLatitude, self.approximateLongitude)
    
    def setAriesFile(self,ariesFile=0):
        self.setAriesFileFlag =1
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
        self.setstarFileFlag =1
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
                    if len(starFilelist) == 4:
                        if(starFilelist[0] == self.body):
                            date_list1 =self.date.split("-")
                            date_month=date_list1[1]
                            date_day = date_list1[2]
                            date_list2 =starFilelist[1].split("/")
                            filedate_day = date_list2[1]
                            filedate_month =date_list2[0]
                            date1 = date_month+date_day  
                            date2 = filedate_month+filedate_day
                            if int(date_month)==int(filedate_month) and int(date_day) <= int(filedate_day) and a ==0:
                                starFile_data = {'body': starFilelist[0], 
                                 'date': starFilelist[1],
                                 'longtitude': starFilelist[2],
                                 'latitude': starFilelist[3]}
                                a += 1
                                return starFile_data
                    if len(starFilelist) ==5:
                        if(starFilelist[0]+' '+starFilelist[1] == self.body):
                            date_list1 =self.date.split("-")
                            date_month=date_list1[1]
                            date_day = date_list1[2]
                            date_list2 =starFilelist[2].split("/")
                            filedate_day = date_list2[1]
                            filedate_month =date_list2[0]
                            date1 = date_month+date_day  
                            date2 = filedate_month+filedate_day
                            if int(date_month)==int(filedate_month)and int(date_day)>= int(filedate_day) and a ==0:
                                starFile_data = {'body': starFilelist[0]+' '+starFilelist[1], 
                                 'date': starFilelist[2],
                                 'longtitude': starFilelist[3],
                                 'latitude': starFilelist[4]}
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
#                 date1 = time.strptime(self.date, "%Y-%m-%d")
                time1list = self._time_.split(":")
                time1 = int(time1list[0])
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
            
    def calculatelocalhourangle(self):
            geo_lon_angle = Angle.Angle()
            geo_lon_angle_number  = geo_lon_angle.setDegreesAndMinutes(self.geographicPositionLongitude)
            print "self.geographicPositionLongitude",self.geographicPositionLongitude
            assumd_lon_angle =Angle.Angle()
            assumd_lon_angle_number = assumd_lon_angle.setDegreesAndMinutes(self.assumd_lon)
            self.assumd_lon_angle_number =assumd_lon_angle_number
            LHA = geo_lon_angle_number  + assumd_lon_angle_number
            print "LHA:",LHA
            LHA_angle = Angle.Angle()
            LHA_angle.setDegrees(LHA)
            LHA_angle_str = LHA_angle.getString()
            geo_lat_angle =Angle.Angle()
            geo_lat_angle_number = geo_lat_angle.setDegreesAndMinutes(self.geographicPositionLatitude)
            geoLatitude_radians = math.radians(geo_lat_angle_number)
            sinlat1 = math.sin(geoLatitude_radians)
            print "sinlat1:",sinlat1
            assumd_lat_angle =Angle.Angle()
            assumd_lat_angle_number = assumd_lat_angle.setDegreesAndMinutes(self.assumd_lat)
            self.assumd_lat_angle_number =assumd_lat_angle_number
            assumd_lat_radians = math.radians(assumd_lat_angle_number)
            sinlat2 = math.sin(assumd_lat_radians)
            print "sinlat2:",sinlat2
            sinlat =sinlat1 * sinlat2
            print "sinlat:",sinlat
            coslat1 = math.cos(geoLatitude_radians)
            print "coslat1",coslat1
            coslat2 =math.cos(assumd_lat_radians)
            print "coslat2",coslat1
            LHA_angle_radians = math.radians(LHA)
            cos_LHA = math.cos(LHA_angle_radians)
            print "coslha",cos_LHA
            coslat = coslat1*coslat2*cos_LHA
            print "coslat",coslat
            intermediate_distance=coslat+sinlat
            print "intermediate_distance",intermediate_distance
            corrected_altitude  = math.asin(intermediate_distance)
            print "corrected_altitude",corrected_altitude
            corrected_altitude_degree = math.degrees(corrected_altitude)
            print "corrected_altitude-degrees",corrected_altitude_degree
            distance_adjustment = corrected_altitude_degree - self.adjustideAtitude
            print 'distance_adjustment',distance_adjustment
            distance_adjustment = round(60 * distance_adjustment)
            print 'distance_adjustment_round',distance_adjustment
            numerator_1 = sinlat1-sinlat2*intermediate_distance
            print 'numerator',numerator_1
            coslat3 = math.cos(corrected_altitude)
            denominator =  coslat2 * coslat3
            intermedia_azimuth =    numerator_1 / denominator
            azimuth_adjustment =    math.acos(numerator_1 /denominator)
            print 'azimuth_adjustment',azimuth_adjustment
            azimuth_adjustment_degree =math.degrees(azimuth_adjustment)
            azimuth_adjustment_angle =Angle.Angle()
            azimuth_adjustment_angle.setDegrees(azimuth_adjustment_degree)
            azimuth_adjustment_str = azimuth_adjustment_angle.getString()
            print 'azimuth_adjustment_str',azimuth_adjustment_str
            return azimuth_adjustment_str,distance_adjustment
             
            
            
                