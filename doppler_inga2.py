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

# hibabecsles
Frerror = 1
Sperror = (340 * 1000)/(Freq**2) * Frerror
Perror = Sperror
Alpherror = Alpha * np.sqrt( (Perror/Pos)**2 + (1/71)**2 )

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
fig, axs = plt.subplots(2, sharex=True)
fig.suptitle('Inga mérése Doppler-effektussal')

fitlim=600
axs[0].plot(Time, Alpha, '.', color='crimson', label = 'Mért szögkitérés a sebesség numerikus integrálásából')
axs[1].plot(Time, Pos, '.', color='orange', label = 'A lengés irányába vett elmozdulás numerikus integrálásból')

# hiba abrazolasa es szinuszfuggveny illesztes hibaval
axs[0].errorbar(Time, Alpha, yerr=Alpherror, fmt=' ', color='#FE6F5E')
axs[1].errorbar(Time, Pos, yerr=Perror, fmt=' ', color='yellow')
popt, pcov = curve_fit(func, Time[:fitlim], Speed[:fitlim], sigma = Sperror[:fitlim], p0=[1, 3.14,-3.14], method='lm')

# szogkiteres, elomzdulas illesztesbol
TheoAlph = -popt[0]/(popt[1]*0.71) * np.cos( popt[1] * Time  + popt[2])
TheoPos = -popt[0]/popt[1] * np.cos( popt[1] * Time + popt[2])


print(popt, '\n',pcov)

# uj amplitudo hibaja kiteresre
newamp_err = popt[0]/popt[1] * np.sqrt( (np.sqrt(pcov[0][0])/popt[0])**2 + (np.sqrt(pcov[1][1])/popt[1])**2 )
# szogre
newamp_err2 = popt[0]/(popt[1] *0.71 ) * np.sqrt( (np.sqrt(pcov[0][0])/popt[0])**2 + (np.sqrt(pcov[1][1])/popt[1])**2 + (1/71)**2 )


axs[0].plot(Time[:fitlim], TheoAlph[:fitlim], 'orange',
             label = '$\\varphi (t) =$ ( ' + str( round(1/popt[0]/(popt[1] *0.71 ), 4) ) + ' $\pm$ ' + str( round(newamp_err2, 4) ) +' ) $\cdot \cos(($'
             + str( round(popt[1], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[1][1]), 4) ) + '$) \cdot t)$ rad')
axs[1].plot(Time[:fitlim], TheoPos[:fitlim], 'crimson',
             label = '$s (t) =$ ( ' + str( round(1/popt[0]/popt[1], 4) ) + ' $\pm$ ' + str( round(newamp_err, 4) ) +' ) $\cdot \cos(($'
             + str( round(popt[1], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[1][1]), 4) ) + '$) \cdot t)$ m')

plt.xlabel('$t$ (s)')
axs[0].set_ylabel('$\\varphi$ (rad)')
axs[1].set_ylabel('$s$ (m)')

for ax in axs:
    ax.legend(loc='upper left')
    ax.grid()

# grafikon mentese
plt.savefig('doppler_inga2', dpi=300)