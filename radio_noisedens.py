import numpy as np
import matplotlib.pyplot as plt

# adatok betoltese
data1 = np.loadtxt('meresek\\2radiobugas.csv', delimiter='\t', skiprows=1)
data2 = np.loadtxt('meresek\\2otthoni_hatter.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Freq1 = data1[:,0]
Amp1 = data1[:,1]
Freq2 = data2[:,0]
Amp2 = data2[:,1]

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
plt.loglog(Freq2, Amp2, 'goldenrod', label='Az otthoni háttérzaj FFT-ja')
plt.loglog(Freq1, Amp1, label='Autó rádió jelének FFT-ja')
plt.title('Üres frekvenciára hangolt rádió Zajspektruma')
plt.xlabel('$\\nu$ (Hz)')
plt.ylabel('Amplitude (a.u.)')
plt.grid()
plt.legend(loc='lower left')

# grafikon mentese
plt.savefig('radiobugas_zajspektrum', dpi=300)