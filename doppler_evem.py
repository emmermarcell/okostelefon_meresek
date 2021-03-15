import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x + b

# adatok betoltese
data = np.loadtxt('meresek\\3doppler_evem1.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Time = data[:,0]
Freq = data[:,1]
Speed = -data[:,2]

for idx, val in enumerate(Freq):
    if np.isnan(val):
        Freq[idx] = 1000
        Speed[idx] = 0
        
for idx, val in enumerate(Time):
    if val > 3:
        print(idx)
        break

Frerror = 2
Sperror = (340 * 1000)/(Freq**2) * Frerror

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
fig, axs = plt.subplots(2, sharex=True)
fig.suptitle('Egyenes vonalú egyenletes mozgás mérése Doppler-effektussal')

axs[0].plot(Time, Freq, 'C0.', label = '$\\nu = 1000$ Hz-es szinuszjel mért frekvenciája')
axs[1].plot(Time, Speed, 'g.', label = 'Mért sebesség a Doppler-effektus alapján')

# hiba abrazolasa es egyenes illesztes hibaval
axs[0].errorbar(Time, Freq, yerr=Frerror, fmt=' ', color='lightskyblue')
axs[1].errorbar(Time, Speed, yerr=Sperror, fmt=' ', color='springgreen')
popt, pcov = curve_fit(lambda x, b: func(x, 0, b), Time[40:-10], Speed[40:-10], sigma = Sperror[40:-10], absolute_sigma=True)
axs[1].plot(Time[40:-10], func(Time, 0, *popt)[40:-10], 'y-',
            label = 'Illesztés: $v = $(' + str( round(popt[0], 4) ) + ' $\pm$ ' + str( round(np.sqrt(np.diag(pcov))[0], 4) ) + ') m/s' )

print(Time[-10] - Time[40])

plt.xlabel('$t$ (s)')
axs[0].set_ylabel('$\\nu$ (Hz)')
axs[1].set_ylabel('$v$ (m/s)')

for ax in axs:
    ax.legend(loc='upper left')
    ax.grid()

# grafikon mentese
plt.savefig('doppler_evem1', dpi=300)