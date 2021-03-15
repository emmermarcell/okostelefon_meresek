import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapz

def func(x, a, omega, phi):
    return a * np.sin(omega * x + phi)

# adatok betoltese
data = np.loadtxt('meresek\\3doppler_inga6ts15.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Time = data[:,0]
Freq = data[:,1]
Speed = data[:,2]

# nan adatok kivetele
for idx, val in enumerate(Freq):
    if np.isnan(val):
        Freq[idx] = 1000
        Speed[idx] = 0
        
# Az elmozdulas numerikus integrálása a sebessegbol trapezszaballyal
Pos = np.zeros((Time.size))
for i, val in enumerate(Speed):
    Pos[i] = trapz(Speed[:i]-np.mean(Speed), Time[:i])
    
# szogkiteres meghatarozasa az elmozdulasbol ha l = 71 cm
Alpha = Pos / 0.71
Height = 0.71 *(1- np.cos(Alpha))

# hibabecsles
Frerror = 1
Sperror = (340 * 1000)/(Freq**2) * Frerror
Perror = Sperror
Alpherror = Alpha * np.sqrt( (Perror/Pos)**2 + (1/71)**2 )
Herror = np.sqrt( ((1-np.cos(Alpha))*0.01)**2 + (0.71*np.sin(Alpha)*Alpherror)**2 )

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
plt.title('Inga mérése Doppler-effektussal')

fitlim=600
plt.plot(Time, Height, '.',label = 'A nyugalmi helyzethez képesti magasság')

# hiba abrazolasa es szinuszfuggveny illesztes hibaval
plt.errorbar(Time, Height, yerr=Herror, fmt=' ', color='lightskyblue')
popt, pcov = curve_fit(func, Time[:fitlim], Speed[:fitlim], sigma = Sperror[:fitlim], p0=[1, 3.14,-3.14], method='lm')

# szogkiteres illeszztesbol
TheoAlph = -popt[0]/(popt[1]*0.71) * np.cos( popt[1] * Time  + popt[2])
TheoHeight = 0.71 * (1- np.cos(TheoAlph) )

# szogre
newamp_err2 = popt[0]/(popt[1] *0.71 ) * np.sqrt( (np.sqrt(pcov[0][0])/popt[0])**2 + (np.sqrt(pcov[1][1])/popt[1])**2 + (1/71)**2 )


plt.plot(Time[:fitlim], TheoHeight[:fitlim], 'crimson', label= '$h(t) = l \cdot( 1 - \cos  \\varphi )$')

plt.xlabel('$t$ (s)')
plt.ylabel('$h$ (m)')
plt.legend(loc='upper right')
plt.grid()

# grafikon mentese
plt.savefig('doppler_inga3', dpi=300)