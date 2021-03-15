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

# hibabecsles
Frerror = 1
Sperror = (340 * 1000)/(Freq**2) * Frerror

# Az elmozdulas numerikus integrálása a sebessegbol trapezszaballyal
Pos = np.zeros((Time.size))
for i, val in enumerate(Speed):
    Pos[i] = trapz(Speed[:i], Time[:i])
# szogkiteres meghatarozasa az elmozdulasbol ha l = 71 cm
Alpha = Pos / 0.71

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
fig, axs = plt.subplots(2, sharex=True)
fig.suptitle('Inga mérése Doppler-effektussal')

axs[0].plot(Time, Freq, 'C0.', label = '$\\nu = 1000$ Hz-es szinuszjel mért frekvenciája')
axs[1].plot(Time, Speed, 'g.', label = 'Mért sebesség a Doppler-effektus alapján')

# hiba abrazolasa es szinuszfuggveny illesztes hibaval
axs[0].errorbar(Time, Freq, yerr=Frerror, fmt=' ', color='lightskyblue')
axs[1].errorbar(Time, Speed, yerr=Sperror, fmt=' ', color='springgreen')

fitlim=600

popt, pcov = curve_fit(func, Time[:fitlim], Speed[:fitlim], sigma = Sperror[:fitlim], p0=[1, 3.14,-3.14], method='lm')

print(popt, '\n',pcov)

axs[1].plot(Time[:fitlim], func(Time, *popt)[:fitlim], 'y-',
            label = '$v(t) =$ ( ' + str( round(popt[0], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[0][0]), 4) ) +' ) $\cdot \sin(($'
            + str( round(popt[1], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[1][1]), 4) ) + '$) \cdot t)$ m/s')

plt.xlabel('$t$ (s)')
axs[0].set_ylabel('$\\nu$ (Hz)')
axs[1].set_ylabel('$v$ (m/s)')

for ax in axs:
    ax.legend(loc='upper left')
    ax.grid()

# grafikon mentese
plt.savefig('doppler_inga', dpi=300)