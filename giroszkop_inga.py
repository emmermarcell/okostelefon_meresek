import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, T, phi):
    return a * np.sin(((2 * np.pi) / T) * x + phi)

# adatok betoltese
data = np.loadtxt('meresek\\4inga_giroszkop.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Time = data[:,0]-2.5
Gir = data[:,1]

# hibabecsles
Girror = np.full( (Gir.size), 0.0036)

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fitinf = 0
fitsup = -2000
# abrazolas, tengelyek elnevezese, cim, stb.
plt.title('Inga lengésidejének mérése giroszkóppal')
plt.plot(Time[:fitsup], Gir[:fitsup], '.', color='crimson', label = 'Mérési pontok')

# hiba abrazolasa es szinuszfuggveny illesztes hibaval
plt.errorbar(Time[:fitsup], Gir[:fitsup], yerr=Girror[:fitsup],
             fmt=' ', color='#FE6F5E')

popt, pcov = curve_fit(func, Time[fitinf:fitsup], Gir[fitinf:fitsup],
                       sigma = Girror[fitinf:fitsup], method='trf',
                       p0 = [3.35895184, 1.6928995, 4.31165587])

print(popt, '\n',pcov)

plt.plot(Time[fitinf:fitsup], func(Time, *popt)[fitinf:fitsup], 'y',
            label = '$\\beta(t) =$ (' + str( round(np.abs(popt[0]), 4) ) + ' $\pm$ '
            + str( round(np.sqrt(pcov[0][0]), 4) ) +') $\cdot \sin( 2 \pi /($'
            + str( round(popt[1], 4) ) + ' $\pm$ ' + str( round(np.sqrt(pcov[1][1]), 4) )
            + '$) \cdot t)$ rad/s')

plt.xlabel('$t$ (s)')
plt.ylabel('$\\beta$ (rad/s)')
plt.legend(loc='upper left')
plt.grid()

# grafikon mentese
plt.savefig('giroszkop_inga', dpi=300)