import numpy as np
from scipy.special import factorial2

class shell:
    def __init__(self,l,exp,coef,coord):
        self.l = l
        self.exp = exp
        self.coef = coef
        self.coord = np.array(coord)
        self.k = len(exp)
        
        #normalizacion
        for i in range(self.k):
            coef[i] = coef[i]*(2*exp[i]/np.pi)**(3/4)*(4*exp[i])**(l/2)
            
        norm = 0
        for j in range(self.k):
            for k in range(self.k):
                norm += coef[j]*coef[k]*(np.pi/(exp[j]+exp[k]))**(3/2)/(2*(exp[j]+exp[k]))**(l)

        for i in range(self.k):
            coef[i] = coef[i]/np.sqrt(norm)
        
        self.orientaciones = []
        i = 0
        for lx in range(l,-1,-1):
            for ly in range(l-lx,-1,-1):
                lz = l-lx-ly
                self.orientaciones.append([i,lx,ly,lz])      
                i = i + 1

        self.N = np.ones(int((l+1)*(l+2)/2))
        for i,lx,ly,lz in self.orientaciones:
            self.N[i] = np.sqrt(1/(factorial2(2*lx-1)*factorial2(2*ly-1)*factorial2(2*lz-1)))

class shell_pair:
    def __init__(self,g_a,g_b):
        
        self.g_a = g_a
        self.g_b = g_b
        
        self.exp = np.add.outer(g_a.exp, g_b.exp).flatten()
        self.coef = np.multiply.outer(g_a.coef, g_b.coef).flatten()
        
        self.coord = []
        self.ab = []
        for i in range(g_a.k):
            for j in range(g_b.k):
                self.coord.append((g_a.exp[i]*g_a.coord+g_b.exp[j]*g_b.coord)/(g_a.exp[i]+g_b.exp[j]))
                self.ab.append((g_a.exp[i],g_b.exp[j]))

                
        self.alpha = []
        for i in range(g_a.k):
            for j in range(g_b.k):
                self.alpha.append((g_a.exp[i]*g_b.exp[j])/(g_a.exp[i]+g_b.exp[j]))
                                
        self.k = len(self.exp)            
