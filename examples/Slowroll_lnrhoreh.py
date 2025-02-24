import pyaspic
import numpy as np

class Slowroll():
    
    def __init__(self, model, w, lnRhoReh, A_s, *parameters):
#        Pstar = np.exp(A_s)/(10**10)
        Pstar = A_s
        C = np.euler_gamma+np.log(2)-2
        f = 5
        g = 7
        bfoldstar = 0.0
        
        self.model = model

        if self.model == 'ni':
            parameters = tuple([10**(parameters[0])] + list(parameters)[1:])

        if self.model == 'li':
            parameters = tuple([10**(parameters[0])] + list(parameters)[1:])

        self.xstar, self.bfoldstar = getattr(pyaspic,f'{self.model}_x_star')(*parameters, w, lnRhoReh, Pstar, bfoldstar)
        
        self.eps1 = getattr(pyaspic,f'{self.model}_epsilon_one')(self.xstar,*parameters)
        self.eps2 = getattr(pyaspic,f'{self.model}_epsilon_two')(self.xstar,*parameters)
        self.eps3 = getattr(pyaspic,f'{self.model}_epsilon_three')(self.xstar,*parameters)
        
        self.a0s = 1 -2*(C+1)*self.eps1 -C*self.eps2 +(2*C**2+2*C+np.pi**2/2-f)*self.eps1**2 \
                   +(C**2-C+7*np.pi**2/12-g)*self.eps1*self.eps2 +(1/2*C**2+np.pi**2/8-1)*self.eps2**2 \
                   +(-1/2*C**2+np.pi**2/24)*self.eps2*self.eps3
        self.a1s = -2*self.eps1-self.eps2+2*(2*C+1)*self.eps1**2+(2*C-1)*self.eps1*self.eps2+C*self.eps2**2 \
                   -C*self.eps2*self.eps3
        self.a2s = 4*self.eps1**2+2*self.eps1*self.eps2+self.eps2**2-self.eps2*self.eps3
        self.a0t = 1-2*(C+1)*self.eps1 +(2*C**2+2*C+np.pi**2/2-f)*self.eps1**2+(-C**2-2*C+np.pi**2/12-2)*self.eps1*self.eps2
        self.a1t = -2*self.eps1+2*(2*C+1)*self.eps1**2-2*(C+1)*self.eps1*self.eps2
        self.a2t = 4*self.eps1**2-2*self.eps1*self.eps2
        
        self.n_s = 1+self.a1s/self.a0s
        self.alpha_s = (self.a2s*self.a0s-self.a1s**2)/self.a0s**2
        self.n_t = self.a1t/self.a0t
        self.alpha_t = (self.a2t*self.a0t-self.a1t**2)/self.a0t**2
        self.r = 16*self.eps1

        if self.model == 'pli':
            self.xend = 100
        else:
            self.xend = getattr(pyaspic,f'{self.model}_x_endinf')(*parameters)
        
        self.eps1end = getattr(pyaspic,f'{self.model}_epsilon_one')(self.xend,*parameters)
        self.VendOverVstar = (getattr(pyaspic,f'{self.model}_norm_potential')(self.xend,*parameters))/(getattr(pyaspic,f'{self.model}_norm_potential')(self.xstar,*parameters))
        self.lnRhoEnd = pyaspic.ln_rho_endinf_leadorder(Pstar, self.eps1, self.eps1end, self.VendOverVstar)
