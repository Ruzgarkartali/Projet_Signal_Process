import numpy as np
from scipy.io import wavfile
from utils import *
import matplotlib.pyplot as plt

import scipy.signal as sgl

# Ce test n'est pas parfait


Signal, Fe = wavfile.read("male")
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