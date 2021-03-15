import numpy as np
import matplotlib.pyplot as plt
                 
f = 5000
    
# adatok betoltese
data = np.loadtxt('meresek\\sine' +str(f) +'.csv', delimiter='\t', skiprows=1)
raw_data = np.loadtxt('meresek\\sine' +str(f) +'_raw_data.csv', delimiter='\t', skiprows=1)

# tengelyek definialasa
Freq = data[:,0]
Amp = data[:,1]
Time = raw_data[:-1,0]
Raw_kiteres = raw_data[:-1,1]

# elmeleti tokeletes jelalak
sample_rate = 2048
t = np.linspace(0, np.amax(Time)  ,sample_rate)
theo_signal = np.amax(Raw_kiteres) * np.sin(2 * np.pi * f * t)
theo__fft = np.fft.rfft(theo_signal)

# kovarianciamatrix a valodi es az elmeleti jelek kozott
SigCov = np.abs( np.cov(theo__fft[:sample_rate//2-1], Amp[:sample_rate//2-1])[0][1] )
SigCor = SigCov / ( np.sqrt(np.var(theo__fft[:sample_rate//2-1])) * np.sqrt(np.var(Amp[:sample_rate//2-1])) )
SigCor = round(SigCor, 5)

# betutipus beallitasa
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# abrazolas, tengelyek elnevezese, cim, stb.
plt.loglog(Freq, Amp, label='Mért jel FFT-ja')
plt.loglog(Freq[:sample_rate//2-1], np.abs(theo__fft[:sample_rate//2-1]), '--', label='illesztés FFT-ja')

plt.title('Szinuszhullám FFT, $\\nu = ' +str(f) +'$ Hz, Corr = ' + str(SigCor))
plt.xlabel('$\\nu$ (Hz)')
plt.ylabel('Amplitude (a.u.)')
plt.grid()
plt.legend()

# grafikon mentese
plt.savefig('sine' +str(f), dpi=300)