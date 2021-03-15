import numpy as np
import matplotlib.pyplot as plt

# adatok betoltese
data1 = np.loadtxt('meresek\\porszivo.csv', delimiter='\t', skiprows=1)
data2 = np.loadtxt('meresek\\2porszivo_valaszfal.csv', delimiter='\t', skiprows=1)
data3 = np.loadtxt('meresek\\2otthoni_hatter.csv', delimiter='\t', skiprows=1)
data4 = np.loadtxt('meresek\\2porszivo_ajto.csv', delimiter='\t', skiprows=1)
data5 = np.loadtxt('meresek\\2porszivo_fal.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Freq1 = data1[:,0]
Amp1 = data1[:,1]
Freq2 = data2[:,0]
Amp2 = data2[:,1]
Freq3 = data3[:,0]
Amp3 = data3[:,1]
Freq4 = data4[:,0]
Amp4 = data4[:,1]
Freq5 = data5[:,0]
Amp5 = data5[:,1]

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
plt.loglog(Freq3, Amp3, 'goldenrod', label='Az otthoni háttérzaj')
plt.loglog(Freq1, Amp1, label='Csillapítatlan porszívó')
plt.loglog(Freq2, Amp2, 'crimson', label='Ajtóval letakart porszívó')
plt.loglog(Freq4, Amp4, label='Zárt ajtó mögött álló porszívó')
plt.loglog(Freq5, Amp5, label='Fal mögött álló porszívó')
plt.title('Porszívó Zajspektruma különböző csillapítások esetén')
plt.xlabel('$\\nu$ (Hz)')
plt.ylabel('Amplitude (a.u.)')
plt.grid()
plt.legend(loc='lower left')

# grafikon mentese
plt.savefig('csill_porszivo_zajspektrum', dpi=300)