import pyaspic
import numpy as np
Pstar = 2.2030e-09 #powerAmpScalar
lnRhoNuc = -187.77
#alpha = np.sqrt(2.)*10**(-5./2.)
alpha = 4.9193495029447058e-3/1.1
pred_file = []
while alpha <= 0.9:
    alpha = alpha*1.1
    w=0.
    lnRhoRehMin = lnRhoNuc
    lnRhoRehMax = pyaspic.pli_lnrhoreh_max(alpha, Pstar)
    print(f'alpha={alpha} lnRhoRehMin={lnRhoRehMin} lnRhoRehMax={lnRhoRehMax}')
    npts = 2
    for i in range(1, npts + 1):
        lnRhoReh = lnRhoRehMin + (lnRhoRehMax - lnRhoRehMin)*(i - 1)/(npts - 1)

        bfoldstar = 0.0
        xstar = pyaspic.pli_x_star(alpha,w,lnRhoReh,Pstar,bfoldstar)

        print(f'lnRhoReh={lnRhoReh} bfoldstar={bfoldstar} xstar={xstar}')


        eps1 = pyaspic.pli_epsilon_one(xstar,alpha)
        eps2 = pyaspic.pli_epsilon_two(xstar,alpha)
        eps3 = pyaspic.pli_epsilon_three(xstar,alpha)


        logErehGeV = pyaspic.log_energy_reheat_ingev(lnRhoReh)
        Treh = 10.0**(logErehGeV - 0.25*np.log10(np.pi**2/30) )

        ns = 1 - 2*eps1 - eps2
        r =16*eps1
        pred_file.append([alpha,eps1,eps2,eps3,r,ns,Treh])
pred = np.array(pred_file)
np.savetxt('pli_predic.dat', pred)
