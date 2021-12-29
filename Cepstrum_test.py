import numpy as np
from scipy.io import wavfile
from utils import *
import matplotlib.pyplot as plt

import scipy.signal as sgl

# Ce test n'est pas parfait

'''
def Compute_cepstrum(Signal, Frqsample):

    Framesize = Signal.size                                           
    Signalw = np.hamming(Framesize) * Signal                          #on utilise le filtre de hamming
    Dt = 1/Frqsample
    Frqvector = np.fft.rfftfreq(Framesize, D=Dt)                      #on utilise la fonction issue de numpy pour avoir la Transfo. de Fourier discr.
    F = np.fft.rfft(Signalw)
    logF = np.log(np.abs(F))                                          #il est conseillé de passer en log 
    #plt.plot(frqvector, D=Dt)
    #plt.show()
    Cepstrum = np.fft.rfft(logF)
    Df = Frqvector[1] - Frqvector[0]
    qfrvect = np.fft.rfftfreq(logF.size, Df)
    #plt.plot(qfrvector, np.abs(Cepstrum))
    #plt.xlabel('quefrency (s)')
    #plt.show()
    return qfrvect, Cepstrum


def Cepstrum_frqfond(Signal, Frqsample,Fmax=500, Fmin=60):

    qfrvect, Cepstrum = Compute_cepstrum (Signal, Frqsample)
    Domainevalide = (qfrvect > 1/Fmax) & (qfrvect <= 1/Fmin)        #on définit la région où on prend le maxima
    Maxqfr = np.argmax(np.abs(Cepstrum)[Domainevalide])
    F0 = 1/qfrvect[Domainevalide][Maxqfr]                           #on trouve la fréquence fondamentale
    return F0

def Cepstrum(Signal, Fe, threshold):                                #threshold = seuil
    Cepstrumlist = []
    Energie = Energy(Signal)

    if Energie > threshold:

            SignalArr = np.array(Signal)   

            Ffdmtl = Cepstrum_frqfond(SignalArr, Fe)

            Cepstrumlist.append(Ffdmtl)    

    else:

            Ffdmtl = 0
            Cepstrumlist.append(Ffdmtl)


    CepstrumArr = np.array(Cepstrumlist)  
    CepstrumMoy = abs(np.mean(CepstrumArr))  
    return Cepstrumlist
'''

Signal, Fe = wavfile.ReadFiles("male")
print("Fe : ", Fe)
print("data", Signal)

plt.plot(Signal)
plt.show()

Signalnorm = normalisation(Signal)

plt.plot(Signalnorm)
plt.show()

Tss = 100
Tw = 100

Signalnormsplit = split(Signalnorm, Fe, Tss, Tw)
plt.plot(Signalnormsplit)
plt.show()

F1 = 100
F2 = 500
F3 = 1000
S1 = []
S2 = []
S3 = []
Fe = 16000
somme = []

for t in range(800):
    S1.append(np.sin(2 * np.pi * F1 * (t / Fe)))
    S2.append(np.sin(2 * np.pi * F2 * (t / Fe)))
    S3.append(np.sin(2 * np.pi * F3 * (t / Fe)))

# print("f1 = "+str(Cepstrum(S1,Fe,20)))
# print("f2 = "+str(cepstrum(S2,Fe,1)))
# print("f3 = "+str(cepstrum(S3,Fe,1)))
# print(len(cepstrum(S1,Fe,100)))
# valeurs espérées

Signalnormsplitenergycepstrum = Cepstrum(Signalnormsplit, Fe, 40)
plt.plot(Signalnormsplitenergycepstrum)
plt.show()