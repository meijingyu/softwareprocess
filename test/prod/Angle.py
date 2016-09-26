from numpy import integer
class Angle():
    def __init__(self):
        self.degrees = 0    #   set to 0 degrees 0 minutes
        
    
    def setDegrees(self, degrees):
        if(isinstance(degrees, float)) or (isinstance(degrees, int)):
            if degrees >= -360 and degrees <= 0:
                degrees = degrees + 360            
            if degrees >=0 and degrees <= 360:
                degrees = degrees 
            if degrees <= -360 or degrees >= 360:
                n = degrees % 360 
                degrees = n
                degrees = float(degrees)
                return degrees
        else:
            raise ValueError("error")
               
                  
    def setDegreesAndMinutes(self, degrees):
        if(isinstance(degrees,basestring)):
            degreeslist = degrees.split('d')
            D = degreeslist[0]
            M = degreeslist[1]
            M = float(M)
            if M > 60:
                M = M%6
                D = D + (M/60)
            M = str(M)               
            Mlist = M.split('.')
            Mlist[0] = int(Mlist[0])
            Mlist[1] = int(Mlist[1])
            if Mlist[1] == 0:
                M = Mlist[0]
            D = int(D)
            if len(degrees.split('d')) == 2 and M >= 0 and Mlist[1] <= 9:
                if D >= -360 and D <= 0:
                    D = D + 360            
                if D >=0 and D <= 360:
                    D = D 
                if degrees <= -360 or degrees >= 360:
                    n = D % 360 
                    D = n
                    M = int(M)
                    M = M/6 
                    D = str(D)
                    M = str(M)
                    
                    degrees = D+'.'+M
                    degrees = float(degrees)
                    
                    return degrees
            else:
                raise ValueError('error')
        else:
            raise ValueError('error')       
            
            return
                
    def add(self, angle):
        if isinstance(angle,Angle):
            self.degrees = self.degrees + angle.degrees
        else:
            raise ValueError('error')
                                            
        
        
    
    def subtract(self, angle):
        if isinstance(angle.degrees,Angle):
            angle.degrees = self.setDegreesAndMinutes(angle.degrees)
        else:
            angle.degrees = self.setDegrees(angle.degrees)
        if isinstance(self.degrees,basestring):
            self.degrees = self.setDegreesAndMinutes(self.degrees)
        else:
            self.degrees = self.setDegrees(self.degrees)
            
        self.degrees = self.degrees - angle.degrees
        
        self.degrees = self.setDegrees(self.degrees)

    
    def compare(self, angle):
        if isinstance(angle,Angle):
            angle.degrees = angle.degrees
            if self.degrees > angle.degrees:
                return -1
            if self.degrees == angle.degrees:
                return 0
            if self.degrees < angle.degrees:
                return 1
        else:
            raise ValueError('error')
        
    def getString(self):
        intdegrees = int(self.degrees)
        flodegrees = self.degrees - intdegrees
        strdegrees = str(intdegrees)+'d'+str(flodegrees)
        
        return strdegrees
        
    def getDegrees(self):
        return self.degrees
        