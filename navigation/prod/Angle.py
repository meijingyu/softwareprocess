from numpy import integer
from tarfile import TUREAD
class Angle():
    def __init__(self):
        self.degrees = 0    #   set to 0 degrees 0 minutes
        
    
    def setDegrees(self, degrees=0.0):
        if(isinstance(degrees, float)) or (isinstance(degrees, int)):
            degrees = round( degrees * 60.0, 1) / 60.0
            if degrees > -360 and degrees < 0:
                degrees = degrees + 360    
            elif degrees >=0 and degrees < 360:
                degrees = degrees 
            elif degrees <= -360:
                n = degrees % 360
                degrees = n
            elif degrees >=360:
                n = degrees % 360
                degrees = n
            degrees = float(degrees)
        else:
            raise ValueError("Angle.setDegrees: Value Error")
        self.degrees= degrees
        return degrees
                  
    def setDegreesAndMinutes(self, degrees):
        if(isinstance(degrees,basestring)):

            try:
                degreeslist = degrees.split('d')
            except:
                raise ValueError('Angle.setDegreesAndMinutes:')
            if (len(degreeslist)== 2):
                D = degreeslist[0]
                M = degreeslist[1]
                try:
                    D = int(D)
                except:
                    raise ValueError('Angle.setDegreesAndMinutes:')
                try:
                    M = float(M)
                except:
                    raise ValueError('Angle.setDegreesAndMinutes:')
                if (D is not None and D !=''):
                    if (M is not None and M !='' and M >=0):
                        M_list = str(M).split('.')
                        if len(M_list)==1:
                            pass
                        elif len(M_list)==2:
                            M_1 = int(M_list[1]) 
                        if 0<= M_1 <= 9: 
                            D_degrees= int(D)
                            D = int(D)
                            if D >= 0 and D < 360:
                                D = D 
                            elif D <0 and D>= -360:
                                D = abs(D) 
                            elif D >= 360:
                                D = D % 360
                            elif D< -360:
                                D =  D% 360    
                            M = float(M)
                            M = M/60
                            degrees = abs(int(D))+float(M)
                            degrees = float(degrees)
                            if D_degrees < 0 and D_degrees > -360:
                                degrees = 360 -degrees 
                            self.setDegrees(degrees)
                            return self.degrees
                        else:
                            raise ValueError('Angle.setDegreesAndMinutes:')
                    else:
                        raise ValueError('Angle.setDegreesAndMinutes:')
            else:
                raise ValueError('Angle.setDegreesAndMinutes:')
        else:
            raise ValueError('Angle.setDegreesAndMinutes:')       
            
            return
                
    def add(self, angle=0):
        if isinstance(angle,Angle):
            self.degrees = self.degrees + angle.degrees
            self.setDegrees(self.degrees)
            return float(self.degrees)
        else:
            raise ValueError('Angle.add:')
                                            
        
        
    def subtract(self, angle=0):
        if isinstance(angle,Angle):
            self.degrees = self.degrees - angle.degrees
            self.setDegrees(self.degrees)
            return float(self.degrees)
        else:
            raise ValueError('Angle.subtract:')
                                            
    def compare(self, angle=0):
        if isinstance(angle,Angle):
            angle.degrees = angle.degrees
            if self.degrees > angle.degrees:
                return 1
            if self.degrees == angle.degrees:
                return 0
            if self.degrees < angle.degrees:
                return -1
        else:
            raise ValueError('Angle.compare:')
        
    def getString(self):
        angleDegreeInt = int(self.degrees)
        angleMinuteFloat = self.degrees-angleDegreeInt
        angleMinute=round(angleMinuteFloat * 60, 1)
        angleDegreeString = str(angleDegreeInt) + "d" + str(angleMinute)
        return angleDegreeString   
 
        
    def getDegrees(self):
        return self.degrees
