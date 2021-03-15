import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, T, phi):
    return a * np.sin(((2 * np.pi) / T) * x + phi)

# adatok betoltese
data = np.loadtxt('meresek\\4inga_accwog.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Time = data[:,0]-1
Acc = data[:,2]

# hibabecsles
Accor = np.full( (Acc.size), 0.041) + 0.1 * Acc

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fitinf = 100
fitsup = 600
# abrazolas, tengelyek elnevezese, cim, stb.
plt.title('Inga lengésidejének mérése gyorsulásmérő szenzorral')
plt.plot(Time[:fitsup], Acc[:fitsup], 'C0.', label = 'Mérési pontok')

# hiba abrazolasa es szinuszfuggveny illesztes hibaval
plt.errorbar(Time[:fitsup], Acc[:fitsup], yerr=Accor[:fitsup],
             fmt=' ', color='lightskyblue')

popt, pcov = curve_fit(func, Time[fitinf:fitsup], Acc[fitinf:fitsup],
                       sigma = Accor[fitinf:fitsup], method='trf',
                       p0 = [3.35895184, 1.6928995, 4.31165587])

print(popt, '\n',pcov)

plt.plot(Time[fitinf:fitsup], func(Time, *popt)[fitinf:fitsup], 'y-',
            label = '$a(t) =$ (' + str( round(popt[0], 4) ) + ' $\pm$ '
            + str( round(np.sqrt(pcov[0][0]), 4) ) +') $\cdot \sin( 2 \pi /($'
            + str( round(popt[1], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[1][1]), 4) )
            + '$) \cdot t)$ m/s$^2$')

plt.xlabel('$t$ (s)')
plt.ylabel('$a$ (m/s$^2$)')
plt.legend(loc='upper left')
plt.grid()

# grafikon mentese
plt.savefig('gyorsulas_inga2', dpi=300)