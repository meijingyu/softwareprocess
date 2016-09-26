import math
class TCurve(object):

# outward facing methods
    def __init__(self, n=None):
        functionName = "TCurve.__init__: "
        if(n == None):
            raise ValueError(functionName + "invalid n")
        if(not(isinstance(n, int))):
            raise ValueError(functionName + "invalid n")
        if((n < 2) or (n >= 30)):
            raise ValueError(functionName + "invalid n")
        self.n = n

    
    def p(self, t=None, tails=1):
        functionName = "TCurve.p: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if(not(isinstance(t, float))):
            raise ValueError(functionName + "invalid t")
        if(t < 0.0):
            raise ValueError(functionName + "invalid t")
        
        if(not(isinstance(tails, int))):
            raise ValueError(functionName + "invalid tails")
        if((tails != 1) & (tails != 2)):
            raise ValueError(functionName + "invalid tails")
        
        constant = self. calculateConstant(self.n)
        integration = self.integrate(t, self.n, self.f)
        if(tails == 1):
            result = constant * integration + 0.5
        else:
            result = constant * integration * 2
            
        if(result > 1.0):
            raise ValueError(functionName + "result > 1.0")
        
        return result
        
# internal methods
    def gamma(self, x):
        if(x == 1):
            return 1
        if(x == 0.5):
            return math.sqrt(math.pi)
        return (x - 1) * self.gamma(x - 1)
    
    def calculateConstant(self, n):
        n = float(n)
        numerator = self.gamma((n + 1.0) / 2.0)
        denominator = self.gamma(n / 2.0) * math.sqrt(n * math.pi)
        result = numerator / denominator
        return result
    
    def f(self, u, n):
        n = float(n)
        base = (1.0 + (u ** 2) / n)
        exponent = -(n + 1.0) / 2.0
        result = base ** exponent
        return result
    def f_1(self, u, n):
        return u
    def f_2(self,u, n): 
        return u**2
    def f_3(self,u, n): 
        return u**6
    def f_4(self,u, n): 
        return u**100
     
    
    def integrate(self, t, n, f):
        epsilon = 0.001
        simpsonOld = 0.0
        simpsonNew = epsilon
        highBound =t 
        lowBound =0.0
        s=4.0
        Sim =f(lowBound,n)
        while (abs((simpsonNew - simpsonOld ) / simpsonNew) > epsilon):
            simpsonOld = simpsonNew
            w = (highBound - lowBound) / s
            W= w/3.0
            a=2
            while (a <=s) :
                Sim= Sim+4.0*f((a-1)*w,n)
                a=a+2
            a=3
            while (a <=s-1):
                Sim=Sim+2.0*f((a-1)*w,n)
                a=a+2
            Sim =Sim+f(s*w,n)
            simpsonNew = W * Sim
            s=s*2 
            return simpsonNew

        
        
    
        
            
        
