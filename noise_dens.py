import numpy as np
import matplotlib.pyplot as plt

# adatok betoltese
data1 = np.loadtxt('meresek\\hajszarito_gyenge.csv', delimiter='\t', skiprows=1)
data2 = np.loadtxt('meresek\\hajszarito_eros.csv', delimiter='\t', skiprows=1)
data3 = np.loadtxt('meresek\\2otthoni_hatter.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Freq1 = data1[:,0]
Amp1 = data1[:,1]
Freq2 = data2[:,0]
Amp2 = data2[:,1]
Freq3 = data3[:,0]
Amp3 = data3[:,1]

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
plt.loglog(Freq3, Amp3, 'goldenrod', label='Az otthoni háttérzaj FFT-ja')
plt.loglog(Freq1, Amp1, label='Alacsony teherlésű hajszárító jelének FFT-ja')
plt.loglog(Freq2, Amp2, 'crimson', label='Magas teherlésű hajszárító jelének FFT-ja')
plt.title('Hajszárító Zajspektruma')
plt.xlabel('$\\nu$ (Hz)')
plt.ylabel('Amplitude (a.u.)')
plt.grid()
plt.legend(loc='lower left')

# grafikon mentese
plt.savefig('hajszarito_zajspektrum', dpi=300)